import unittest
from typing import Dict

from tests.utils import integration_test
from wavyfm import WavyClientCredentials, WavyClient

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
    def test_wavyfm_profile_by_id(self):
        self.assertIsInstance(
            self.client.users.by_id("070f13d4-1645-4516-ae8b-372a97b86b48").get_profile(),
            Dict,
            "should receive an Dict")

    @integration_test
    def test_wavyfm_profile_by_username(self):
        self.assertIsInstance(
            self.client.users.by_username("Aram").get_profile(),
            Dict,
            "should receive an Dict")

    @integration_test
    def test_wavyfm_profile_by_discord_id(self):
        self.assertIsInstance(
            self.client.users.by_discord_id("104749643715387392").get_profile(),
            Dict,
            "should receive an Dict")

    @integration_test
    def test_wavyfm_user_total_listens(self):
        self.assertIsInstance(
            self.client.users.by_username("Aram").get_total_listens(),
            int,
            "should receive an int")

    @integration_test
    def test_wavyfm_user_total_artists(self):
        self.assertIsInstance(
            self.client.users.by_username("Aram").get_total_artists(),
            int,
            "should receive an int")

    @integration_test
    def test_wavyfm_user_history_stats(self):
        self.assertIsInstance(
            self.client.users.by_username("Aram").get_history_stats(),
            Dict,
            "should receive a Dict")

    @integration_test
    def test_wavyfm_user_currently_listening(self):
        self.assertIsInstance(
            self.client.users.by_username("Aram").get_currently_listening(),
            Dict,
            "should receive a Dict")

    @integration_test
    def test_wavyfm_user_recent_listens(self):
        self.assertIsInstance(
            self.client.users.by_username("Aram").get_recent_listens(10),
            Dict,
            "should receive a Dict")
