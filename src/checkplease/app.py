"""
Executes the checkplease application and management logic.

Given an initialized configuration, creates the necessary runtime components and runs them.
"""

from checkplease import log
from checkplease.diff import Diff, Summary
from checkplease.requests import Requests
from checkplease.rest_client import RestClient


def run(config):
    """Runs the checkplease application with the given configuration."""
    log.info("Starting checkplease application...")
    comparisons = config.compare
    rest_client = RestClient()
    diffs = []
    for ct in comparisons.content_types:
        diff_requests = Requests(config.requests_file, config.url_one, config.url_two, ct).load()
        log.debug(f"Loaded {len(diff_requests)} {ct.value} diff requests.")
        for diff_request in diff_requests:
            diff_response = rest_client.call(diff_request)
            diff = Diff(config.response_dir, diff_request, diff_response, config.diff)
            diff.save()
            diffs.append(diff)
    Summary(config.response_dir, diffs).summarize()
    log.info(f"Completed REST requests for {len(diffs)} diffs.")
    log.info("checkplease application finished.")
