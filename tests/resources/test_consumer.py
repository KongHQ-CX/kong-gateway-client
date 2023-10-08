import unittest
from unittest.mock import MagicMock, patch
from requests import Session
from src.kong_gateway_client.resources.consumers import Consumer
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


class TestConsumer(unittest.TestCase):
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

    def test_consumer_create(self):
        mock_response = MockResponse(
            {"id": "123", "username": "test-consumer-1", "custom_id": "custom-1"}
        )
        self.mock_request.return_value = mock_response
        consumer = Consumer(self.client)
        result = consumer.create("test-consumer-1", "custom-1")
        self.assertEqual(result.username, "test-consumer-1")
        self.assertEqual(result.custom_id, "custom-1")

    def test_consumer_get_by_id(self):
        mock_response = MockResponse(
            {"id": "123", "username": "test-consumer-1", "custom_id": "custom-1"}
        )
        self.mock_request.return_value = mock_response

        consumer = Consumer(self.client)
        result = consumer.get("123")

        self.assertEqual(result.id, "123")
        self.assertEqual(result.username, "test-consumer-1")
        self.assertEqual(result.custom_id, "custom-1")

    def test_consumer_get_by_name(self):
        mock_response = MockResponse(
            {"id": "123", "username": "test-consumer-1", "custom_id": "custom-1"}
        )
        self.mock_request.return_value = mock_response

        consumer = Consumer(self.client)
        result = consumer.get("test-consumer-1")

        self.assertEqual(result.id, "123")
        self.assertEqual(result.username, "test-consumer-1")
        self.assertEqual(result.custom_id, "custom-1")

    def test_consumer_patch(self):
        mock_response = MockResponse(
            {
                "id": "123",
                "username": "updated-test-consumer-1",
                "custom_id": "custom-1",
            }
        )
        self.mock_request.return_value = mock_response

        consumer = Consumer(self.client)
        result = consumer.patch(
            "123",
            username="updated-test-consumer-1",
            custom_id="custom-1",
        )

        self.assertEqual(result.username, "updated-test-consumer-1")
        self.assertEqual(result.custom_id, "custom-1")

    def test_consumre_put(self):
        mock_response = MockResponse(
            {
                "id": "123",
                "username": "recreated-test-consumer-1",
                "custom_id": "custom-1",
            }
        )
        self.mock_request.return_value = mock_response

        consumer = Consumer(self.client)
        result = consumer.put(
            "123",
            name="recreated-test-consumer-1",
            custom_id="custom-1",
        )

        self.assertEqual(result.username, "recreated-test-consumer-1")
        self.assertEqual(result.custom_id, "custom-1")

    def test_consumer_delete(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        consumer = Consumer(self.client)
        result = consumer.delete("123")
        self.assertIsNone(result)

    def test_consumer_get_all(self):
        mock_response = MockResponse(
            {
                "data": [
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

        consumer = Consumer(self.client)
        results = consumer.get_all()

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, "123")
        self.assertEqual(results[1].id, "124")

    def test_consumer_create_no_username_or_custom_id(self):
        consumer = Consumer(self.client)
        with self.assertRaises(ValueError):
            consumer.create("", "")

    def test_consumer_create_kong_error(self):
        mock_response = MockResponse(None)
        mock_response.ok = False
        self.mock_request.return_value = mock_response

        consumer = Consumer(self.client)
        with self.assertRaises(Exception):
            consumer.create("test-consumer-1", "custom-1")

    def test_consumer_get_all_no_consumers(self):
        mock_response = MockResponse([])
        self.mock_request.return_value = mock_response

        consumer = Consumer(self.client)
        results = consumer.get_all()

        self.assertEqual(len(results), 0)


class TestConsumerACL(unittest.TestCase):
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
        self.consumer = Consumer(self.client)

    def tearDown(self):
        self.get_patcher.stop()
        self.request_patcher.stop()

    def test_get_acls_by_consumer(self):
        mock_response = MockResponse(
            {
                "total": 1,
                "data": [
                    {
                        "group": "bar-group",
                        "created_at": 1511391162000,
                        "id": "0905f68e-fee3-4ecb-965c-fcf6912bf29e",
                        "consumer": {"id": "c0d92ba9-8306-482a-b60d-0cfdd2f0e880"},
                    }
                ],
            }
        )
        self.mock_request.return_value = mock_response

        results = self.consumer.get_acls_by_consumer("test-consumer")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].group, "bar-group")

    def test_get_acl_by_id(self):
        mock_response = MockResponse(
            {
                "group": "foo-group",
                "created_at": 1511391159000,
                "id": "724d1be7-c39e-443d-bf36-41db17452c75",
                "consumer": {"id": "89a41fef-3b40-4bb0-b5af-33da57a7ffcf"},
            }
        )
        self.mock_request.return_value = mock_response

        result = self.consumer.get_acl("test-consumer", "acl-id")

        self.assertEqual(result.group, "foo-group")

    def test_get_consumer_by_acl(self):
        mock_response = MockResponse(
            {
                "created_at": 1507936639000,
                "username": "foo",
                "id": "c0d92ba9-8306-482a-b60d-0cfdd2f0e880",
            }
        )
        self.mock_request.return_value = mock_response

        result = self.consumer.get_consumer_by_acl("acl-id")

        self.assertEqual(result["username"], "foo")

    def test_update_or_insert_acl(self):
        mock_response = MockResponse(
            {
                "group": "new-group",
                "created_at": 1622000000,
                "id": "acl-id",
                "consumer": {"id": "consumer-id"},
            }
        )
        self.mock_request.return_value = mock_response

        result = self.consumer.update_or_insert_acl(
            "test-consumer", "acl-id", group="new-group"
        )

        self.assertEqual(result.group, "new-group")

    def test_update_acl_group_by_id(self):
        mock_response = MockResponse(
            {
                "group": "group1",
                "created_at": 1622000000,
                "id": "acl-id",
                "consumer": {"id": "consumer-id"},
            }
        )
        self.mock_request.return_value = mock_response

        result = self.consumer.update_acl_group("test-consumer", group="group1")

        self.assertEqual(result.group, "group1")

    def test_delete_acl_by_id(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        result = self.consumer.delete_acl("test-consumer", "acl-id")

        self.assertIsNone(result)

    def test_delete_acl_by_group_name(self):
        mock_response = MockResponse({})
        self.mock_request.return_value = mock_response

        result = self.consumer.delete_acl("test-consumer", "test-group")

        self.assertIsNone(result)


class TestConsumerKeyAuth(unittest.TestCase):
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
        self.consumer = Consumer(self.client)

    def tearDown(self):
        self.get_patcher.stop()
        self.request_patcher.stop()

    def test_create_key_auth(self):
        mock_response = MockResponse(
            {
                "key": "5SRmk6gLnTy1SyQ1Cl9GzoRXJbjYGGbZ",
                "created_at": 1655412883,
                "tags": None,
                "ttl": None,
                "id": "0103844a-0b40-42c8-aa71-64e98e2e525f",
                "consumer": {"id": "d9e37c7d-3261-4b7b-81a6-a94bc203a0ca"},
            }
        )
        self.mock_request.return_value = mock_response

        result = self.consumer.add_key_auth("test-consumer")

        self.assertEqual(result.key, "5SRmk6gLnTy1SyQ1Cl9GzoRXJbjYGGbZ")
