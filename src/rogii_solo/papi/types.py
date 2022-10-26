from typing import Any, Dict, Iterator, List, Literal, NamedTuple, TypedDict


class ProxyData(TypedDict):
    scheme: Literal['http'] | Literal['https']
    netloc: str


class ProxyNetloc(TypedDict):
    host: str
    port: int


UserProxyData = Dict[Literal['http'] | Literal['https'], ProxyNetloc]


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


PapiTrajectory = List[PapiTrajectoryPoint]

PapiData = Dict[str, Any]
PapiDataList = List[Dict[str, Any]]
PapiDataIterator = Iterator[Dict[str, Any]]
PapiAssembledSegments = Dict[Literal['segments'] | Literal['horizons'], Any]
