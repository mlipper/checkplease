import os
from ast import List
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from checkplease.content_type import ContentType
from checkplease.url import Url

@dataclass
class Environment:
    key_one: str
    url_one: str
    key_two: str
    url_two: str

    # Use environment variables to override config values if set
    def resolve_url_one(self, url: Url) -> Url:
        url.key = os.environ.get(self.key_one, url.key)
        url.url = os.environ.get(self.url_one, url.url)
        return url

    def resolve_url_two(self, url: Url) -> Url:
        url.key = os.environ.get(self.key_two, url.key)
        url.url = os.environ.get(self.url_two, url.url)
        return url

@dataclass
class ContentTypes:
    """ Specifies which ContentType should be compared: JSON, XML, or both."""
    content_types: List[ContentType]

    def only_json(self):
        self.content_types = [ContentType.JSON]

    def only_xml(self):
        self.content_types = [ContentType.XML]


@dataclass
class Config:
    compare: ContentTypes
    environment: Environment
    requests_file: Path
    response_dir: Path
    url_one: Url
    url_two: Url

    def show_config(self) -> str:
        return f"""
comparisons: {', '.join([ct.value for ct in self.compare.content_types])}
environment:
  API_KEY_ONE={os.environ.get("API_KEY_ONE", "<unset>")}
  API_URL_ONE={os.environ.get("API_URL_ONE", "<unset>")}
  API_KEY_TWO={os.environ.get("API_KEY_TWO", "<unset>")}
  API_URL_TWO={os.environ.get("API_URL_TWO", "<unset>")}
requests_file: {self.requests_file.resolve()}
response_dir: {self.response_dir.resolve()}
url_one:
  key: {self.url_one.key}
  url: {self.url_one.url}
url_two:
  key: {self.url_two.key}
  url: {self.url_two.url}
"""

def load_config(data: Any) -> Config:
    environment=Environment(
        key_one=data['environment']['key_one'],
        url_one=data['environment']['url_one'],
        key_two=data['environment']['key_two'],
        url_two=data['environment']['url_two'],
    )
    # Initialize Url instances with config file values
    # and update with environment variables if set
    url_one=Url(
        key=data['url_one']['key'],
        url=data['url_one']['url'],
    )
    environment.resolve_url_one(url_one)
    url_two=Url(
        key=data['url_two']['key'],
        url=data['url_two']['url'],
    )
    environment.resolve_url_two(url_two)
    # Content type comparisons to make for each request
    comparisons = [ContentType.from_string(ct) for ct in data['comparisons']]
    return Config(
        compare=ContentTypes(content_types=comparisons),
        environment=environment,
        requests_file=Path(data['requests_file']),
        response_dir=Path(data['response_dir']),
        url_one=url_one,
        url_two=url_two,
    )
