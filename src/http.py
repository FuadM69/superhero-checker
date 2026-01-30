import requests

from .constants import REQUEST_TIMEOUT_SECONDS

_session = requests.Session()
_session.trust_env = False


def get(url: str):
    return _session.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
