from typing import Optional

class ApplicationError(Exception):
    def __init__(self, message: str, error_code: str, status_code: int):
        super().__init__(f'[{error_code}][{status_code}] Application Error: {message}')
        self.message = message
        self.error_code = error_code
        self.status_code = status_code


class NotFound(ApplicationError):
    def __init__(self, what: Optional[str] = 'Resource'):
        super().__init__(
            message = f'{what} is not found.',
            error_code = 'not_found',
            status_code=404
        )
