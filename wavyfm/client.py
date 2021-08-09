import logging

__all__ = ["WavyClient", "WavyException"]

import json
import requests
from requests.packages import urllib3

from wavyfm.error import WavyException
from wavyfm.metrics import _WavyMetricsEndpoints
from wavyfm.users import _WavyUsersEndpoints
from wavyfm.util import API_BASE_DEFAULT
from wavyfm.auth import _WavyAuthBase

logger = logging.getLogger(__name__)


class WavyClient(object):
    default_retry_codes = (429, 500, 502, 503, 504)

    def __init__(self,
                 requests_session=True,
                 auth: str = None,
                 auth_manager: _WavyAuthBase = None,
                 proxies=None,
                 requests_timeout=30,
                 status_forcelist=None,
                 retries=3,
                 status_retries=3,
                 backoff_factor=0.3):
        self._auth = auth
        self.auth_manager = auth_manager
        self.proxies = proxies
        self.requests_timeout = requests_timeout
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist or self.default_retry_codes
        self.status_retries = status_retries

        if isinstance(requests_session, requests.Session):
            self._session = requests_session
        elif requests_session:  # Build a new session if it's a truthy value.
            self._session = requests.Session()
        else:  # Use the Requests API module as a "session".
            from requests import api
            self._session = api

        self._metrics = _WavyMetricsEndpoints(self)
        self._users = _WavyUsersEndpoints(self)

    @property
    def metrics(self) -> _WavyMetricsEndpoints:
        return self._metrics

    @property
    def users(self) -> _WavyUsersEndpoints:
        return self._users

    def _build_session(self):
        self._session = requests.Session()
        retry = urllib3.Retry(
            total=self.retries,
            connect=None,
            read=False,
            method_whitelist=frozenset(['GET', 'POST', 'PUT', 'DELETE']),
            status=self.status_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist)

        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)

    def _auth_headers(self):
        if self._auth:
            return {"Authorization": f"Bearer {self._auth}"}
        if not self.auth_manager:
            return {}
        token = self.auth_manager.get_access_token()
        return {"Authorization": f"Bearer {token}"}

    def _internal_call(self, method: str, url: str, payload, params):
        args = dict(params=params)
        if not url.startswith("http"):
            url = API_BASE_DEFAULT + url
        headers = self._auth_headers()

        if "content_type" in args["params"]:
            headers["Content-Type"] = args["params"]["content_type"]
            del args["params"]["content_type"]
            if payload:
                args["data"] = payload
        else:
            headers["Content-Type"] = "application/json"
            if payload:
                args["data"] = json.dumps(payload)

        logger.debug('Sending %s to %s with Params: %s Headers: %s and Body: %r ',
                     method, url, args.get("params"), headers, args.get('data'))

        try:
            response = self._session.request(
                method, url, headers=headers, proxies=self.proxies,
                timeout=self.requests_timeout, **args
            )

            response.raise_for_status()
            results = response.json()
        except requests.exceptions.HTTPError as http_error:
            response = http_error.response
            try:
                msg = response.json()["name"]
            except (ValueError, KeyError):
                msg = "error"
            try:
                code = response.json()["code"]
            except (ValueError, KeyError):
                code = None
            try:
                detail = response.json()["detail"]
            except (ValueError, KeyError):
                detail = None

            logger.error('HTTP Error for %s to %s returned %s due to %s',
                         method, url, response.status_code, msg)

            raise WavyException(
                msg,
                error_status=response.status_code,
                error_code=code,
                error_detail=detail,
            )
        except requests.exceptions.RetryError as retry_error:
            logger.error('Max Retries reached')
            try:
                reason = retry_error.args[0].reason
            except (IndexError, AttributeError):
                reason = None
            raise WavyException(
                reason,
                error_status=-1,
            )
        except ValueError:
            results = None

        return results

    def __del__(self):
        # Make sure the connection gets closed
        if isinstance(self._session, requests.Session):
            self._session.close()
