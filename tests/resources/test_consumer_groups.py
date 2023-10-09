import unittest
from unittest.mock import MagicMock, patch
from requests import Session

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


class TestConsumerGroup(unittest.TestCase):
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

    def test_consumer_group_create(self):
        mock_response = MockResponse({"id": "456", "name": "test-group"})
        self.mock_request.return_value = mock_response

        result = self.client.consumer_group.create("test-group")
        self.assertEqual(result.name, "test-group")

    def test_consumer_group_get(self):
        mock_response = MockResponse({"id": "456", "name": "test-group"})
        self.mock_request.return_value = mock_response

        result = self.client.consumer_group.get("456")
        self.assertEqual(result.name, "test-group")

    def test_consumer_group_get_consumers(self):
        mock_response = MockResponse(
            {
                "consumers": [
                    {
                        "id": "123",
                        "username": "test-consumer-1",
                        "custom_id": "custom-1",
                    },
                    {
                        "id": "124",
                        "username": "test-consumer-2",
                        "custom_id": "custom-2",
                    },
                ]
            }
        )
        self.mock_request.return_value = mock_response

        results = self.client.consumer_group.get_consumers("test-group")
        self.assertEqual(len(results.consumers), 2)

    def test_consumer_group_add_consumer(self):
        mock_response = MockResponse({"consumers": [{"id": "123", "group": "456"}]})
        self.mock_request.return_value = mock_response

        result = self.client.consumer_group.add_consumer(
            "test-consumer-1", "test-group"
        )
        self.assertEqual(len(result.consumers), 1)
        self.assertEqual(result.consumers[0].id, "123")

    def test_consumer_group_get_all(self):
        mock_response = MockResponse(
            {
                "data": [
                    {"id": "456", "name": "test-group-1"},
                    {"id": "457", "name": "test-group-2"},
                ]
            }
        )
        self.mock_request.return_value = mock_response

        results = self.client.consumer_group.get_all()
        self.assertEqual(len(results), 2)

    def test_consumer_group_put(self):
        mock_response = MockResponse({"id": "456", "name": "updated-test-group"})
        self.mock_request.return_value = mock_response

        result = self.client.consumer_group.put("456", name="updated-test-group")
        self.assertEqual(result.name, "updated-test-group")

    def test_consumer_group_delete(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        result = self.client.consumer_group.delete("456")
        self.assertIsNone(result)

    def test_consumer_group_delete_consumer(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        result = self.client.consumer_group.delete_consumer(
            "test-group", "test-consumer-1"
        )
        self.assertIsNone(result)

    def test_consumer_group_delete_consumers(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        result = self.client.consumer_group.delete_consumers("test-group")
        self.assertIsNone(result)

    def test_consumer_group_configure_rate_limit(self):
        mock_response = MockResponse(
            {
                "config": {
                    "limit": [10],
                    "window_size": [60],
                    "window_type": "sliding",
                    "retry_after_jitter_max": 0,
                },
                "group": "456",
                "plugin": "rate-limiting-advanced",
            }
        )
        self.mock_request.return_value = mock_response

        result = self.client.consumer_group.configure_rate_limit(
            "test-group", [10], [60]
        )
        self.assertEqual(result.config["limit"][0], 10)
        self.assertEqual(result.config["window_size"][0], 60)
        self.assertEqual(result.group, "456")
        self.assertEqual(result.plugin, "rate-limiting-advanced")
