from typing import Any, Dict, List, TypedDict

from pandas import DataFrame

DataList = List[Dict[str, Any]]


class Interpretation(TypedDict):
    meta: DataFrame
    horizons: DataFrame
    segments: DataFrame
    earth_models: DataFrame
