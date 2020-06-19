from datetime import datetime

API_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

def to_api(datetime_instance: datetime) -> str:
    return datetime_instance.strftime(API_DATETIME_FORMAT)