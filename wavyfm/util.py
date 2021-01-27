from datetime import datetime

__all__ = ["ENV_VARS", "API_BASE_DEFAULT", "API_BASE_V1"]

"""The v1 API base URL"""
API_BASE_V1 = "https://wavy.fm/api/v1beta"

"""The default API base URL"""
API_BASE_DEFAULT = API_BASE_V1

"""Environment variable names"""
ENV_VARS = {
    "client_id": "WAVYFM_CLIENT_ID",
    "client_secret": "WAVYFM_CLIENT_SECRET",
}


def datetime_from_string(raw_date: str) -> datetime:
    """
    Creates a UTC DateTime object from a RFC3339 formatted string.
    """
    return datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%S.%f%z')
