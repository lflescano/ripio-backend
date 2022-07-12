class ExceptionError(Exception):
    def __init__(self, key, message):
        super().__init__(message)
        self.key = key
        self.message = message
