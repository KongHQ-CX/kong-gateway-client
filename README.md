# Kong Gateway Client

A Python client library for interacting with the Kong API. This client library
was created for use with the `convert2kong` suite of migration tools, and as such
it only implements a small subset of the Kong Gateway admin API. It can certainly 
be used for other use cases, but the functionality would need to be extended to cover
more API resources.

## Features

* Provides easy-to-use methods for common tasks related to Kong's Rate Limiting, 
  ACLs, Key Authentication, and other plugins.
* Simplifies interactions with the admin API, handling token authentication, and error-checking.
* Supports pagination for endpoints that return multiple items.

## Installation

Install directly from the PyPi

```bash

pip install kong-gateway-client
```

## Quick start & Usage

Initialize the client:

```python
from kong_gateway_client.api import KongAPIClient

client = KongAPIClient(
    admin_url="https://your-kong-url",
    admin_token="your-admin-user"
)

# Work with routes, services, consumers, and consumer groups.
all_routes = client.route.get_all()
for route in all_routes:
    client.route.delete(route.id)

service_create = client.service.create("service-name", url="http://example.com")

route_create = client.route.create_for_service("route-name", service_create.id, paths=["/path"])

key_auth_plugin = client.key_auth_plugin.create(service_create.id, key_names=["key-name"])

```

### Handling Responses

Responses from the API are wrapped in a `ResponseObject`, which allows you to 
access the returned data as object attributes:

```python
print(result.name)
print(result.enabled)
```

### Running Tests

Ensure you have all the dependencies installed:

```bash
pip install -r requirements.txt
```
Run the tests:

```bash
python -m unittest discover -s tests
```

## Contributions

Contributions are welcome! Please fork the repository and open a pull request 
with your changes, or open an issue to discuss any improvements or fixes.
