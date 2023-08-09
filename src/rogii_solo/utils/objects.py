from datetime import datetime
from typing import Dict, List, Optional


def find_by_uuid(value, input_list: List[Dict]) -> Optional[Dict]:
    return find_by_key('uuid', value, input_list)


def find_by_key(key, value, input_list: List[Dict]) -> Optional[Dict]:
    return next((item for item in input_list if item[key] == value), None)


def get_datetime(datetime_str: str):
    return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
