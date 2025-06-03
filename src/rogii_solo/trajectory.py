from typing import Any, Dict, List, Optional

from pandas import DataFrame

from rogii_solo.base import BaseObject
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.types import DataList


class TrajectoryPoint(BaseObject):
    """
    Represent a single point in a :class:`TrajectoryPointRepository`, containing measurement depth (MD),
    inclination (INCL), and azimuth (AZIM) values.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')
        trajectory = well.trajectory

        # Get the trajectory point measure units
        measure_unit = trajectory[0].measure_units
        print(measure_unit)

        # Get the Trajectory point measure depth
        point_md = trajectory[0].md
        print(measure_unit)

        # Get the Trajectory point inclination
        point_incl = trajectory[0].incl
        print(point_incl)

        # Get the Trajectory point azimuth
        point_azim = trajectory[0].azim
        print(point_azim)
    """

    def __init__(self, measure_units: EMeasureUnits, **kwargs):
        self.measure_units: str = measure_units
        """The measurement units used for this trajectory point"""

        self.md: Optional[float] = None
        """Measured depth at this point."""

        self.incl: Optional[float] = None
        """Inclination angle at this point."""

        self.azim: Optional[float] = None
        """Azimuth angle at this point."""

        self.__dict__.update(kwargs)

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert the :class:`TrajectoryPoint` to a Dictionary.

        :param get_converted: (Optional) Whether to convert values to project units. Default = True.
        :return: Dictionary representation of the :class:`TrajectoryPoint`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            trajectory_point = well.trajectory[0]

            # Convert the trajectory point to a dictionary
            trajectory_point_dict = trajectory_point.to_dict()
            print(trajectory_point_dict)
        """
        return {
            'md': self.safe_round(self.convert_z(self.md, measure_units=self.measure_units))
            if get_converted
            else self.md,
            'incl': self.safe_round(self.convert_angle(self.incl)) if get_converted else self.incl,
            'azim': self.safe_round(self.convert_angle(self.azim)) if get_converted else self.azim,
        }

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert the :class:`TrajectoryPoint` to a Pandas DataFrame.

        :param get_converted: Whether to convert values to the specified measurement units
        :return: DataFrame representation of the :class:`TrajectoryPoint`

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            trajectory_point = well.trajectory[0]

            # Convert the trajectory point to a DataFrame
            trajectory_point_df = trajectory_point.to_df()
            print(trajectory_point_df)
        """
        return DataFrame([self.to_dict(get_converted)])


class TrajectoryPointRepository(list):
    """
    Repository for managing collections of :class:`TrajectoryPoint` objects.

    :example:

    .. code-block:: python

        from rogii_solo import SoloClient

        client_id = ... # Input your client ID
        client_secret = ... # Input your client secret

        solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
        project = solo_client.set_project_by_name('Project1')
        well = project.wells.find_by_name('Well1')

        # Get the Trajectory object
        trajectory = well.trajectory
        print(trajectory.to_dict())
    """

    def __init__(self, objects: List[TrajectoryPoint] = None):
        if objects is None:
            objects = []

        super().__init__(objects)

    def to_dict(self, get_converted: bool = True) -> DataList:
        """
        Convert all TrajectoryPoints in the repository to a list of dictionaries.

        :param get_converted: Whether to convert values to the specified measurement units
        :return: List of dictionaries representing the trajectory points

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            trajectory = well.trajectory

            # Convert the trajectory to a dictionary without unit conversation
            trajectory_dict = trajectory.to_dict(get_converted=False)
            print(trajectory_dict)

            # Convert the trajectory to a dictionary with unit conversation
            trajectory_dict = trajectory.to_dict()
            print(trajectory_dict)
        """
        return [object_.to_dict(get_converted) for object_ in self]

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert all TrajectoryPoints in the repository to Pandas DataFrame.

        :param get_converted: Whether to convert values to the specified measurement units
        :return: Pandas DataFrame representation of the trajectory points

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')
            well = project.wells.find_by_name('Well1')
            trajectory = well.trajectory

            # Convert the trajectory to a DataFrame without unit conversation
            trajectory_df = trajectory.to_df(get_converted=False)
            print(trajectory_df)

            # Convert the trajectory to a DataFrame with unit conversation
            trajectory_df = trajectory.to_df()
            print(trajectory_df)
        """
        return DataFrame(self.to_dict(get_converted))
