class ServiceResponse:
    def __init__(self, success: bool, message: str, code: int = None, data: dict = None):
        self.success = success
        self.message = message
        self.code = code or (200 if success else 400)
        self.data = data or {}