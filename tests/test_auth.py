import unittest

from tests.utils import integration_test
from wavyfm import WavyClientCredentials, WavyAuthError

try:
    import unittest.mock as mock
except ImportError:
    import mock

patch = mock.patch
DEFAULT = mock.DEFAULT


class TestWavyClientCredentials(unittest.TestCase):
    def test_wavyfm_client_credentials_invalid(self):
        creds = WavyClientCredentials(client_id='INVALID', client_secret='INVALID')
        with self.assertRaises(WavyAuthError) as error:
            creds.get_access_token()
        self.assertEqual(error.exception.error_status, 401,
                         "should fail with Unauthorized (401) error")

    @integration_test
    def test_wavyfm_client_credentials_valid_from_env(self):
        creds = WavyClientCredentials()

        token = creds.get_access_token()
        self.assertIsNotNone(token, "should receive valid access token")

        # check that token is reused
        new_token = creds.get_access_token()
        self.assertEqual(token, new_token, "should have the same token within expiry")
