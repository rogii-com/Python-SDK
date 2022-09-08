from typing import Any, Dict, List, Optional, TypedDict


class RawTrajectoryPoint(TypedDict):
    md: float
    incl: float
    azim: float


RawTrajectory = List[RawTrajectoryPoint]


class TrajectoryPoint(TypedDict):
    md: float
    incl: float
    azim: float
    tvd: float
    ns: float
    ew: float
    x: float
    y: float
    tvdss: float
    vs: float
    dls: float
    dog_leg: float


Trajectory = List[TrajectoryPoint]


class AssembledHorizon(TypedDict):
    uuid: str
    tvd: float


class HorizonShift(TypedDict):
    uuid: str
    start: float
    end: float


class Segment(TypedDict):
    md: float
    vs: float
    start: Optional[float]
    end: Optional[float]
    horizon_shifts: Dict[str, HorizonShift]


class SegmentWithDip(Segment):
    dip: Optional[float]


AssembledHorizons = Dict[str, AssembledHorizon]


class AssembledSegments(TypedDict):
    horizons: AssembledHorizons
    segments: List[Segment]


class SegmentBoundaries(TypedDict):
    md: float
    left_point: Optional[Dict[str, Any]]
    right_point: Optional[Dict[str, Any]]
    interpolated_point: Dict[str, Any]


SegmentsBoundaries = List[SegmentBoundaries]
