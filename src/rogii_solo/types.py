from typing import Any, Dict, List, TypedDict

from pandas import DataFrame

DataList = List[Dict[str, Any]]


class Interpretation(TypedDict):
    """
    A TypedDict representing the types of an :class:`~rogii_solo.interpretation.Interpretation`
    structure by the use of :class:`DataFrame`.
    """

    meta: DataFrame
    """Metadata information about the :class:`~rogii_solo.interpretation.Interpretation`."""

    horizons: DataFrame
    """Horizon data associated with the :class:`~rogii_solo.interpretation.Interpretation`."""

    segments: DataFrame
    """Segment information for the :class:`~rogii_solo.interpretation.Interpretation`."""

    earth_models: DataFrame
    """Earth model data used in the :class:`~rogii_solo.interpretation.Interpretation`."""
