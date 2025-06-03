from typing import Any, Dict, Iterator, List, Literal, NamedTuple, TypedDict

Scheme = Literal['http', 'https']
TraceType = Literal['DEPTH', 'TIME', 'CALC']


class ProxyData(TypedDict):
    """
    A TypedDict representing proxy configuration data for API connections.
    """

    Scheme: str
    """Protocol scheme for the proxy connection."""


class SettingsAuth(NamedTuple):
    """
    A NamedTuple containing authentication and connection settings for the PAPI client.
    """

    client_id: str
    """Client identifier for API authentication."""

    client_secret: str
    """Client secret for API authentication."""

    papi_domain_name: str
    """Domain name of the PAPI server."""

    proxies: ProxyData
    """Proxy configuration for API connections."""


PapiVar = Dict[Literal['val'] | Literal['undefined'], Any]


class PapiTrajectoryPoint(TypedDict):
    """
    A TypedDict representing a trajectory point in the PAPI format.
    """

    md: PapiVar
    """Measured depth."""

    incl: PapiVar
    """Inclination angle."""

    azim: PapiVar
    """Azimuth angle."""


class PapiStarredHorizons(TypedDict):
    """
    A TypedDict representing the starred horizons in a PAPI object.
    """

    top: str
    """The top starred horizon."""

    center: str
    """The center starred horizon."""

    bottom: str
    """The bottom starred horizon."""


class PapiStarredTops(TypedDict):
    """
    A TypedDict representing the starred tops in a PAPI object.
    """

    top: str
    """The top starred top."""

    center: str
    """The center starred top."""

    bottom: str
    """The bottom starred top."""


class PapiLogPoint(TypedDict):
    """
    A TypedDict representing a log data point in the PAPI format.
    """

    index: PapiVar
    """Index value of the log point."""

    value: PapiVar
    """Measured value at the log point."""


class PapiObjectCreationResult(TypedDict):
    """
    A TypedDict representing the result of creating a new object in the PAPI system.
    """

    uuid: str
    """UUID of the newly created object."""


PapiTrajectory = List[PapiTrajectoryPoint]
PapiData = Dict[str, Any]
PapiDataList = List[Dict[str, Any]]
PapiDataIterator = Iterator[Dict[str, Any]]
PapiAssembledSegments = Dict[Literal['segments'] | Literal['horizons'], Any]
