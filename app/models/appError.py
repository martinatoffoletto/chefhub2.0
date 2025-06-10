
class AppError(Exception):
    def __init__(self, code: str, message):
        self.code = code
        self.message = message 
        super().__init__(self.message)
