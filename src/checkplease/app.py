"""
Executes the checkplease application and management logic.

Given an initialized configuration, creates the necessary runtime components and runs them.
"""

from checkplease import log
from checkplease.diff import Diff
from checkplease.requests import Requests
from checkplease.rest_client import RestClient


def run(config):
    """Runs the checkplease application with the given configuration."""
    log.info("Starting checkplease application...")
    comparisons = config.compare
    diffs = []
    for ct in comparisons.content_types:
        diff_requests = Requests(config.requests_file, config.url_one, config.url_two, ct).load()
        log.debug(f"Loaded {len(diff_requests)} {ct.value} diff requests.")
        for diff_request in diff_requests:
            rest_client = RestClient()
            diff_response = rest_client.call(diff_request)
            diff = Diff(config.response_dir, diff_request, diff_response)
            diff.save()
            diffs.append(diff)
            #log.info(f"Processed diff request {diff_request.date_stamp} and created diff {diff_response}.")
    log.info(f"Completed REST requests for {len(diffs)} diffs.")
    log.info("checkplease application finished.")
