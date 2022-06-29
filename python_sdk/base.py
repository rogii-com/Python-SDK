from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Literal, Optional, Set, Tuple

from pandas import DataFrame

from python_sdk.papi.client import PapiClient


class DataFrameable(ABC):
    """
    Object that can be converted to Pandas DataFrame
    """
    @abstractmethod
    def to_df(self) -> DataFrame:
        """
        Convert object to DataFrame
        :return
        """
        pass


class BaseObject(ABC):
    """
    Base data object
    """
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert object to dict
        :return
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

    def to_dict(self) -> Dict[str, Any]:
        return {}

    def _prepare_papi_var(self, value: float) -> Dict[Literal['val'] | Literal['undefined'], Any]:
        """
        Create value dict for PAPI
        :param value:
        :return:
        """
        if value is None:
            return {'undefined': True}

        return {'val': value}

    def _parse_papi_data(self, data: Any, default: Any = None) -> Any:
        """
        Recursive dictionary parsing.
        Elements can be either of the regular type values, list/dict, or dicts with "val" or "undefined" key.
        """
        if isinstance(data, dict):
            if 'val' in data or 'undefined' in data:
                return data.get('val', default)
            else:
                return {item: self._parse_papi_data(value) for item, value in data.items()}
        elif isinstance(data, list):
            return [self._parse_papi_data(item) for item in data]
        else:
            return data

    def _request_all_pages(self, func, **kwargs):
        """
        Retrieve PAPI data using methods which returns content right away
        :param func:
        :param kwargs:
        :return:
        """
        result = []
        offset = self._papi_client.DEFAULT_OFFSET

        while True:
            response = func(offset=offset, **kwargs)

            if not len(response):
                break

            result.extend(response)
            offset += self._papi_client.DEFAULT_LIMIT

        return result

    def _request_all_pages_with_content(self, func, **kwargs):
        """
        Retrieve PAPI data using methods which returns entire response
        :param func:
        :param kwargs:
        :return:
        """
        result = []
        offset = self._papi_client.DEFAULT_OFFSET
        last = False

        while not last:
            response = func(offset=offset, **kwargs)

            result.extend(response['content'])
            offset += self._papi_client.DEFAULT_LIMIT
            last = response['last']

        return result


class ObjectRepository(list):
    """
    List of objects with utility methods
    """
    def __init__(self, dicts: List[Dict], objects: List[BaseObject]):
        super().__init__(objects)

        self._dicts = dicts
        self._objects = objects

    def to_df(self) -> DataFrame:
        """
        Convert list to Pandas DataFrame
        :return:
        """
        return DataFrame(self._dicts)

    def to_dict(self) -> List[Dict]:
        """
        Return list of dicts
        :return:
        """
        return self._dicts

    def find_by_id(self, value) -> Optional[BaseObject]:
        """
        Find object by ID
        :param value:
        :return:
        """
        return self._find_by_attr(attr='uuid', value=value)

    def find_by_name(self, value) -> Optional[BaseObject]:
        """
        Find object by name
        :param value:
        :return:
        """
        return self._find_by_attr(attr='name', value=value)

    def _find_by_attr(self, attr: str, value) -> Optional[BaseObject]:
        return next((item for item in self if getattr(item, attr, None) == value), None)
