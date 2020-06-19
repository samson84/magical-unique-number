from functools import wraps
from typing import NoReturn, Union
from flask import request
import traceback

from jsonschema import validate, exceptions

from unique_number.utils import errors

def validate_json(schema: dict) -> Union[NoReturn, None]:
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.json
            if data is None:
                raise errors.ValidationError('Invalid JSON given or the content-type header is not correct!')
            try:
                validate(instance=data, schema=schema)
            except exceptions.ValidationError as error:
                traceback.print_exc()
                raise errors.ValidationError(str(error)) from error
            return func(*args, **kwargs)
        return wrapper
    return decorator
            