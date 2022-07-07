from typing import TypedDict

from pandas import DataFrame


class Interpretation(TypedDict):
    meta: DataFrame
    horizons: DataFrame
    segments: DataFrame
