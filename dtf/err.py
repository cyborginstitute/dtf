class DtfException(Exception)
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        if self.msg is None:
            return "dtf Error: Unspecified"
        else:
            return "dtf Error: " + self.msg

class DtfNotImplemented(DtfException):
    pass

class DtfDiscoveryException(DtfException):
    pass

class DtfTestException(DtfException):
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        if self.msg is None:
            return "Test failure in 'fatal' mode: No message."
        else:
            return "Test failure in 'fatal' mode: " + self.msg
