from typing import Any, Dict, Iterable, List, Set, Tuple

from pandas import DataFrame


def to_pandas_dataframe(row_list: list) -> DataFrame:
    return DataFrame(row_list)


def pd_to_dict(dataframe):
    if isinstance(dataframe, DataFrame):
        if not dataframe.empty and len(dataframe.index) == 1:
            return dataframe.loc[0].to_dict()

    return None


def is_data_dict(value):
    if isinstance(value, dict):
        # TODO: refine expression
        if len(value) == 1 and ('val' in value or 'undefined' in value):
            return True

    return False


def find_by_key(key, value, input_list):
    return next((item for item in input_list if item[key] == value), {})


def find_by_path(
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
            res = _find_by_path(
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


def _find_by_path(
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


def prepare_papi_var(value: float) -> dict:
    if value:
        return {'val': value}
    else:
        return {'undefined': True}
