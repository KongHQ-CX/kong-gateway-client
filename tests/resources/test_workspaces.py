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


class TestWorkspace(unittest.TestCase):
    def setUp(self):
        mock_response_auth = MagicMock()
        mock_response_auth.json.return_value = {"auth_key": "some_auth_value"}
        mock_response_auth.raise_for_status.return_value = None

        self.get_patcher = patch.object(Session, "get", return_value=mock_response_auth)
        self.request_patcher = patch.object(
            Session, "request", return_value=mock_response_auth
        )
        self.mock_request = self.request_patcher.start()

        self.mock_get = self.get_patcher.start()

        self.mock_request = self.request_patcher.start()

        self.client = KongAPIClient(
            "http://mock-url", admin_token="mock-pass"
        ).get_kong_client()

    def tearDown(self):
        self.get_patcher.stop()
        self.request_patcher.stop()

    def test_workspace_create(self):
        mock_response = MockResponse({"id": "123", "name": "test-workspace-1"})
        self.mock_request.return_value = mock_response
        result = self.client.workspace.create(name="123")
        self.assertEqual(result.name, "test-workspace-1")

    def test_workspace_get(self):
        mock_response = MockResponse({"id": "123", "name": "test-workspace-1"})
        self.mock_request.return_value = mock_response

        result = self.client.workspace.get("123")
        self.assertEqual(result.name, "test-workspace-1")

    def test_workspace_delete(self):
        mock_response = MagicMock()
        self.mock_request.return_value = mock_response

        result = self.client.workspace.delete("123")
        self.assertTrue(result)

    def test_workspace_patch(self):
        mock_response = MockResponse(
            {"id": "123", "name": "test-workspace-1", "comment": "Updated Comment"}
        )
        self.mock_request.return_value = mock_response

        result = self.client.workspace.patch("123", comment="Upadated Comment")
        self.assertEqual(result.comment, "Updated Comment")

    def test_workspace_put_update(self):
        mock_response = MockResponse({"id": "123", "name": "updated-workspace-1"})
        self.mock_request.return_value = mock_response

        result = self.client.workspace.put("123", "upadated-workspace-1")
        self.assertEqual(result.name, "updated-workspace-1")

    def test_workspace_put_create(self):
        mock_response = MockResponse({"id": "124", "name": "new-workspace-1"})
        self.mock_request.return_value = mock_response

        result = self.client.workspace.put("123", "new-workspace-1")
        self.assertEqual(result.name, "new-workspace-1")


if __name__ == "__main__":
    unittest.main()
