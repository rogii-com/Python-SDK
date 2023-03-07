class BaseRogiiSoloException(Exception):
    pass


class ProjectNotFoundException(BaseRogiiSoloException):
    pass


class InvalidProjectException(BaseRogiiSoloException):
    pass


class TraceNotFoundException(BaseRogiiSoloException):
    pass


class InterpretationOutOfTrajectoryException(BaseRogiiSoloException):
    pass
