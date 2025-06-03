from math import fabs
from typing import Any, Dict, Optional

from pandas import DataFrame

import rogii_solo.well
from rogii_solo.base import ComplexObject, ObjectRepository
from rogii_solo.calculations.base import calc_segment_vs_length, get_nearest_values
from rogii_solo.calculations.converters import meters_to_feet
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.trajectory import (
    calculate_trajectory,
    interpolate_trajectory_point,
)
from rogii_solo.calculations.types import HorizonShift, Segment
from rogii_solo.earth_model import EarthModel
from rogii_solo.exceptions import InterpretationOutOfTrajectoryException
from rogii_solo.horizon import Horizon
from rogii_solo.papi.client import PapiClient
from rogii_solo.papi.types import (
    PapiAssembledSegments,
    PapiStarredHorizons,
    PapiTrajectory,
)
from rogii_solo.types import DataList
from rogii_solo.types import Interpretation as InterpretationType

TVT_DATA_MAX_MD_STEP = 100000


class Interpretation(ComplexObject):
    """
    Represent an :class:`Interpretation` for a :class:`~rogii_solo.well.Well`, containing data
    about :class:`~rogii_solo.horizon.Horizon`, :class:`~rogii_solo.earth_model.EarthModel`, and assembled Segments.
    The :class:`Interpretation` class provides methods to get and process :class:`Interpretation` details.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ...  # Input your client ID
        client_secret = ...  # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        projects = solo_client.set_project_by_name('Project1')
        well = projects.wells.find_by_name('Well1')

        # Get an Interpretation in the Well
        interpretation = well.interpretations.find_by_name('Interpretation1')

        # Get the Well object to which Interpretation belongs
        well = interpretation.well
        print(well.name)

        # Get a unique ID of the Interpretation
        interpretation_uuid = interpretation.uuid
        print(interpretation_uuid)

        # Get the name of the Interpretation
        interpretation_name = interpretation.name
        print(interpretation_name)

        # Get the owner ID of the Interpretation
        interpretation_owner = interpretation.owner
        print(interpretation_owner)

        # Get the sharing mode of the Interpretation
        interpretation_mode = interpretation.mode
        print(interpretation_mode)

        # Get the version of the Interpretation
        interpretation_format = interpretation.format
        print(interpretation_format)
    """

    def __init__(self, papi_client: PapiClient, well: 'rogii_solo.well.Well', **kwargs):
        super().__init__(papi_client)

        self.well = well
        """The well object to which :class:`Interpretation` belongs."""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`Interpretation`."""

        self.name: Optional[str] = None
        """Name of the :class:`Interpretation`."""

        self.mode: Optional[str] = None
        """Sharing mode of the :class:`Interpretation`."""

        self.owner: Optional[int] = None
        """User ID of the :class:`Interpretation`'s creator or owner."""

        self.properties: Optional[DataList] = None
        """Dictionary of :class:`Interpretation` specific visualization and display settings."""

        self.format: Optional[str] = None
        """Version of the :class:`Interpretation`."""

        self.__dict__.update(kwargs)

        self._assembled_segments_data: Optional[PapiAssembledSegments] = None
        self._horizons: Optional[ObjectRepository[Horizon]] = None
        self._earth_models: Optional[ObjectRepository[EarthModel]] = None
        self._starred_horizons_data: Optional[PapiStarredHorizons] = None
        self._starred_horizon_top: Optional[Horizon] = None
        self._starred_horizon_center: Optional[Horizon] = None
        self._starred_horizon_bottom: Optional[Horizon] = None

    @property
    def assembled_segments(self) -> PapiAssembledSegments:
        """
        Get the assembled Segments data for :class:`Interpretation`,
        including :class:`~rogii_solo.horizon.Horizon` positions and fitted Segments.

        :return: Assembled Segments data.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ...  # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')

            # Get the assembled Segments data
            assembled_segments = interpretation.assembled_segments
            print(assembled_segments.to_dict())
        """
        if self._assembled_segments_data is not None:
            return self._assembled_segments_data

        self._assembled_segments_data = self._papi_client.get_interpretation_assembled_segments_data(
            interpretation_id=self.uuid
        )

        try:
            well_data = self.well.to_dict(get_converted=False)
            calculated_trajectory = calculate_trajectory(
                raw_trajectory=self.well.trajectory.to_dict(get_converted=False),
                well=well_data,
                measure_units=self.well.project.measure_unit,
            )
            self._assembled_segments_data['segments'] = self._get_fitted_segments(
                calculated_trajectory=calculated_trajectory,
                well=well_data,
                measure_units=self.well.project.measure_unit,
            )
        except InterpretationOutOfTrajectoryException:
            self._assembled_segments_data = None

            return {'horizons': None, 'segments': None}

        assembled_horizons_data = self._assembled_segments_data['horizons']
        measure_units = self.well.project.measure_unit

        for horizon in self.horizons.to_dict():
            assembled_horizons_data[horizon['uuid']]['name'] = horizon['name']

            if measure_units != EMeasureUnits.METER:
                assembled_horizons_data[horizon['uuid']]['tvd'] = meters_to_feet(
                    assembled_horizons_data[horizon['uuid']]['tvd']
                )

        return self._assembled_segments_data

    @property
    def horizons(self) -> ObjectRepository[Horizon]:
        """
        Get the collection of :class:`~rogii_solo.horizon.Horizon` objects for this :class:`Interpretation`.

        :return: An :class:`~rogii_solo.base.ObjectRepository` containing the :class:`~rogii_solo.horizon.Horizon`
         instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ...  # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')

            # Get the Horizons for this Interpretation
            horizons = interpretation.horizons
            print(horizons.to_dict())
        """
        if self._horizons is None:
            self._horizons = ObjectRepository(
                objects=[
                    Horizon(interpretation=self, **item)
                    for item in self._papi_client.get_interpretation_horizons_data(interpretation_id=self.uuid)
                ]
            )

        return self._horizons

    @property
    def earth_models(self) -> ObjectRepository[EarthModel]:
        """
        Get the collection of :class:`~rogii_solo.earth_model.EarthModel` objects for this :class:`Interpretation`.

        :return: An :class:`~rogii_solo.base.ObjectRepository` containing :class:`~rogii_solo.earth_model.EarthModel`
         instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ...  # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')

            # Get the EarthModels for this Interpretation
            earth_models = interpretation.earth_models
            print(earth_models.to_dict())
        """
        if self._earth_models is None:
            self._earth_models = ObjectRepository(
                objects=[
                    EarthModel(papi_client=self._papi_client, interpretation=self, **item)
                    for item in self._papi_client.get_interpretation_earth_models_data(interpretation_id=self.uuid)
                ]
            )

        return self._earth_models

    @property
    def starred_horizon_top(self) -> Optional[Horizon]:
        """
        Get the top starred :class:`~rogii_solo.horizon.Horizon` for this :class:`Interpretation`.

        :return: A :class:`~rogii_solo.horizon.Horizon` instance representing the top
         starred :class:`~rogii_solo.horizon.Horizon`, or None if none exists.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ...  # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')

            # Get the top starred Horizon for this Interpretation
            top_starred_horizon = interpretation.starred_horizon_top
            print(top_starred_horizon.to_dict())
        """
        if self._starred_horizon_top is None:
            starred_horizons_data = self._get_starred_horizons_data()
            self._starred_horizon_top = self.horizons.find_by_id(starred_horizons_data['top'])

        return self._starred_horizon_top

    @property
    def starred_horizon_center(self) -> Optional[Horizon]:
        """
        Get the center starred :class:`~rogii_solo.horizon.Horizon` for this :class:`Interpretation`.

        :return: A :class:`~rogii_solo.horizon.Horizon` instance representing the center starred
         :class:`~rogii_solo.horizon.Horizon`, or None if none exists.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ...  # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')

            # Get the center starred Horizon for this Interpretation
            center_starred_horizon = interpretation.starred_horizon_center
            print(center_starred_horizon.to_dict())
        """
        if self._starred_horizon_center is None:
            starred_horizons_data = self._get_starred_horizons_data()
            self._starred_horizon_center = self.horizons.find_by_id(starred_horizons_data['center'])

        return self._starred_horizon_center

    @property
    def starred_horizon_bottom(self) -> Optional[Horizon]:
        """
        Get the bottom starred :class:`~rogii_solo.horizon.Horizon` for this :class:`Interpretation`.

        :return: A :class:`~rogii_solo.horizon.Horizon` instance representing the bottom starred
         :class:`~rogii_solo.horizon.Horizon`, or None if none exists.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ...  # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')

            # Get the bottom starred Horizon for this Interpretation
            bottom_starred_horizon = interpretation.starred_horizon_bottom
            print(bottom_starred_horizon.to_dict())
        """
        if self._starred_horizon_bottom is None:
            starred_horizons_data = self._get_starred_horizons_data()
            self._starred_horizon_bottom = self.horizons.find_by_id(starred_horizons_data['bottom'])

        return self._starred_horizon_bottom

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert the :class:`Interpretation` instance to a dictionary.

        :param get_converted: (Optional) Whether to convert numeric values to the current project's measurement units.
         Default = True.
        :return: Dictionary containing meta information, horizons, segments, and earth model info.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ...  # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')

            # Convert the Interpretation to a dictionary
            interpretation_dict = interpretation.to_dict()
            print(interpretation_dict)
        """
        return self._get_data()

    def to_df(self, get_converted: bool = True) -> InterpretationType:
        """
        Convert the :class:`Interpretation` to a dictionary with Pandas DataFrames.

        :param get_converted: (Optional) Whether to convert numeric values to the current project's measurement units.
         Default = True.
        :return: A dictionary of DataFrames, containing :class:`Interpretation` metadata,
         :class:`~rogii_solo.horizon.Horizon`, :class:`EarthModels` and Segments.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ...  # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')

            # Convert the Interpretation to a dictionary with DataFrames
            interpretation_df = interpretation.to_df()
            print(interpretation_df)
        """
        data = self._get_data()

        return {
            'meta': DataFrame([data['meta']]),
            'horizons': DataFrame(data['horizons']).transpose(),
            'segments': DataFrame(data['segments']),
            'earth_models': DataFrame(data['earth_models']),
        }

    def get_tvt_data(self, md_step: int = 1) -> DataList:
        """
        Get TVT (True Vertical Thickness) list of the :class:`Interpretation`.

        :param md_step: (Optional) Step size for MD (measured depth) when fetching TVT data. Default = 1.
        :return: A list of TVT data points.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ... # Input your client secret
            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            projects = solo_client.set_project_by_name('Project1')
            well = projects.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')

            # Get TVT data for the Interpretation
            tvt_data = interpretation.get_tvt_data(md_step=10)
            print(tvt_data)
        """
        return self._papi_client.get_interpretation_tvt_data(interpretation_id=self.uuid, md_step=md_step)

    def _get_data(self):
        meta = {
            'uuid': self.uuid,
            'name': self.name,
            'mode': self.mode,
            'owner': self.owner,
            'format': self.format,
            'properties': self.properties,
        }

        return {
            'meta': meta,
            'horizons': self.assembled_segments['horizons'],
            'segments': self.assembled_segments['segments'],
            'earth_models': self.earth_models,
        }

    def _get_starred_horizons_data(self):
        if self._starred_horizons_data is None:
            self._starred_horizons_data = self._papi_client.get_interpretation_starred_horizons(self.uuid)

        return self._starred_horizons_data

    def _get_fitted_segments(
        self, calculated_trajectory: PapiTrajectory, well: Dict[str, Any], measure_units: EMeasureUnits
    ):
        segments = self._assembled_segments_data['segments']

        if segments is None:
            return

        fitted_segments = []
        min_trajectory_md = calculated_trajectory[0]['md']
        max_trajectory_md = calculated_trajectory[-1]['md']

        if segments[0]['md'] > max_trajectory_md:
            raise InterpretationOutOfTrajectoryException

        for i, segment in enumerate(segments):
            left_segment = segment

            try:
                right_segment = segments[i + 1]
            except IndexError:
                right_segment = None

            if left_segment['md'] < min_trajectory_md or left_segment['md'] > max_trajectory_md:
                continue
            elif right_segment and (left_segment['md'] <= max_trajectory_md < right_segment['md']):
                fitted_segments.append(
                    self._get_truncated_segment(
                        left=left_segment,
                        right=right_segment,
                        well=well,
                        trajectory=calculated_trajectory,
                        measure_units=measure_units,
                    )
                )
            else:
                nearest_points = get_nearest_values(
                    value=left_segment['md'], input_list=calculated_trajectory, key=lambda it: it['md']
                )

                if len(nearest_points) < 2:
                    # Interpretation start MD = calculated trajectory start MD
                    # Otherwise (MD approximately equal or equal the last trajectory point MD) two points are found
                    interpolated_point = calculated_trajectory[0]
                else:
                    nearest_left_point, nearest_right_point = nearest_points
                    interpolated_point = interpolate_trajectory_point(
                        left_point=nearest_left_point,
                        right_point=nearest_right_point,
                        md=left_segment['md'],
                        well=well,
                        measure_units=measure_units,
                    )

                left_segment['vs'] = interpolated_point['vs']
                fitted_segments.append(left_segment)

        return fitted_segments

    def _get_truncated_segment(
        self, left: Segment, right: Segment, well: Dict[str, Any], trajectory: DataList, measure_units: EMeasureUnits
    ) -> Segment:
        new_shifts = {}
        segment_vs_length = calc_segment_vs_length(
            x1=left['x'], y1=left['y'], x2=right['x'], y2=right['y'], azimuth_vs=well['azimuth']
        )
        nearest_points = get_nearest_values(value=left['md'], input_list=trajectory, key=lambda it: it['md'])

        if len(nearest_points) < 2:
            # Interpretation start MD = calculated trajectory start MD
            # Otherwise (MD approximately equal or equal the last trajectory point MD) two points are found
            interpolated_point = trajectory[0]
        else:
            nearest_left_point, nearest_right_point = nearest_points
            interpolated_point = interpolate_trajectory_point(
                left_point=nearest_left_point,
                right_point=nearest_right_point,
                md=left['md'],
                well=well,
                measure_units=measure_units,
            )

        left_point_vs = interpolated_point['vs']
        right_point_vs = trajectory[-1]['vs']

        truncated_segment_vs_length = fabs(right_point_vs - left_point_vs)
        truncated_segment_height = left['end'] - left['start']
        truncated_segment_new_end = (
            truncated_segment_height * truncated_segment_vs_length / segment_vs_length + left['start']
        )

        for uuid, horizons_shift in left['horizon_shifts'].items():
            shift_height = horizons_shift['end'] - horizons_shift['start']
            shift_new_end = shift_height * truncated_segment_vs_length / segment_vs_length + horizons_shift['start']

            new_shifts[uuid] = HorizonShift(
                uuid=horizons_shift['uuid'], start=horizons_shift['start'], end=shift_new_end
            )

        return Segment(
            uuid=left['uuid'],
            md=left['md'],
            x=left['x'],
            y=left['y'],
            vs=left_point_vs,
            boundary_type=left['boundary_type'],
            start=left['start'],
            end=truncated_segment_new_end,
            horizon_shifts=new_shifts,
        )
