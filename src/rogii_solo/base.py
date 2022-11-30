from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, TypeVar

from pandas import DataFrame

from rogii_solo.calculations.converters import convert_value, radians_to_degrees
from rogii_solo.calculations.enums import EMeasureUnits
from rogii_solo.papi.client import PapiClient
from rogii_solo.types import DataList


class Convertable:
    @staticmethod
    def convert_xy(value: float, measure_units: EMeasureUnits, force_to_meters: bool = False) -> Optional[float]:
        if value is not None:
            return convert_value(value, measure_units=measure_units, force_to_meters=force_to_meters)

    @staticmethod
    def convert_z(value: float, measure_units: EMeasureUnits) -> Optional[float]:
        if value is not None:
            return convert_value(value=value, measure_units=measure_units)

    @staticmethod
    def convert_angle(value: float) -> Optional[float]:
        if value is not None:
            return radians_to_degrees(value)


class BaseObject(ABC, Convertable):
    """
    Base data object
    """

    @abstractmethod
    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        """
        Convert object to dict
        :return
        """
        pass

    @abstractmethod
    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert object to DataFrame
        :return
        """
        pass

    def _find_by_path(self,
                      obj: Dict or Iterable[Dict],
                      path: str or Iterable[str],
                      default: Any = None,
                      divider: str = None,
                      check_none: bool = False,
                      to_list: bool = False,
                      ) -> Any:
        """
        Find nested key value in dict
        :param obj:
        :param path:
        :param default:
        :param divider:
        :param check_none:
        :param to_list:
        :return:
        """
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

    def __find_by_path(self,
                       obj: Dict,
                       path: str,
                       default: Any = None,
                       divider: str = None,
                       check_none: bool = False,
                       to_list: bool = False,
                       ) -> Any:
        if not obj:
            return None if not to_list else []

        for p in path.split(divider or "."):
            if p not in obj or not obj[p]:
                return default if not to_list else []
            obj = obj[p]

        obj = obj if not check_none else default if obj is None else obj
        if not to_list:
            return obj

        return obj if isinstance(obj, list) else [obj] if obj else []


class ComplexObject(BaseObject):
    """
    Object with access to PAPI
    """
    def __init__(self, papi_client: PapiClient):
        super().__init__()

        self._papi_client = papi_client

    def to_dict(self, get_converted: bool = True) -> Dict[str, Any]:
        return {}

    def to_df(self, get_converted: bool = True) -> DataFrame:
        return DataFrame([self.to_dict(get_converted)])


T = TypeVar('T', bound=BaseObject)


class ObjectRepository(list[T]):
    """
    List of objects with utility methods
    """
    def __init__(self, objects: List[T] = None):
        if objects is None:
            objects = []

        super().__init__(objects)

    def to_dict(self, get_converted: bool = True) -> DataList:
        """
        Return list of dicts
        :return:
        """
        return [object_.to_dict(get_converted) for object_ in self]

    def to_df(self, get_converted: bool = True) -> DataFrame:
        """
        Convert list to Pandas DataFrame
        :return:
        """
        return DataFrame(self.to_dict(get_converted))

    def find_by_id(self, value) -> Optional[T]:
        """
        Find object by ID
        :param value:
        :return:
        """
        return self._find_by_attr(attr='uuid', value=value)

    def find_by_name(self, value) -> Optional[T]:
        """
        Find object by name
        :param value:
        :return:
        """
        return self._find_by_attr(attr='name', value=value)

    def _find_by_attr(self, attr: str, value) -> Optional[T]:
        return next((item for item in self if getattr(item, attr, None) == value), None)
