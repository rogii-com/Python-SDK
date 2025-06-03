from typing import Any, Dict, Optional

from pandas import DataFrame

from rogii_solo.base import BaseObject


class TargetLine(BaseObject):
    """
    Represent a :class:`TargetLine` object of the :class:`~rogii_solo.well.Well`, containing
    the start and end points of the line that represent a planned trajectory.

    :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ...  # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')

            # Get a TargetLine in the Well
            target_line = well.target_lines.find_by_name('TargetLine1')

            # Get a unique ID of the TargetLine
            target_line_uuid = target_line.uuid
            print(target_line_uuid)
    """

    def __init__(self, **kwargs):
        self.uuid: Optional[str] = None
        """Unique identifier of the :class:`TargetLine`."""

        self.name: Optional[str] = None
        """Name of the :class:`TargetLine`."""

        self.azimuth: Optional[float] = None
        """Azimuth of the :class:`TargetLine` in degrees."""

        self.delta_tvd: Optional[float] = None
        """Vertical distance (TVD) between origin and target points."""

        self.delta_vs: Optional[float] = None
        """Vertical section (VS) distance between origin and target points."""

        self.inclination: Optional[float] = None
        """Inclination angle of the :class:`TargetLine` in degrees."""

        self.length: Optional[float] = None
        """Length of the :class:`TargetLine` in 3D space."""

        self.origin_base_corridor_tvd: Optional[float] = None
        """Base corridor TVD at the origin point."""

        self.origin_md: Optional[float] = None
        """Measured depth at which this :class:`TargetLine` is located."""

        self.origin_top_corridor_tvd: Optional[float] = None
        """Top corridor TVD at the origin point."""

        self.origin_tvd: Optional[float] = None
        """True vertical depth (TVD) at the origin point."""

        self.origin_vs: Optional[float] = None
        """Vertical section (VS) at the origin point."""

        self.origin_x: Optional[float] = None
        """X coordinate at the origin point."""

        self.origin_y: Optional[float] = None
        """Y coordinate at the origin point."""

        self.origin_z: Optional[float] = None
        """Z coordinate (TVDSS) at the origin point."""

        self.target_base_corridor_tvd: Optional[float] = None
        """Base corridor TVD at the target point."""

        self.target_md: Optional[float] = None
        """Measured depth (MD) at which the target point is located."""

        self.target_top_corridor_tvd: Optional[float] = None
        """Top corridor TVD at the target point."""

        self.target_tvd: Optional[float] = None
        """True vertical depth (TVD) at the target point."""

        self.target_vs: Optional[float] = None
        """Vertical section (VS) at the target point."""

        self.target_x: Optional[float] = None
        """X coordinate at the target point."""

        self.target_y: Optional[float] = None
        """Y coordinate at the target point."""

        self.target_z: Optional[float] = None
        """Z coordinate (TVDSS) at the target point."""

        self.tvd_vs: Optional[float] = None
        """Ratio of TVD to VS (used for trajectory steepness analysis)."""

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert the :class:`TargetLine` instance to a dictionary.

        :param get_converted: (Optional) Whether to apply `safe_round` to numeric values. Default = True.
        :return: Dictionary representation of the target line.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ...  # Input your client ID
            client_secret = ...  # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            target_line = well.target_lines.find_by_name('Targetline1')

            # Convert the TargetLine to a dictionary
            target_line_dict = target_line.to_dict()
            print(target_line_dict)
        """
        return {
            'uuid': self.uuid,
            'name': self.name,
            'azimuth': self.safe_round(self.azimuth) if get_converted else self.azimuth,
            'delta_tvd': self.safe_round(self.delta_tvd) if get_converted else self.delta_tvd,
            'delta_vs': self.safe_round(self.delta_vs) if get_converted else self.delta_vs,
            'inclination': self.safe_round(self.inclination) if get_converted else self.inclination,
            'length': self.safe_round(self.length) if get_converted else self.length,
            'origin_base_corridor_tvd': self.safe_round(self.origin_base_corridor_tvd)
            if get_converted
            else self.origin_base_corridor_tvd,
            'origin_md': self.safe_round(self.origin_md) if get_converted else self.origin_md,
            'origin_top_corridor_tvd': self.safe_round(self.origin_top_corridor_tvd)
            if get_converted
            else self.origin_top_corridor_tvd,
            'origin_tvd': self.safe_round(self.origin_tvd) if get_converted else self.origin_tvd,
            'origin_vs': self.safe_round(self.origin_vs) if get_converted else self.origin_vs,
            'origin_x': self.safe_round(self.origin_x) if get_converted else self.origin_x,
            'origin_y': self.safe_round(self.origin_y) if get_converted else self.origin_y,
            'origin_z': self.safe_round(self.origin_z) if get_converted else self.origin_z,
            'target_base_corridor_tvd': self.safe_round(self.target_base_corridor_tvd)
            if get_converted
            else self.target_base_corridor_tvd,
            'target_md': self.safe_round(self.target_md) if get_converted else self.target_md,
            'target_top_corridor_tvd': self.safe_round(self.target_top_corridor_tvd)
            if get_converted
            else self.target_top_corridor_tvd,
            'target_tvd': self.safe_round(self.target_tvd) if get_converted else self.target_tvd,
            'target_vs': self.safe_round(self.target_vs) if get_converted else self.target_vs,
            'target_x': self.safe_round(self.target_x) if get_converted else self.target_x,
            'target_y': self.safe_round(self.target_y) if get_converted else self.target_y,
            'target_z': self.safe_round(self.target_z) if get_converted else self.target_z,
            'tvd_vs': self.safe_round(self.tvd_vs) if get_converted else self.tvd_vs,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`TargetLine` to a dictionary with Pandas DataFrames.

        :param get_converted: (Optional) Whether to apply `safe_round` to numeric values. Default = True
        :return: A dictionary of DataFrames, containing :class:`TargetLine` metadata.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            target_line = well.target_lines.find_by_name('Targetline1')

            # Convert the TargetLine to a DataFrame
            target_line_df = target_line.to_df()
            print(target_line_df)
        """
        return DataFrame([self.to_dict(get_converted)])
