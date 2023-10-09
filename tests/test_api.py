import unittest
from unittest.mock import patch, MagicMock
from src.kong_gateway_client.api import KongAPIClient


class TestKongAPIClient(unittest.TestCase):
    @patch("src.kong_gateway_client.api.KongClient")
    def test_get_kong_client(self, mock_kong_client):
        client_instance = KongAPIClient("http://mock-url", admin_token="mock")
        returned_client = client_instance.get_kong_client()

        mock_kong_client.assert_called_once()
        self.assertIsInstance(returned_client, MagicMock)
