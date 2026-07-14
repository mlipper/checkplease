# checkplease

**checkplease** is a CLI tool that compares REST API responses between two different service endpoints and produces visual HTML diffs of the results.

At a high level, it:

1. Reads a list of configured API requests from `requests.json`
2. Fires each request against two configured URLs (e.g., a local dev instance vs. a live API) for both JSON and XML response formats
3. Saves the response pairs to a date-stamped output directory under `responses/`
4. Generates a full side-by-side HTML diff for each request pair (use `--diff-short` to show only the changed sections), and optionally a unified `.patch` file (use `--diff-patch`)
5. Produces an `index.html` summary page linking to only the responses that differ between the two endpoints

The intended use case is giving a developer a quick, browsable view of how API responses have changed between two versions of a service — for example, to decide whether changes are backwards-compatible enough to provide them as a minor point release versus a new major version release.

## Features

* Supports multiple diff output formats (including HTML) using `difflib`
* Configurable:
  * List multiple endpoints and query strings in a file
  * Configure default URLs and API keys in a file and override via environment variables
* Supports JSON and XML responses

## Limitations

__for now...__
* Only supports `GET` requests
* Only supports API key submission through HTTP query string

