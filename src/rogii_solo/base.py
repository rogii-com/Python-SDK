from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, TypeVar

from pandas import DataFrame

from rogii_solo.calculations.constants import ROUNDING_PRECISION
from rogii_solo.calculations.converters import convert_value, radians_to_degrees
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList


class Convertible:
    """
    :class:`Convertible` is used to convert values of inherited objects by changing measure units.
    """

    @staticmethod
    def convert_xy(value: float, measure_units: EMeasureUnits, force_to_meters: bool = False) -> Optional[float]:
        """
        Convert an XY-coordinate value based on changes of XY coordinate measurement units.

        :param value: The XY-coordinate value to be converted.
        :param measure_units: The measurement units of XY coordinates.
        :param force_to_meters: If True, forces the conversion to meters regardless of the current units.

        :return: The converted XY coordinate value.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Get a well
            well = project.wells.find_by_name('Well1')

            # Convert Y coordinate to meters
            y_srf = well.y_srf
            y_srf_in_meters = well.convert_xy(value=y_srf, measure_units=project.measure_unit, force_to_meters=True)
            print(y_srf_in_meters)
        """
        if value is not None:
            return convert_value(value, measure_units=measure_units, force_to_meters=force_to_meters)

    @staticmethod
    def convert_z(value: float, measure_units: EMeasureUnits) -> Optional[float]:
        """
        Convert a given Z value based on the specified measurement units.

        :param value: The Z value to be converted.
        :param measure_units: The measurement units to use for the conversion.

        :return: The converted Z coordinate value, or None if the input value is None.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Get a well
            well = project.wells.find_by_name('Well1')

            # Convert kb based on measure unit
            kb = well.kb
            kb_converted = well.convert_z(value=kb, measure_units=project.measure_unit)
            print(kb_converted)
        """
        if value is not None:
            return convert_value(value=value, measure_units=measure_units)

    @staticmethod
    def convert_angle(value: float) -> Optional[float]:
        """
        Convert a given angle value from radians to degrees.

        :param value: The angle value in radians to be converted.

        :return: The converted angle value in degrees, or None if the input value is None.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Get a well
            well = project.wells.find_by_name('Well1')

            # Convert azimuth to degrees
            azimuth = well.azimuth
            azimuth_converted = well.convert_angle(value=azimuth)
            print(azimuth_converted)
        """
        if value is not None:
            return radians_to_degrees(value)

    @staticmethod
    def safe_round(value, precision: int = ROUNDING_PRECISION):
        """
        Safely rounds a given value to the specified number of decimal places.

        :param value: The value to be rounded.
        :param precision: The number of decimal places to round to.

        :return: The rounded value, or None if the input value is None.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Get a well
            well = project.wells.find_by_name('Well1')

            # Round kb
            kb_rounded = well.safe_round(value=well.kb, precision=2)
            print(kb_rounded)
        """
        if value is not None:
            return round(value, ndigits=precision) + 0  # Convert negative zero to positive


class BaseObject(ABC, Convertible):
    """
    Class with private and abstract methods.
    """

    @abstractmethod
    def to_dict(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Expected to convert object to dictionary
        """
        pass

    @abstractmethod
    def to_df(self, *args, **kwargs) -> DataFrame:
        """
        Expected to convert object to Pandas DataFrame
        """
        pass

    def _find_by_path(
        self,
        obj: Dict or Iterable[Dict],
        path: str or Iterable[str],
        default: Any = None,
        divider: str = None,
        check_none: bool = False,
        to_list: bool = False,
    ) -> Any:
        if not obj:
            return None if not to_list else []

        if not isinstance(obj, (List, Tuple, Set)):
            obj = [obj]

        if not isinstance(path, (List, Tuple, Set)):
            path = [path]

        result = [] if to_list else None
        for o in obj:
            for p in path:
                res = self.__find_by_path(
                    obj=o,
                    path=p,
                    default=default,
                    divider=divider,
                    check_none=check_none,
                    to_list=to_list,
                )
                if to_list:
                    result.extend(res)
                elif not to_list and res:
                    result = res
                    break

        return result

    def __find_by_path(
        self,
        obj: Dict,
        path: str,
        default: Any = None,
        divider: str = None,
        check_none: bool = False,
        to_list: bool = False,
    ) -> Any:
        if not obj:
            return None if not to_list else []

        for p in path.split(divider or '.'):
            if p not in obj or not obj[p]:
                return default if not to_list else []
            obj = obj[p]

        obj = obj if not check_none else default if obj is None else obj
        if not to_list:
            return obj

        return obj if isinstance(obj, list) else [obj] if obj else []


class ComplexObject(BaseObject):
    """
    Class with methods to convert inherited objects to Pandas DataFrame
    """

    def __init__(self, papi_client: PapiClient):
        super().__init__()

        self._papi_client = papi_client

    def to_dict(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Return empty dictionary
        """
        return {}

    def to_df(self, *args, **kwargs) -> DataFrame:
        """
        Return empty DataFrame
        """
        return DataFrame([self.to_dict(*args, **kwargs)])


T = TypeVar('T', bound=BaseObject)


class ObjectRepository(list[T]):
    """
    :class:`ObjectRepository` is used to detect objects by name and id. Moreover,
    it has methods to convert objects to Dictionary and Pandas DataFrame.
    It is inherited by all main objects in the documentation, which represent a group of geological objects.
    """

    def __init__(self, objects: List[T] = None):
        if objects is None:
            objects = []

        super().__init__(objects)

    def to_dict(self, *args, **kwargs) -> DataList:
        """
        Convert inherited object to the list of dictionaries

        :return: List of dictionaries

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Get a group of wells
            wells = project.wells

            # Convert wells to the list of dictionaries
            wells_to_dict = wells.to_dict()
            print(wells_to_dict)
        """
        return [object_.to_dict(*args, **kwargs) for object_ in self]

    def to_df(self, *args, **kwargs) -> DataFrame:
        """
        Convert inherited object to the Pandas DataFrame

        :return: Pandas DataFrame

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Get a group of wells
            wells = project.wells

            # Convert wells to the list of Pandas DataFrame
            wells_to_df = wells.to_df()
            print(wells_to_df)
        """
        return DataFrame(self.to_dict(*args, **kwargs))

    def find_by_id(self, value) -> Optional[T]:
        """
        Find an object by its unique identifier (UUID).

        :param value: The object UUID to search for.

        :return: The object with the matching UUID, or None if not found.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Get a group of wells
            wells = project.wells

            # Get a well by ID
            well = wells.find_by_id('WellID')
            print(well.to_dict())
        """
        return self._find_by_attr(attr='uuid', value=value)

    def find_by_name(self, value) -> Optional[T]:
        """
        Find an object by its name.

        :param value: The object name to search for.

        :return: The object with the matching name, or None if not found.

        :example:

        .. code-block:: python

            from rogii_solo import SoloClient

            client_id = ... # Input your client ID
            client_secret = ... # Input your client secret

            solo_client = SoloClient(client_id=client_id, client_secret=client_secret)
            project = solo_client.set_project_by_name('Project1')

            # Get a group of wells
            wells = project.wells

            # Get a well by name
            well = wells.find_by_name('Well1')
            print(well.to_dict())
        """
        return self._find_by_attr(attr='name', value=value)

    def _find_by_attr(self, attr: str, value) -> Optional[T]:
        return next((item for item in self if getattr(item, attr, None) == value), None)
