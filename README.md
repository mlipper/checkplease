# checkplease

**checkplease** is a CLI tool that compares REST API responses between two different service endpoints and produces visual HTML diffs of the results.

At a high level, it:

1. Reads a list of configured API requests from `requests.json`
2. Fires each request against two configured URLs (e.g., a local dev instance vs. a live API) for both JSON and XML response formats
3. Saves the response pairs to a date-stamped output directory under `responses/`
4. Generates a full side-by-side HTML diff for each request pair (use `--diff-short` to show only the changed sections), and optionally a unified `.patch` file (use `--diff-patch`)
5. Produces an `index.html` summary page linking to only the responses that differ between the two endpoints

The intended use case is giving a developer a quick, browsable view of how API responses have changed between two versions of a REST service — for example, to decide whether changes are backwards-compatible enough to provide them as a minor point release versus a new major version.

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
* Does not examine `HTTP` headers for changes

## CLI

```text
Usage: checkplease [OPTIONS]

Runs the checkplease application.

If file .local exists in the same directory as this script, it is sourced
before any command line options are processed. Any API_* variable can be
configured there and will override the default values used if unset.

Options can be used to set the API_URL_ONE and API_URL_TWO environment
variables. When given, these take precedence over either of these variables
even if they've already be set.

At this time, the API_KEY_ONE and API_KEY_TWO are assumed to have already been
set or configured in .local.

Options:
  --help                  Show this message.

  --container             The local container should be run and environment
                          variable API_URL_ONE will be set using this template:

                          http://localhost:<local-port>/geoclient/v2

                          If the --local-port option is not given, it defaults
                          to 9090.

                          Default is not to run a local container and assume
                          that the value of API_URL_ONE refers to a running
                          Geoclient v2 service. 

  --diff-patch            If given, a .patch file is generated in unified diff
                          format in addition to an HTML diff.
                          Defaults to false.

  --diff-short            If given, the HTML diff will be generated in short
                          format. Short format will only show the differences
                          and a few lines of context instead of the full
                          response files.
                          Defaults to false.

  --config                Show the value of environment variables used by
                          this application, the arguments of this script
                          and call the app with the '--config' argument
                          which outputs the app's final configuration.

                          NOTE: If this flag is given, the application is not run.

  NOTE: The following options are ignored if --container flag is not given.

  --local-port=<port>     Local port to use for the container.
                          Defaults to 9090.

  --container-port=<port> Container port to use for the container.
                          Defaults to 8080.

  --image-name=<name>     Name of the image to run.
                          Defaults to "geoclient".

  --image-tag=<tag>       Tag of the image to run.
                          Defaults to "latest".

  NOTE: If any of the following options are given and the --container flag is
        also given, no attempt is made to validate they match any other
        container-related options provided.

  --url-one=<url>         Sets the value of the API_URL_ONE environment variable.
                          This takes precedence over any other configuration
                          that sets this variable.
                          Defaults to http://localhost:9090/geoclient/v2 if API_URL_ONE
                          has not been set.

  --url-two=<url>         Sets the value of the API_URL_TWO environment variable.
                          This takes precedence over any other configuration
                          that sets this variable.
                          Defaults to https://api.nyc.gov/geoclient/v2 if API_URL_TWO
                          has not been set.
```
## Development

### Running the tests

```sh
uv run pytest
```
