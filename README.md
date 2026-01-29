# checkplease

Compares responses from two REST endpoints.

Benefits:

* Supports multiple diff output format (including HTML) using `difflib`
* Configurable:
  * List multiple endpoints and query strings in a file
  * Configure default URLs and API keys in file and override by environment variables
* Supports JSON and XML responses

Drawbacks:

__for now...__
* Only supports `GET` requests
* Only API key submission through `HTTP` query string

