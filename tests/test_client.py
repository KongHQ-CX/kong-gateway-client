import unittest
import requests
from unittest.mock import patch, MagicMock
from kong_gateway_client.client import KongClient
from kong_gateway_client.common import ResponseObject
from kong_gateway_client.resources.consumer_groups import ConsumerGroup
from kong_gateway_client.resources.services import Service
from kong_gateway_client.resources.routes import Route
from kong_gateway_client.resources.consumers import Consumer
from kong_gateway_client.resources.plugins import PluginResource
from kong_gateway_client.resources.plugin_types.key_auth import KeyAuthPlugin
from kong_gateway_client.resources.plugin_types.acl import ACLPlugin
from kong_gateway_client.resources.plugin_types.rate_limiting_advanced import (
    RateLimitingAdvancedPlugin,
)


from src.kong_gateway_client.api import KongAPIClient
import json


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.content = json.dumps(json_data).encode("utf-8") if json_data else b""
        self.ok = True if status_code == 200 else False
        self.status_code = status_code
        self.text = "Mock API Error"

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if not self.ok:
            raise requests.HTTPError(response=self)


class TestKongClient(unittest.TestCase):
    def setUp(self):
        mock_response_auth = MagicMock()
        mock_response_auth.json.return_value = {"auth_key": "some_auth_value"}
        mock_response_auth.raise_for_status.return_value = None

        self.get_patcher = patch(
            "requests.Session.get", return_value=mock_response_auth
        )
        self.request_patcher = patch(
            "requests.Session.request", return_value=mock_response_auth
        )

        self.mock_get = self.get_patcher.start()
        self.mock_request = self.request_patcher.start()

        self.client = KongClient(
            Service,
            Route,
            PluginResource,
            Consumer,
            ConsumerGroup,
            KeyAuthPlugin,
            ACLPlugin,
            RateLimitingAdvancedPlugin,
            ResponseObject,
            admin_url="http://mock-url",
            admin_token="mock-token",
        )

    def tearDown(self):
        self.get_patcher.stop()
        self.request_patcher.stop()

    def test_request_success(self):
        mock_data = {"key": "value"}
        mock_response = MockResponse(mock_data)
        self.mock_request.return_value = mock_response

        result = self.client.request("GET", "/endpoint")
        self.assertEqual(result.key, "value")

    def test_request_failure(self):
        mock_response = MockResponse({"error": "something went wrong"}, status_code=400)
        self.mock_request.return_value = mock_response

        with self.assertRaises(requests.HTTPError):
            self.client.request("GET", "/bad-endpoint")

    def test_fetch_all(self):
        mock_data1 = [{"id": "1", "name": "item1"}, {"id": "2", "name": "item2"}]
        mock_response1 = MockResponse({"data": mock_data1, "next": "/next-endpoint"})

        mock_data2 = [{"id": "3", "name": "item3"}]
        mock_response2 = MockResponse({"data": mock_data2})

        self.mock_request.side_effect = [mock_response1, mock_response2]

        result = self.client.fetch_all("/endpoint")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[2]["name"], "item3")


if __name__ == "__main__":
    unittest.main()
