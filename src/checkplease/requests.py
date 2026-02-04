from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

from checkplease import constants, io
from checkplease.content_type import ContentType
from checkplease.url import Url

@dataclass
class DiffRequest:
    """Holds information about a request to be diffed."""
    content_type: ContentType
    request_one: Request
    request_two: Request
    date_stamp: str

    def common_name(self) -> str:
        return f"{self.request_one.file_id()}"

    def dirname(self) -> str:
        return self.date_stamp

    def file_id_one(self) -> str:
        return f"{self.request_one.file_id()}-1{self.content_type.as_file_extension()}"

    def file_id_two(self) -> str:
        return f"{self.request_two.file_id()}-2{self.content_type.as_file_extension()}"

@dataclass
class Request:
    """Formats URL and query parameters for a REST request."""
    base_url: Url
    endpoint: str
    id: str
    params: Optional[Dict[str, str]]
    content_type: ContentType

    def __post_init__(self):
        if self.params is None:
            self.params = {}

    def file_id(self) -> str:
        return f"{self.id}-{self.endpoint.replace('/', '-')}"
    
    def query_params(self) -> Dict[str, str]:
        self.params[constants.API_KEY_PARAM] = self.base_url.key
        return self.params
    
    def url(self) -> str:
        return f"{self.base_url.url}/{self.endpoint}{self.content_type.as_uri_path()}"

class Requests:
    """Factory class to load and configure requests."""
    def __init__(self, requests_file: Path, url_one: Url, url_two: Url, content_type: ContentType):
        self.requests_file = requests_file
        self.url_one = url_one
        self.url_two = url_two
        self.content_type = content_type

    def load(self) -> list[DiffRequest]:
        data = io.load_json_file(self.requests_file)
        reqs = data["requests"]
        diff_requests = []
        for item in reqs:
            endpoint = item.get("type")
            request_id = item.get("id")
            params = item.get("parameters", {})
            request_one = Request(
                base_url=self.url_one,
                endpoint=endpoint,
                id=request_id,
                params=params,
                content_type=self.content_type
            )
            request_two = Request(
                base_url=self.url_two,
                endpoint=endpoint,
                id=request_id,
                params=params,
                content_type=self.content_type
            )
            
            diff_request = DiffRequest(
                content_type=self.content_type,
                request_one=request_one,
                request_two=request_two,
                date_stamp=f"{datetime.now().strftime(constants.FORMAT_DATE_STAMP)}"
            )
            diff_requests.append(diff_request)
        return diff_requests