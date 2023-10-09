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


class TestService(unittest.TestCase):
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

    def test_service_create(self):
        mock_response_services = MockResponse({"id": "123", "name": "test-service-1"})
        self.mock_request.return_value = mock_response_services
        result = self.client.service.create("test-service-1", "http://test-service-1")
        self.assertEqual(result.name, "test-service-1")

    def test_service_get_by_id(self):
        mock_response = MockResponse(
            {
                "id": "123",
                "name": "test-service-1",
                "port": "80",
                "path": "/test-url",
                "protocol": "http",
            }
        )
        self.mock_request.return_value = mock_response

        result = self.client.service.get("123")

        self.assertEqual(result.id, "123")
        self.assertEqual(result.name, "test-service-1")
        self.assertEqual(result.path, "/test-url")

    def test_service_get_by_name(self):
        mock_response = MockResponse(
            {
                "id": "123",
                "name": "test-service-1",
                "port": "80",
                "path": "/test-url",
                "protocol": "http",
            }
        )
        self.mock_request.return_value = mock_response

        result = self.client.service.get("test-service-1")

        self.assertEqual(result.id, "123")
        self.assertEqual(result.name, "test-service-1")
        self.assertEqual(result.path, "/test-url")

    def test_service_patch(self):
        mock_response = MockResponse(
            {
                "id": "123",
                "name": "updated-test-service-1",
                "port": "80",
                "path": "/updated-test-url",
                "protocol": "http",
            }
        )
        self.mock_request.return_value = mock_response

        result = self.client.service.patch(
            "123",
            name="updated-test-service-1",
            url="http://updated-test-url",
        )

        self.assertEqual(result.name, "updated-test-service-1")
        self.assertEqual(result.path, "/updated-test-url")

    def test_service_put(self):
        mock_response = MockResponse(
            {
                "id": "123",
                "name": "recreated-test-service-1",
                "port": "80",
                "path": "/recreated-test-url",
                "protocol": "http",
            }
        )
        self.mock_request.return_value = mock_response

        result = self.client.service.put(
            "123",
            name="recreated-test-service-1",
            url="http://recreated-test-url",
        )

        self.assertEqual(result.name, "recreated-test-service-1")
        self.assertEqual(result.path, "/recreated-test-url")

    def test_service_delete(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        result = self.client.service.delete("123")
        self.assertIsNone(result)
