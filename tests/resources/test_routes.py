import unittest
from unittest.mock import MagicMock, patch
from requests import Session

from src.kong_gateway_client.api import KongAPIClient
import json


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data
        self.content = json.dumps(json_data).encode("utf-8") if json_data else b""

    def json(self):
        return self.json_data

    def ok(self):
        return True

    def raise_for_status(self):
        pass


class TestRoute(unittest.TestCase):
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

        self.client = KongAPIClient(
            "http://mock-url", admin_token="mock-pass"
        ).get_kong_client()

    def tearDown(self):
        self.get_patcher.stop()
        self.request_patcher.stop()

    def test_route_create(self):
        mock_response_routes = MockResponse({"id": "123", "name": "test-route-1"})
        self.mock_request.return_value = mock_response_routes
        result = self.client.route.create("test-route-1", protocols=["http", "https"])
        self.assertEqual(result.name, "test-route-1")

    def test_route_get_by_id(self):
        mock_response = MockResponse(
            {
                "id": "123",
                "name": "test-route-1",
                "protocols": ["http"],
                "methods": ["GET"],
                "hosts": ["example.com"],
                "paths": ["/test-route"],
            }
        )
        self.mock_request.return_value = mock_response

        result = self.client.route.get("123")

        self.assertEqual(result.id, "123")
        self.assertEqual(result.name, "test-route-1")
        self.assertEqual(result.paths[0], "/test-route")

    def test_route_patch(self):
        mock_response = MockResponse(
            {
                "id": "123",
                "name": "updated-test-route-1",
                "protocols": ["http"],
                "methods": ["GET"],
                "hosts": ["example.com"],
                "paths": ["/updated-test-route"],
            }
        )
        self.mock_request.return_value = mock_response

        result = self.client.route.patch(
            "123", name="updated-test-route-1", protocols=["http"]
        )

        self.assertEqual(result.name, "updated-test-route-1")
        self.assertEqual(result.paths[0], "/updated-test-route")

    def test_route_put(self):
        mock_response = MockResponse(
            {
                "id": "123",
                "name": "recreated-test-route-1",
                "protocols": ["http"],
                "methods": ["GET"],
                "hosts": ["example.com"],
                "paths": ["/recreated-test-route"],
            }
        )
        self.mock_request.return_value = mock_response

        result = self.client.route.put(
            "123", name="recreated-test-route-1", protocols=["http"]
        )

        self.assertEqual(result.name, "recreated-test-route-1")
        self.assertEqual(result.paths[0], "/recreated-test-route")

    def test_route_delete(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        result = self.client.route.delete("123")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
