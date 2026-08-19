"""Tests for content_type module."""
from pytest import raises

from checkplease.constants import DEFAULT_PATH_SUFFIX, PATH_SUFFIX_XML
from checkplease.content_type import ContentType

class TestContentType:

    def test_from_string_valid(self):
        assert(ContentType.JSON == ContentType.from_string("JSON"))
        assert(ContentType.XML == ContentType.from_string("XML"))

    def test_from_string_invalid(self):
        with raises(ValueError):
            ContentType.from_string("json")
        with raises(ValueError):
            ContentType.from_string("xml")

    def test_as_dirname(self):
        assert(ContentType.JSON.value.lower() == ContentType.JSON.as_dir_name())
        assert(ContentType.XML.value.lower() == ContentType.XML.as_dir_name())

    def test_as_uri_path(self):
        assert(DEFAULT_PATH_SUFFIX == f"{ContentType.JSON.as_uri_path()}")
        assert(f".{PATH_SUFFIX_XML}" == f"{ContentType.XML.as_uri_path()}")

    def test_as_file_extension(self):
        assert(f".{ContentType.JSON.value.lower()}" == f"{ContentType.JSON.as_file_extension()}")
        assert(f".{ContentType.XML.value.lower()}" == f"{ContentType.XML.as_file_extension()}")
