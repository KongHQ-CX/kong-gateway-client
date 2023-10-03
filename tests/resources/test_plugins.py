import unittest
from unittest.mock import MagicMock, patch
from requests import Session
from src.kong_gateway_client.resources.plugins import PluginResource
from src.kong_gateway_client.client import KongClient
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


class TestPluginResource(unittest.TestCase):
    def setUp(self):
        mock_response_auth = MagicMock()
        mock_response_auth.json.return_value = {"auth_key": "some_auth_value"}
        mock_response_auth.raise_for_status.return_value = None

        self.get_patcher = patch.object(Session, "get", return_value=mock_response_auth)
        self.request_patcher = patch.object(
            Session, "request", return_value=mock_response_auth
        )

        self.mock_get = self.get_patcher.start()
        self.mock_request = self.request_patcher.start()

        self.client = KongClient("http://mock-url", admin_token="mock-pass")

    def tearDown(self):
        self.get_patcher.stop()
        self.request_patcher.stop()

    def test_plugin_create(self):
        mock_response = MockResponse(
            {"id": "789", "name": "test-plugin", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.create("test-plugin")
        self.assertEqual(result.name, "test-plugin")

    def test_plugin_get(self):
        mock_response = MockResponse(
            {"id": "789", "name": "test-plugin", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.get("789")
        self.assertEqual(result.name, "test-plugin")

    def test_plugin_update(self):
        mock_response = MockResponse(
            {"id": "789", "name": "updated-plugin", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.update("789", name="updated-plugin")
        self.assertEqual(result.name, "updated-plugin")

    def test_plugin_delete(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        plugin_resource.delete("789")
        self.mock_request.assert_called_with(
            "DELETE", "http://mock-url/default/plugins/789", verify=False
        )

    def test_plugin_list_all(self):
        mock_response = MockResponse(
            {
                "data": [
                    {"id": "789", "name": "test-plugin-1", "enabled": True},
                    {"id": "790", "name": "test-plugin-2", "enabled": True},
                ]
            }
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        results = plugin_resource.list_all()
        self.assertEqual(len(results.data), 2)

    def test_plugin_create_for_route(self):
        mock_response = MockResponse(
            {"id": "789", "name": "test-plugin-for-route", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.create_for_route("test-route", "test-plugin-for-route")
        self.assertEqual(result.name, "test-plugin-for-route")

    def test_plugin_get_for_route(self):
        mock_response = MockResponse(
            {"id": "789", "name": "test-plugin-for-route", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.get_for_route("test-route", "789")
        self.assertEqual(result.name, "test-plugin-for-route")

    def test_plugin_update_for_route(self):
        mock_response = MockResponse(
            {"id": "789", "name": "updated-plugin-for-route", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.update_for_route(
            "test-route", "789", name="updated-plugin-for-route"
        )
        self.assertEqual(result.name, "updated-plugin-for-route")

    def test_plugin_delete_for_route(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        plugin_resource.delete_for_route("test-route", "789")
        self.mock_request.assert_called_with(
            "DELETE",
            "http://mock-url/default/routes/test-route/plugins/789",
            verify=False,
        )

    def test_plugin_create_for_service(self):
        mock_response = MockResponse(
            {"id": "789", "name": "test-plugin-for-service", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.create_for_service(
            "test-service", "test-plugin-for-service"
        )
        self.assertEqual(result.name, "test-plugin-for-service")

    def test_plugin_get_for_service(self):
        mock_response = MockResponse(
            {"id": "789", "name": "test-plugin-for-service", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.get_for_service("test-service", "789")
        self.assertEqual(result.name, "test-plugin-for-service")

    def test_plugin_update_for_service(self):
        mock_response = MockResponse(
            {"id": "789", "name": "updated-plugin-for-service", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.update_for_service(
            "test-service", "789", name="updated-plugin-for-service"
        )
        self.assertEqual(result.name, "updated-plugin-for-service")

    def test_plugin_delete_for_service(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        plugin_resource.delete_for_service("test-service", "789")
        self.mock_request.assert_called_with(
            "DELETE",
            "http://mock-url/default/services/test-service/plugins/789",
            verify=False,
        )

    def test_plugin_create_for_consumer(self):
        mock_response = MockResponse(
            {"id": "789", "name": "test-plugin-for-consumer", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.create_for_consumer(
            "test-consumer", "test-plugin-for-consumer"
        )
        self.assertEqual(result.name, "test-plugin-for-consumer")

    def test_plugin_get_for_consumer(self):
        mock_response = MockResponse(
            {"id": "789", "name": "test-plugin-for-consumer", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.get_for_consumer("test-consumer", "789")
        self.assertEqual(result.name, "test-plugin-for-consumer")

    def test_plugin_update_for_consumer(self):
        mock_response = MockResponse(
            {"id": "789", "name": "updated-plugin-for-consumer", "enabled": True}
        )
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        result = plugin_resource.update_for_consumer(
            "test-consumer", "789", name="updated-plugin-for-consumer"
        )
        self.assertEqual(result.name, "updated-plugin-for-consumer")

    def test_plugin_delete_for_consumer(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        plugin_resource = PluginResource(self.client)
        plugin_resource.delete_for_consumer("test-consumer", "789")
        self.mock_request.assert_called_with(
            "DELETE",
            "http://mock-url/default/consumers/test-consumer/plugins/789",
            verify=False,
        )
