from typing import Dict, Union


class _WavyProfileEndpoints:
    """
    Endpoints for fetching a user's information.
    """

    def __init__(self, client, user_uri: str):
        self._client = client
        self._uri = user_uri

    def __repr__(self):
        return f"<WavyProfileEndpoints '{self._uri}'>"

    def get_profile(self) -> Dict:
        """
        Retrieve this user's profile.
        """
        return self._client._internal_call("GET", f"/users/{self._uri}", None, {})

    def get_history_stats(self) -> Dict:
        """
        The total amount of listens and artists for this user.
        """
        return self._client._internal_call("GET", f"/users/{self._uri}/history/stats", None, {})

    def get_total_listens(self) -> int:
        """
        The total amount of listens this user.
        """
        stats = self.get_history_stats()
        return stats["total_listens"]

    def get_total_artists(self) -> int:
        """
        The total amount of artists this user.
        """
        stats = self.get_history_stats()
        return stats["total_artists"]

    def get_currently_listening(self) -> Dict:
        """
        What the user is currently listening to.
        The 'item' key will be None if the user is not listening to music.

        Note: This endpoint is cached for about 15 seconds, and is somewhat unstable.
        """
        return self._client._internal_call(
            "GET", f"/users/{self._uri}/history/current", None, {})

    def get_recent_listens(self, size: int = 10) -> Dict:
        """
        Retrieves the user's most recently played tracks.

        Note: the model for this endpoint is heavily subject to change.
        :param size: the amount of listens to retrieve. Valid values are 1 <= size <= 50.
        """
        return self._client._internal_call(
            "GET", f"/users/{self._uri}/history/recent", None, {"size": size})


class _WavyUsersEndpoints:
    """
    Endpoints for fetching users.
    """

    def __init__(self, client):
        self._client = client

    def by_uri(self, uri: str) -> _WavyProfileEndpoints:
        """
        Returns the endpoints for this user by URI.
        This DOES NOT make any HTTP calls.
        """
        return _WavyProfileEndpoints(self._client, uri)

    def by_id(self, user_id: str) -> _WavyProfileEndpoints:
        """
        Returns the endpoints for this user by wavy.fm User ID.
        This DOES NOT make any HTTP calls.
        """
        return _WavyProfileEndpoints(self._client, f"wavyfm:user:id:{user_id}")

    def by_username(self, username: str) -> _WavyProfileEndpoints:
        """
        Returns the endpoints for this user by wavy.fm username.
        This DOES NOT make any HTTP calls.
        """
        return _WavyProfileEndpoints(self._client, f"wavyfm:user:username:{username}")

    def by_discord_id(self, snowflake: Union[str, int]) -> _WavyProfileEndpoints:
        """
        Returns the endpoints for this user by Discord ID (snowflake).
        This DOES NOT make any HTTP calls.
        """
        return _WavyProfileEndpoints(self._client, f"wavyfm:user:discord:{snowflake}")
