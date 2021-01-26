import unittest
from typing import List

from wavyfm import WavyClientCredentials, WavyClient
from tests.utils import integration_test

try:
    import unittest.mock as mock
except ImportError:
    import mock

patch = mock.patch
DEFAULT = mock.DEFAULT


class TestMetricsEndpoints(unittest.TestCase):

    def setUp(self):
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = WavyClient(auth_manager=WavyClientCredentials())
        return self._client

    @integration_test
    def test_wavyfm_total_listens(self):
        self.assertIsInstance(self.client.metrics.get_total_listens(), int,
                              "should receive an int")

    @integration_test
    def test_wavyfm_total_users(self):
        self.assertIsInstance(self.client.metrics.get_total_users(), int,
                              "should receive an int")

    @integration_test
    def test_wavyfm_listens_leaderboard(self):
        self.assertIsInstance(self.client.metrics.get_user_listens_leaderboard(), List,
                              "should receive a list")
