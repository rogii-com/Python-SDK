from typing import Any, Dict, List, TypedDict

from pandas import DataFrame

DataList = List[Dict[str, Any]]


class Interpretation(TypedDict):
    meta: DataFrame
    horizons: DataFrame
    segments: DataFrame


class Horizon(TypedDict):
    meta: DataFrame
    points: DataFrame


class Log(TypedDict):
    meta: DataFrame
    points: DataFrame
