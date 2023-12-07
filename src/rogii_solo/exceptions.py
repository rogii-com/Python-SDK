from typing import Optional


class BaseRogiiSoloException(Exception):
    default_message = 'Error occurred.'

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.default_message

    def __str__(self):
        return str(self.message)


class ProjectNotFoundException(BaseRogiiSoloException):
    pass


class InvalidProjectException(BaseRogiiSoloException):
    pass


class TraceNotFoundException(BaseRogiiSoloException):
    pass


class InterpretationOutOfTrajectoryException(BaseRogiiSoloException):
    pass


class InvalidTopDataException(BaseRogiiSoloException):
    default_message = 'Measured depth value in project units must be in [0; 100000] range.'
