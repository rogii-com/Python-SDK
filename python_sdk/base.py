from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Set, Tuple

from pandas import DataFrame

from python_sdk.papi.client import PapiClient


class DataFrameable(ABC):
    @abstractmethod
    def to_df(self) -> DataFrame:
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        pass


class BaseObject:
    def __init__(self, papi_client: PapiClient):
        self._papi_client = papi_client

    def _find_by_key(self, input_list, key, value):
        return next((item for item in input_list if item.get(key, None) == value), {})

    def _find_by_attr(self, input_list, attr, value):
        return next((item for item in input_list if getattr(item, attr, None) == value), None)

    def pd_to_dict(self, data_frame):
        if isinstance(data_frame, DataFrame):
            if not data_frame.empty and len(data_frame.index) == 1:
                return data_frame.loc[0].to_dict()

        return None

    def _parse_papi_dict(self, obj: Any, default: Any = None) -> Any:
        """
        Recursive dictionary parsing. Its elements can be either of the regular type values,
        list/dictionary, or dictionaries with "val" or "undefined" key
        """
        if isinstance(obj, dict):
            if self._is_data_dict(obj):
                return obj.get('val', default)
            else:
                return {item: self._parse_papi_dict(value) for item, value in obj.items()}
        elif isinstance(obj, list):
            return [self._parse_papi_dict(item) for item in obj]
        else:
            return obj

    def _is_data_dict(self, value):
        if isinstance(value, dict):
            # TODO: refine expression
            if len(value) == 1 and ('val' in value or 'undefined' in value):
                return True

        return False

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

        for p in path.split(divider or "."):
            if p not in obj or not obj[p]:
                return default if not to_list else []
            obj = obj[p]

        obj = obj if not check_none else default if obj is None else obj
        if not to_list:
            return obj

        return obj if isinstance(obj, list) else [obj] if obj else []

    def _prepare_papi_var(self, value: float) -> dict:
        if value is None:
            return {'undefined': True}

        return {'val': value}

    def _request_all_pages(self, func, **kwargs):
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
        result = []
        offset = self._papi_client.DEFAULT_OFFSET
        last = False

        while not last:
            response = func(offset=offset, **kwargs)

            result.extend(response['content'])
            offset += self._papi_client.DEFAULT_LIMIT
            last = response['last']

        return result


class BaseObjectList(list):
    def __init__(self, dicts_list: list[dict], objects_list: list[object]):
        super().__init__(objects_list)

        self._dicts_list = dicts_list
        self._objects_list = objects_list

    def to_df(self) -> DataFrame:
        return DataFrame(self._dicts_list)

    def find_by_id(self, value):
        return self._find_by_attr(input_list=self, attr='uuid', value=value)

    def find_by_name(self, value):
        return self._find_by_attr(input_list=self, attr='name', value=value)

    def _find_by_attr(self, input_list: list[object], attr: str, value):
        return next((item for item in input_list if getattr(item, attr, None) == value), None)
