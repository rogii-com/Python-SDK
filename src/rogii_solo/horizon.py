from typing import Dict, Optional

from pandas import DataFrame

import rogii_solo.interpretation
from rogii_solo.base import BaseObject, ObjectRepository
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.calculations.interpretation import (
    get_segments,
    get_segments_boundaries,
    interpolate_horizon,
)
from rogii_solo.calculations.trajectory import calculate_trajectory
from rogii_solo.types import DataList


class Horizon(BaseObject):
    """
    Represent a :class:`Horizon` within an :class:`~rogii_solo.interpretation.Interpretation`, providing access
    to :class:`Horizon` specific data such as points (MD/TVD pairs). A :class:`Horizon` is an
    interface or boundary marker used to correlate and track formations or
    lithologic units across the well.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        interpretation = well.interpretations.find_by_name('Interpretation1')
        horizon = interpretation.horizons.find_by_name('Horizon1')

        # Get the Interpretation associated with this Horizon
        interpretation = horizon.interpretation
        print(interpretation.name)

        # Get the unique ID of the Horizon
        horizon_uuid = horizon.uuid
        print(horizon_uuid)

        # Get the name of the Horizon
        horizon_name = horizon.name
        print(horizon_name)
    """

    def __init__(self, interpretation: 'rogii_solo.interpretation.Interpretation', **kwargs):
        self.interpretation = interpretation
        """Represent the :class:`~rogii_solo.interpretation.Interpretation` of the :class:`Horizon`"""

        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`Horizon`."""

        self.name: Optional[str] = None
        """Name of the :class:`Horizon`."""

        self.__dict__.update(kwargs)

        self._points: Optional[ObjectRepository] = None

    @property
    def points(self) -> ObjectRepository:
        """
        Get the points (MD/TVD pairs) associated with this :class:`Horizon`.

        :return: :class:`~rogii_solo.base.ObjectRepository` containing :class:`HorizonPoint` instances.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            horizon = interpretation.horizons.find_by_name('Horizon1')

            # Get the Horizon points
            horizon_points = horizon.points
            print(horizon_points.to_dict())
        """
        if self._points is None:
            self._points = ObjectRepository(
                [
                    HorizonPoint(measure_units=self.interpretation.well.project.measure_unit, **point)
                    for point in self._get_points_data()
                ]
            )

        return self._points

    def to_dict(self) -> Dict:
        """
        Convert the :class:`Horizon` instance to a dictionary.

        :return: Dictionary representation of the :class:`Horizon`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            horizon = interpretation.horizons.find_by_name('Horizon1')

            # Get the Horizon data as a dictionary
            horizon_data = horizon.to_dict()
            print(horizon_data)
        """
        return {'uuid': self.uuid, 'name': self.name}

    def to_df(self) -> DataFrame:
        """
        Convert the :class:`Horizon` instance to a Pandas DataFrame.

        :return: DataFrame representation of the :class:`Horizon`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            horizon = interpretation.horizons.find_by_name('Horizon1')

            # Get the Horizon data as a Pandas DataFrame
            horizon_df = horizon.to_df()
            print(horizon_df)
        """
        return DataFrame([self.to_dict()])

    def _get_points_data(self) -> DataList:
        well_data = self.interpretation.well.to_dict(get_converted=False)
        trajectory_data = self.interpretation.well.trajectory.to_dict(get_converted=False)
        assembled_segments_data = self.interpretation.assembled_segments
        measure_units = self.interpretation.well.project.measure_unit

        calculated_trajectory = calculate_trajectory(
            well=well_data, raw_trajectory=trajectory_data, measure_units=measure_units
        )

        segments = get_segments(
            well=well_data,
            assembled_segments=assembled_segments_data['segments'],
            calculated_trajectory=calculated_trajectory,
            measure_units=measure_units,
        )

        segments_boundaries = get_segments_boundaries(
            assembled_segments=segments, calculated_trajectory=calculated_trajectory
        )

        return interpolate_horizon(
            segments_boundaries=segments_boundaries,
            horizon_uuid=self.uuid,
            horizon_tvd=assembled_segments_data['horizons'][self.uuid]['tvd'],
        )


class HorizonPoint(BaseObject):
    """
    Represent an individual point on a :class:`Horizon`, storing the measured depth (MD)
    and true vertical depth (TVD). These points are used to define a horizon's path along the
    :class:`~rogii_solo.well.Well`.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        interpretation = well.interpretations.find_by_name('Interpretation1')
        horizon = interpretation.horizons.find_by_name('Horizon1')

        # Get the first Horizon point
        horizon_point = horizon.points[0]
        print(horizon_point.to_dict())

        # Get measured depth (MD)
        point_md = horizon_point.md
        print(point_md)

        # Get true vertical depth (TVD)
        point_tvd = horizon_point.tvd
        print(point_tvd)
    """

    def __init__(self, measure_units: EMeasureUnits, md: float, tvd: float) -> None:
        self.measure_units = measure_units
        """The measurement units used for this :class:`HorizonPoint`"""

        self.md: float = md
        """The measured depth (MD) of the :class:`HorizonPoint`"""

        self.tvd: float = tvd
        """The true vertical depth (TVD) of the :class:`HorizonPoint`"""

    def to_dict(self, get_converted: bool = True) -> Dict:
        """
        Convert the :class:`HorizonPoint` instance to a dictionary, optionally
        converting MD and TVD values to the project's measurement units.

        :param get_converted: (Optional) Whether to convert the depth values using :meth:`convert_z`. Default is True.
        :return: Dictionary representation of the :class:`HorizonPoint`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            horizon = interpretation.horizons.find_by_name('Horizon1')

            # Get the first Horizon point
            horizon_point = horizon.points[0]
            print(horizon_point.to_dict())
        """
        return {
            'md': self.safe_round(self.convert_z(self.md, measure_units=self.measure_units))
            if get_converted
            else self.md,
            'tvd': self.safe_round(self.convert_z(self.tvd, measure_units=self.measure_units))
            if get_converted
            else self.tvd,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`HorizonPoint` instance to a Pandas DataFrame,
        optionally converting MD and TVD values to the project's measurement units.

        :param get_converted: (Optional) Whether to convert the depth values using :meth:`convert_z`. Default is True.
        :return: DataFrame representation of the :class:`HorizonPoint`.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            interpretation = well.interpretations.find_by_name('Interpretation1')
            horizon = interpretation.horizons.find_by_name('Horizon1')

            # Get the first Horizon point
            horizon_point = horizon.points[0]
            print(horizon_point.to_df())
        """
        return DataFrame([self.to_dict(get_converted)])
