# Changelog

## 0.5.0

🆕 New features:

- Added the workspace resource, users can perform CRUD operations on workspaces
  via the client
- Updated the validators so that they now check args and keyword args

🔧 Fixes:

- Fixed the return value of delete service

💥 Breaking changes:

- The workspace argument is now target_workspace

  ([PR #5](https://github.com/KongHQ-CX/kong-gateway-client/pull/5))


## 0.4.0

🆕 New features:

- Added a `KongAPIClient` facade with method delegation to `KongClient`

  ([PR #4](https://github.com/KongHQ-CX/kong-gateway-client/pull/4))

## 0.3.0

🆕 New features:

- Added routes resource

  ([PR #3](https://github.com/KongHQ-CX/kong-gateway-client/pull/3))

## 0.2.0

🆕 New features:

- Added key auth credential creation for consumers
- Added ACL consumer configuration

  ([PR #2](https://github.com/KongHQ-CX/kong-gateway-client/pull/2))

## 0.1.0

🆕 New features:

- first code commit

- CHANGELOG added

- added test workflow

  For changes prior to this, refer to [commit history](https://github.com/KongHQ-CX/kong-gateway-client/commits/main)

  ([PR #1](https://github.com/KongHQ-CX/kong-gateway-client/pull/1))
