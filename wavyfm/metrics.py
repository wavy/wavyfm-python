from typing import List, Dict


class _WavyMetricsEndpoints:
    """
    Global metrics for wavy.fm.
    """

    def __init__(self, client):
        self._client = client

    def get_total_listens(self) -> int:
        """
        The total amount of recorded listens on wavy.fm.
        """
        return self._client._internal_call("GET", "/metrics/total-listens", None, {})

    def get_total_users(self) -> int:
        """
        The total amount of registered users on wavy.fm.
        """
        return self._client._internal_call("GET", "/metrics/total-users", None, {})

    def get_user_listens_leaderboard(self) -> List[Dict]:
        """
        Get the top 10 registered users on wavy.fm by listen count.
        """
        return self._client._internal_call("GET", "/metrics/user-listens-leaderboard", None, {})
