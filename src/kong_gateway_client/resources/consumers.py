from typing import List, Optional
from kong_gateway_client.client import KongClient, ResponseObject
from kong_gateway_client.utils.helpers import validate_id_or_name


class KongConsumer:
    def __init__(self, data: ResponseObject):
        self.id: str = data.get("id")
        self.username: Optional[str] = data.get("username")
        self.custom_id: Optional[str] = data.get("custom_id")
        self.tags: Optional[List[str]] = data.get("tags")

    def __repr__(self) -> str:
        return (
            f"<KongConsumer(id={self.id}, username={self.username}, "
            f"custom_id={self.custom_id}, tags={self.tags})>"
        )


class Consumer:
    """
    Consumer class to interact with Kong's Consumer entities.
    """

    ENTITY_PATH = "/consumers"

    def __init__(self, client: KongClient):
        """
        Initializes the consumer instance with a KongClient.

        Args:
        - client (KongClient): The client to send requests to Kong.
        """
        self.client = client

    def create(
        self, username: str, custom_id: str, tags: List[str] = []
    ) -> KongConsumer:
        """
        Create a new consumer in Kong.

        Args:
        - name (str): The name of the consumer.
        - custom_id (str): The custom_id of the consumer.
        - tags (List[str]): A list of tags for the consumer.

        Returns:
        - KongConsumer: Response from Kong.
        """
        if not username and not custom_id:
            raise ValueError(
                "At least one of username or custom_id should be provided."
            )

        data = {"username": username, "custom_id": custom_id, "tags": tags}

        response_data: ResponseObject = self.client.request(
            "POST", self.ENTITY_PATH, json=data
        )
        return KongConsumer(response_data)

    @validate_id_or_name
    def get(self, id_or_name: str) -> KongConsumer:
        """
        Retrieve a consumer by its ID or name

        Args:
        - id_or_name (str): The ID or name of the consumer

        Returns:
        - KongConsumer: Response from Kong.
        """

        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("GET", endpoint)
        return KongConsumer(response_data)

    def get_all(self) -> List[KongConsumer]:
        """
        Retrieve all consumers

        Returns:
        - List[KongConsumer]: A list of kong consumers.
        """

        response_data = self.client.fetch_all(self.ENTITY_PATH)
        return [KongConsumer(item) for item in response_data]

    @validate_id_or_name
    def patch(
        self,
        id_or_name: str,
        **kwargs,
    ) -> KongConsumer:
        """
        Partially update a consumer by its ID or name.

        Args:
        - id_or_name (str): The ID or name of the consumer.
        - **kwargs: Other parameters to update.

        Returns:
        - KongConsumer: The Kong consumer object.
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("PATCH", endpoint, json=kwargs)
        return KongConsumer(response_data)

    @validate_id_or_name
    def put(
        self,
        id_or_name: str,
        **kwargs,
    ) -> KongConsumer:
        """
        Update (or potentially create) a consumer by its ID or name.

        Args:
        - id_or_name (str): The ID of the consumer.
        - **kwargs: Parameters for the consumer.

        Returns:
        - KongConsumer: The Kong consumer object.
        """
        if not id_or_name:
            raise ValueError("Either the consumer id or name must be provided.")

        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("PUT", endpoint, json=kwargs)
        return KongConsumer(response_data)

    @validate_id_or_name
    def delete(self, id_or_name: str) -> None:
        """
        Delete a consumer by its ID or name.

        Args:
        - id_or_name (str): The ID or name of the consumer

        Returns:
        -
        """
        endpoint = f"{self.ENTITY_PATH}/{id_or_name}"
        response_data = self.client.request("DELETE", endpoint)
        return response_data
