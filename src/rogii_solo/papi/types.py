from typing import Any, Dict, Iterator, List, Literal, NamedTuple, TypedDict

Scheme = Literal['http', 'https']
TraceType = Literal['DEPTH', 'TIME']


class ProxyData(TypedDict):
    Scheme: str


class SettingsAuth(NamedTuple):
    client_id: str
    client_secret: str
    papi_domain_name: str
    proxies: ProxyData


PapiVar = Dict[Literal['val'] | Literal['undefined'], Any]


class PapiTrajectoryPoint(TypedDict):
    md: PapiVar
    incl: PapiVar
    azim: PapiVar


class PapiStarredHorizons(TypedDict):
    top: str
    center: str
    bottom: str


class PapiStarredTops(TypedDict):
    top: str
    center: str
    bottom: str


class PapiLogPoint(TypedDict):
    index: PapiVar
    value: PapiVar


PapiTrajectory = List[PapiTrajectoryPoint]

PapiData = Dict[str, Any]
PapiDataList = List[Dict[str, Any]]
PapiDataIterator = Iterator[Dict[str, Any]]
PapiAssembledSegments = Dict[Literal['segments'] | Literal['horizons'], Any]
