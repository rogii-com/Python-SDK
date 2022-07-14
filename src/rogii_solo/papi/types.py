from typing import Any, Dict, Iterator, List, Literal, NamedTuple, TypedDict


class SettingsAuth(NamedTuple):
    client_id: str
    client_secret: str
    papi_domain_name: str


PapiVar = Dict[Literal['val'] | Literal['undefined'], Any]


class PapiTrajectoryPoint(TypedDict):
    md: PapiVar
    incl: PapiVar
    azim: PapiVar


PapiTrajectory = List[PapiTrajectoryPoint]

PapiData = Dict[str, Any]
PapiDataList = List[Dict[str, Any]]
PapiDataIterator = Iterator[Dict[str, Any]]
PapiAssembledSegments = Dict[Literal['segments'] | Literal['horizons'], Any]
