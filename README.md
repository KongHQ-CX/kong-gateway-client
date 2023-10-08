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

pip install kong-gateway-client.git
```

## Quick start

Initialize the client:

```python

from kong_gateway_client.client import KongClient

client = KongClient(admin_url="http://your-kong-url:8001", admin_token="your-admin-token")
```

## Working with Plugins

Here's a brief overview of how to use some of the plugin features:

### ACL Plugin

```python
from kong_gateway_client.resources.plugin_types.acl import ACLPlugin

acl_plugin = ACLPlugin(client.plugin_resource)
result = acl_plugin.create(service_id="123", allow=["admin"])
```

### Rate Limiting Advanced Plugin

```python
from kong_gateway_client.resources.plugin_types.rate_limiting_advanced import RateLimitingAdvancedPlugin

rla_plugin = RateLimitingAdvancedPlugin(client.plugin_resource)
result = rla_plugin.create(service_id="123", limit=[100])
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
