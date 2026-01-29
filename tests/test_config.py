"""Unit tests for config module."""


import pytest
import yaml
from pathlib import Path

from checkplease.config import load_config, Environment
from checkplease.content_type import ContentType
from checkplease.url import Url

@pytest.fixture
def url_one():
    return Url(
        key="secret1",
        url="https://url.one.com"
    )

@pytest.fixture
def url_two():
    return Url(
        key="secret2",
        url="https://url.two.com"
    )

@pytest.fixture
def config_data(url_one, url_two):
    content = f"""comparisons: 
  - JSON
  - XML
environment:
  key_one: KEY_ONE
  url_one: URL_ONE
  key_two: KEY_TWO
  url_two: URL_TWO
requests_file: requests.json
response_dir: results
url_one:
  key: {url_one.key}
  url: {url_one.url}
url_two:
  key: {url_two.key}
  url: {url_two.url}
"""
    return yaml.safe_load(content)

@pytest.fixture
def config(config_data):
    return load_config(config_data)

@pytest.fixture
def patched_env(monkeypatch):
    monkeypatch.setenv("KEY_ONE", "bigsecret1")
    monkeypatch.setenv("URL_ONE", "https://override.one.com")
    monkeypatch.setenv("KEY_TWO", "bigsecret2")
    monkeypatch.setenv("URL_TWO", "https://override.two.com")
    return Environment(key_one="KEY_ONE", url_one="URL_ONE", key_two="KEY_TWO", url_two="URL_TWO")

class TestConfig:
    def test_config_loaded(self, config, url_one, url_two):
        assert config is not None
        assert ContentType.JSON in config.compare.content_types
        assert ContentType.XML in config.compare.content_types
        assert isinstance(config.requests_file, Path)
        assert isinstance(config.response_dir, Path)
        assert config.url_one == url_one
        assert config.url_two == url_two
        assert config.environment.key_one == "KEY_ONE"
        assert config.environment.url_one == "URL_ONE"
        assert config.environment.key_two == "KEY_TWO"
        assert config.environment.url_two == "URL_TWO"

    def test_environment_overrides(self, config, patched_env):
        resolved_url_one = patched_env.resolve_url_one(config.url_one)
        resolved_url_two = patched_env.resolve_url_two(config.url_two)

        assert resolved_url_one.key == "bigsecret1"
        assert resolved_url_one.url == "https://override.one.com"
        assert resolved_url_two.key == "bigsecret2"
        assert resolved_url_two.url == "https://override.two.com"
