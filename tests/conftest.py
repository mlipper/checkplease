import pytest

from checkplease.content_type import ContentType
from checkplease.requests import DiffRequest, Request
from checkplease.rest_client import DiffResponse
from checkplease.url import Url


# ~------ Endpoints ------~ #
@pytest.fixture
def address_endpoint():
    return "address"

@pytest.fixture
def foo_bar_endpoint():
    return "foo/bar"

@pytest.fixture
def version_endpoint():
    return "version"

# ~------ API keys ------~ #
@pytest.fixture
def abc_key():
    return "ABC"

@pytest.fixture
def efg_key():
    return "EFG"

# ~------ URL strings ------~ #
@pytest.fixture
def local_url_str():
    return "http://localhost:8080/example"

@pytest.fixture
def remote_url_str():
    return "https://api.com/example"

# ~------ URLs ------~ #
@pytest.fixture
def local_url(efg_key, local_url_str):
    return Url(key=efg_key, url=local_url_str)

@pytest.fixture
def remote_url(abc_key, remote_url_str):
    return Url(key=abc_key, url=remote_url_str)

# ~------ Params ------~ #
@pytest.fixture
def address_params():
    return {
        "houseNumber": "120",
        "street": "Broadway",
        "borough": "Brooklyn"
    }

@pytest.fixture
def none_params():
    return None

@pytest.fixture
def one_params():
    return {"param1": "value1"}

# ~------ Ids ------~ #
@pytest.fixture
def address_id_zero():
    return "1200"

@pytest.fixture
def address_id_one():
    return "1201"

@pytest.fixture
def foo_bar_id_zero():
    return "1300"

@pytest.fixture
def foo_bar_id_one():
    return "1301"

@pytest.fixture
def version_id_zero():
    return "1400"

@pytest.fixture
def version_id_one():
    return "1401"

@pytest.fixture
def date_stamp_001():
    return "2025-05-10"

@pytest.fixture
def date_stamp_002():
    return "2026-06-12"

# ~------ Requests ------~ #
@pytest.fixture
def address_json_local_request(local_url, address_endpoint, address_id_zero, address_params):
    return Request(
        base_url=local_url,
        endpoint=address_endpoint,
        id=address_id_zero,
        params=address_params,
        content_type=ContentType.JSON
    )

@pytest.fixture
def address_json_remote_request(remote_url, address_endpoint, address_id_one, address_params):
    return Request(
        base_url=remote_url,
        endpoint=address_endpoint,
        id=address_id_one,
        params=address_params,
        content_type=ContentType.JSON
    )

@pytest.fixture
def address_xml_local_request(local_url, address_endpoint, address_id_zero, address_params):
    return Request(
        base_url=local_url,
        endpoint=address_endpoint,
        id=address_id_zero,
        params=address_params,
        content_type=ContentType.XML
    )

@pytest.fixture
def address_xml_remote_request(remote_url, address_endpoint, address_id_one, address_params):
    return Request(
        base_url=remote_url,
        endpoint=address_endpoint,
        id=address_id_one,
        params=address_params,
        content_type=ContentType.XML
    )
@pytest.fixture
def foo_bar_json_local_request(local_url, foo_bar_endpoint, foo_bar_id_zero, one_params):
    return Request(
        base_url=local_url,
        endpoint=foo_bar_endpoint,
        id=foo_bar_id_zero,
        params=one_params,
        content_type=ContentType.JSON
    )

@pytest.fixture
def foo_bar_json_remote_request(remote_url, foo_bar_endpoint, foo_bar_id_one, one_params):
    return Request(
        base_url=remote_url,
        endpoint=foo_bar_endpoint,
        id=foo_bar_id_one,
        params=one_params,
        content_type=ContentType.JSON
    )

@pytest.fixture
def version_json_local_request(local_url, version_endpoint, version_id_zero, none_params):
    return Request(
        base_url=local_url,
        endpoint=version_endpoint,
        id=version_id_zero,
        params=none_params,
        content_type=ContentType.JSON
    )

@pytest.fixture
def version_json_remote_request(remote_url, version_endpoint, version_id_one, none_params):
    return Request(
        base_url=remote_url,
        endpoint=version_endpoint,
        id=version_id_one,
        params=none_params,
        content_type=ContentType.JSON
    )

@pytest.fixture
def version_xml_local_request(local_url, version_endpoint, version_id_zero, none_params):
    return Request(
        base_url=local_url,
        endpoint=version_endpoint,
        id=version_id_zero,
        params=none_params,
        content_type=ContentType.XML
    )

@pytest.fixture
def version_xml_remote_request(remote_url, version_endpoint, version_id_one, none_params):
    return Request(
        base_url=remote_url,
        endpoint=version_endpoint,
        id=version_id_one,
        params=none_params,
        content_type=ContentType.XML
    )

# ~------ DiffRequests ------~ #
@pytest.fixture
def diff_request_json(address_json_local_request, address_json_remote_request, date_stamp_001):
    return DiffRequest(
        request_one=address_json_local_request,
        request_two=address_json_remote_request,
        date_stamp=date_stamp_001,
        content_type=ContentType.JSON
    )

@pytest.fixture
def diff_request_xml(address_xml_local_request, address_xml_remote_request, date_stamp_002):
    return DiffRequest(
        request_one=address_xml_local_request,
        request_two=address_xml_remote_request,
        date_stamp=date_stamp_002,
        content_type=ContentType.XML
    )

# ~------ DiffResponses ------~ #
class MockRestResponse:
    def __init__(self, content, apparent_encoding):
        self.content = content
        self.apparent_encoding = apparent_encoding

    def str_content(self):
        return f"{self.content}"

    def json(self):
        return self.content

@pytest.fixture
def diff_response_json():
    return DiffResponse(
        content_type=ContentType.JSON,
        response_one=MockRestResponse({"foo": "bar"}, "utf-8"),
        response_two=MockRestResponse({"foo": "duh"}, "utf-8")
    )

@pytest.fixture
def diff_response_xml():
    return DiffResponse(
        content_type=ContentType.XML,
        response_one=MockRestResponse("<response><foo>bar</foo></response>", "utf-8"),
        response_two=MockRestResponse("<response><foo>duh</foo></response>", "utf-8")
    )
