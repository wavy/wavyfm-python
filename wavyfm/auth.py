"""
Authentication methods for wavy.fm.

This code is heavily inspired from Spotipy: https://github.com/plamere/spotipy
"""

__all__ = [
    "WavyAuthError",
    "WavyClientCredentials",
    "_WavyAuthBase",
]

import base64
import logging
import os
import time
from typing import Optional, Union, Dict

import requests

from wavyfm.error import WavyException
from wavyfm.util import ENV_VARS, API_BASE_DEFAULT

logger = logging.getLogger(__name__)


class WavyAuthError(WavyException):
    """An error during authentication"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class _WavyAuthBase(object):
    def __init__(self, requests_session: Union[requests.Session, bool] = None):
        if isinstance(requests_session, requests.Session):
            self._session = requests_session
        elif requests_session:  # Build a new session if it's a truthy value.
            self._session = requests.Session()
        else:  # Use the Requests API module as a "session".
            from requests import api
            self._session = api

    @property
    def client_id(self) -> Optional[str]:
        return self._client_id

    @client_id.setter
    def client_id(self, client_id: str):
        self._client_id = _ensure_value(client_id, "client_id")

    @property
    def client_secret(self) -> Optional[str]:
        return self._client_secret

    @client_secret.setter
    def client_secret(self, client_secret: str):
        self._client_secret = _ensure_value(client_secret, "client_secret")

    @staticmethod
    def is_token_expired(token_info):
        now = int(time.time())
        # leave 30 seconds of grace
        return token_info["expires_at"] - now < 30

    def get_access_token(self) -> str:
        raise NotImplementedError()

    def __del__(self):
        # Make sure the connection gets closed
        if isinstance(self._session, requests.Session):
            self._session.close()


class WavyClientCredentials(_WavyAuthBase):
    TOKEN_ENDPOINT = f"{API_BASE_DEFAULT}/token"

    def __init__(self,
                 client_id: str = None,
                 client_secret: str = None,
                 proxies: str = None,
                 requests_session: Union[requests.Session, bool] = True,
                 requests_timeout=None):
        """
        Initializes credentials for the Client Credentials flow. You can
        either provide a client_id and client_secret to this constructor,
        or set WAVYFM_CLIENT_ID and WAVYFM_CLIENT_SECRET environment variables.

        To get a good understanding of this flow, you should read the
        wavy.fm Authorization Guide: https://wavy.fm/developers/docs/topics/auth

        :param client_id: Your app's Client ID, obtained from the app dashboard.
        :param client_secret: Your app's Client Secret, obtained from the app dashboard.
        :param proxies: Refer to the `requests` library (:obj:`requests.Session`).
        :param requests_session: An optional :obj:`requests.Session` instance to use.
                                 If set to `True`, a session will be crafted for you.
        :param requests_timeout: Tell Requests to stop waiting for a response after a given number
                                 of seconds.
        """

        super().__init__(requests_session)

        self.client_id = client_id
        self.client_secret = client_secret
        self.token_info = None
        self.proxies = proxies
        self.requests_timeout = requests_timeout

    def get_access_token(self) -> str:
        """
        If a valid access token is in memory, this function returns it.
        If the token is expired, a new token is automatically requested.

        :return: The access token (str)
        """

        if self.token_info and not _WavyAuthBase.is_token_expired(self.token_info):
            return self.token_info["access_token"]

        token_info = self._request_access_token()
        token_info["expires_at"] = int(time.time()) + token_info["expires_in"]
        self.token_info = token_info
        return self.token_info["access_token"]

    def _request_access_token(self) -> Dict:
        """Requests a client credentials access token"""
        payload = {"grant_type": "client_credentials"}
        headers = self._make_authorization_headers()

        logger.debug(
            "sending POST request to %s with Headers: %s and Body: %r",
            self.TOKEN_ENDPOINT, headers, payload
        )

        response = self._session.post(
            self.TOKEN_ENDPOINT,
            data=payload,
            headers=headers,
            verify=True,
            proxies=self.proxies,
            timeout=self.requests_timeout,
        )

        if response.status_code == 200:
            return response.json()
        else:
            try:
                error_body = response.json()
                raise WavyAuthError(
                    error_body["name"],
                    error_status=response.status_code,
                    error_code=error_body.get("code"),
                    error_detail=error_body.get("detail")
                )
            except ValueError:
                raise WavyAuthError(
                    response.text,
                    error_status=response.status_code,
                    error_code=None,
                    error_detail=None,
                )

    def _make_authorization_headers(self) -> Dict[str, str]:
        """The request headers for authorization"""
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode("ascii")
        ).decode("ascii")

        return {"Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"}


def _ensure_value(value: str, env_key: str) -> str:
    env_val = ENV_VARS[env_key]
    _val = value or os.getenv(env_val)
    if _val is None:
        msg = "No %s. Pass it or set a %s environment variable." % (
            env_key,
            env_val,
        )
        raise WavyAuthError(msg)
    return _val
