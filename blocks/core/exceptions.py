

class SubjectAlreadyExists(Exception):
    pass

class SubjectNonExistent(Exception):
    pass

class LengthMismatch(Exception):
    pass

class BlockDataLengthMismatch(LengthMismatch):
    pass


