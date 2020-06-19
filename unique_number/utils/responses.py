from typing import Any, Optional, Union
import json
from datetime import datetime

from flask import Response
from werkzeug.datastructures import Headers

from unique_number.utils.date import to_api

def convert_json(o):
    if isinstance(o, datetime):
        return to_api(o)

def create_success(payload: Union[dict, list], status_code: Optional[int] =200) -> dict:
    data = {
        'payload': payload
    }
    return create_json_response(data, status_code)

def create_error(message: str, error_code: str, status_code: int) -> dict:
    data = {
        'error': {
            'code': error_code,
            'message': message
        }
    }
    return create_json_response(data, status_code)

def create_json_response(data: Any, status_code: int) -> Response:
    headers = Headers()
    headers.add('content-type', 'application/json')
    return Response(
            response=json.dumps(data, default=convert_json), 
            status=status_code,
            headers=headers)