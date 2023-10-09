import unittest
from unittest.mock import patch, MagicMock
from src.kong_gateway_client.resources.plugins import PluginResource
from src.kong_gateway_client.resources.plugin_types.key_auth import KeyAuthPlugin
from src.kong_gateway_client.api import KongAPIClient
import json


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data
        self.content = json.dumps(json_data).encode("utf-8") if json_data else b""
        self.ok = True

    def json(self):
        return self.json_data

    def raise_for_status(self):
        pass


class TestKeyAuthPlugin(unittest.TestCase):
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

        self.client = KongAPIClient(
            "http://mock-url", admin_token="mock-pass"
        ).get_kong_client()
        self.plugin_resource = PluginResource(self.client)

    def tearDown(self):
        self.get_patcher.stop()
        self.request_patcher.stop()

    def test_key_auth_create(self):
        mock_response = MockResponse({"id": "1", "name": "key-auth", "enabled": True})
        self.mock_request.return_value = mock_response

        key_auth_plugin = KeyAuthPlugin(self.plugin_resource)
        result = key_auth_plugin.create(service_id="123", key_names=["customKey"])
        self.assertEqual(result.name, "key-auth")
        self.assertTrue(result.enabled)

    def test_key_auth_retrieve(self):
        mock_response = MockResponse({"id": "2", "name": "key-auth", "enabled": False})
        self.mock_request.return_value = mock_response

        key_auth_plugin = KeyAuthPlugin(self.plugin_resource)
        result = key_auth_plugin.retrieve(plugin_id="2")
        self.assertEqual(result.name, "key-auth")
        self.assertFalse(result.enabled)

    def test_key_auth_update(self):
        mock_response = MockResponse(
            {
                "id": "3",
                "name": "key-auth",
                "enabled": True,
                "config": {"key_names": ["customKey"]},
            }
        )
        self.mock_request.return_value = mock_response

        key_auth_plugin = KeyAuthPlugin(self.plugin_resource)
        result = key_auth_plugin.update(plugin_id="3", custom_field="value")
        self.assertEqual(result.name, "key-auth")
        self.assertTrue(result.enabled)
        self.assertEqual(result.config, {"key_names": ["customKey"]})

    def test_key_auth_delete(self):
        key_auth_plugin = KeyAuthPlugin(self.plugin_resource)
        key_auth_plugin.delete(plugin_id="4")
        self.mock_request.assert_called_once()

    def test_key_auth_list_for_service(self):
        mock_data = [
            {"id": "5", "name": "key-auth", "enabled": True},
            {"id": "6", "name": "key-auth", "enabled": False},
        ]
        mock_response = MockResponse({"data": mock_data})
        self.mock_request.return_value = mock_response

        key_auth_plugin = KeyAuthPlugin(self.plugin_resource)
        results = key_auth_plugin.list_for_service(service_id="789")
        self.assertEqual(len(results), 2)
        self.assertEqual(results.data[0].name, "key-auth")
        self.assertTrue(results.data[0].enabled)

    def test_key_auth_list_for_route(self):
        mock_data = [
            {"id": "7", "name": "key-auth", "enabled": True},
            {"id": "8", "name": "key-auth", "enabled": False},
        ]
        mock_response = MockResponse({"data": mock_data})
        self.mock_request.return_value = mock_response

        key_auth_plugin = KeyAuthPlugin(self.plugin_resource)
        results = key_auth_plugin.list_for_route(route_id="012")
        self.assertEqual(len(results), 2)
        self.assertEqual(results.data[0].name, "key-auth")
        self.assertTrue(results.data[0].enabled)
