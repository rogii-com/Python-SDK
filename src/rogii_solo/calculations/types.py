from typing import Any, Dict, List, Optional, TypedDict


class RawTrajectoryPoint(TypedDict):
    """
    A TypedDict representing a :class:`RawTrajectoryPoint` with basic directional measurements.
    """

    md: float
    """Measured depth of the trajectory point."""

    incl: float
    """Inclination angle at the trajectory point."""

    azim: float
    """Azimuth angle at the trajectory point."""


RawTrajectory = List[RawTrajectoryPoint]


class TrajectoryPoint(TypedDict):
    """
    A TypedDict representing a :class:`TrajectoryPoint` with calculated spatial coordinates and additional metrics.
    """

    md: float
    """Measured depth of the trajectory point."""

    incl: float
    """Inclination angle at the trajectory point."""

    azim: float
    """Azimuth angle at the trajectory point."""

    tvd: float
    """True vertical depth at the trajectory point."""

    ns: float
    """North-South coordinate of the trajectory point."""

    ew: float
    """East-West coordinate of the trajectory point."""

    x: float
    """X coordinate in the project's coordinate system."""

    y: float
    """Y coordinate in the project's coordinate system."""

    tvdss: float
    """True vertical depth subsea at the trajectory point."""

    vs: float
    """Vertical section at the trajectory point."""

    dls: float
    """Dogleg severity at the trajectory point."""

    dog_leg: float
    """Dogleg angle at the trajectory point."""


Trajectory = List[TrajectoryPoint]


class AssembledHorizon(TypedDict):
    """
    A TypedDict representing a :class:`~rogii_solo.horizon.Horizon` assembled from
    :class:`~rogii_solo.interpretation.Interpretation`.
    """

    uuid: str
    """Unique identifier of the :class:`~rogii_solo.horizon.Horizon`."""

    tvd: float
    """True vertical depth of the :class:`~rogii_solo.horizon.Horizon`."""


class HorizonShift(TypedDict):
    """
    A TypedDict representing a shift applied to a horizon.
    """

    uuid: str
    """Unique identifier of the horizon being shifted."""

    start: float
    """Starting value of the shift."""

    end: float
    """Ending value of the shift."""


class Segment(TypedDict):
    """
    A TypedDict representing a segment of the well path with associated horizon shifts.
    """

    uuid: Optional[str]
    """Unique identifier of the segment."""

    md: float
    """Measured depth at the segment."""

    vs: Optional[float]
    """Vertical section at the segment."""

    start: Optional[float]
    """Starting value of the segment."""

    end: Optional[float]
    """Ending value of the segment."""

    x: float
    """X coordinate in the project's coordinate system."""

    y: float
    """Y coordinate in the project's coordinate system."""

    horizon_shifts: Dict[str, HorizonShift]
    """Dictionary mapping horizon UUIDs to their shifts in this segment."""

    boundary_type: int
    """Type identifier for the segment boundary."""


class SegmentWithDip(Segment):
    """
    A TypedDict extending segment with dip angle information.
    """

    dip: Optional[float]
    """Dip angle of the segment."""


AssembledHorizons = Dict[str, AssembledHorizon]


class AssembledSegments(TypedDict):
    """
    A TypedDict representing a collection of assembled segments and corresponding horizons.
    """

    horizons: AssembledHorizons
    """Dictionary of assembled horizons indexed by their UUIDs."""

    segments: List[Segment]
    """List of segments in the assembly."""


class SegmentBoundaries(TypedDict):
    """
    A TypedDict representing the boundary points of a segment.
    """

    md: float
    """Measured depth at the boundary."""

    left_point: Optional[Dict[str, Any]]
    """Optional dictionary containing data for the left boundary point."""

    right_point: Optional[Dict[str, Any]]
    """Optional dictionary containing data for the right boundary point."""

    interpolated_point: Dict[str, Any]
    """Dictionary containing data for the interpolated boundary point."""


SegmentsBoundaries = List[SegmentBoundaries]
