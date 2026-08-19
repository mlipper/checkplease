from dataclasses import dataclass
from typing import Any
import requests as client
from requests import Response as RestResponse

from checkplease.content_type import ContentType
from checkplease.requests import DiffRequest, Request

@dataclass
class DiffResponse:
    content_type: ContentType
    response_one: Any
    response_two: Any

"""Client to make REST requests based on DiffRequest objects."""
class RestClient:

    def call(self, diff_request: DiffRequest) -> DiffResponse:
        """Make both requests, save responses and return a Diff."""
        response_one = self.make_request(diff_request.request_one)
        response_two = self.make_request(diff_request.request_two)

        return DiffResponse(diff_request.content_type, response_one, response_two)

    def make_request(self, request: Request) -> RestResponse:
        """Make a REST request and return the response."""
        if request.url() is None:
            raise ValueError("Request URL cannot be None")
        response = client.get(request.url(), params=request.query_params())
        response.raise_for_status()
        return response
