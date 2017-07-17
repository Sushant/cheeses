class CheesesException(BaseException):
    pass

class TwoPhaseSetException(CheesesException):
    pass

class LWWSetException(CheesesException):
    pass

class ORSetException(CheesesException):
    pass