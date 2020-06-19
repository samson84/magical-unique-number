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

class RoundAlreadyFinished(ApplicationError):
    def __init__(self):
        super().__init__(
            message = f'The round is already finished.',
            error_code = 'already_finished',
            status_code=409
        )

class ValidationError(ApplicationError):
    def __init__(self, validation_error):
        super().__init__(
            message = f'Invalid input: {validation_error}',
            status_code=400,
            error_code='invalid_input'
        )

class InvalidVote(ApplicationError):
    def __init__(self, message):
        super().__init__(
            message = f'Invalid vote: {message}',
            status_code=409,
            error_code='invalid_vote'
        )

class RoundStillActive(ApplicationError):
    def __init__(self, message):
        super().__init__(
            message = f'The Round is s till active.',
            status_code=409,
            error_code='not_finished'
        )
