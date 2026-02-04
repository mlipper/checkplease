"""Tests for diff module."""

import pytest
from pathlib import Path

from checkplease import io
from checkplease.constants import DIFF_HTML_FILENAME_SUFFIX
from checkplease.diff import Diff


@pytest.fixture
def response_dir(tmp_path):
    d = tmp_path / "responses"
    d.mkdir()
    return d

def expected_paths(respdir, diffreq):
    return (
        Path(
            respdir
            / diffreq.content_type.as_dir_name()
            / diffreq.dirname()
            / diffreq.file_id_one()
        ),
        Path(
            respdir
            / diffreq.content_type.as_dir_name()
            / diffreq.dirname()
            / diffreq.file_id_two(),
        ),
    )

class TestDiff:
    def test_dirpath_json(self, response_dir, diff_request_json, diff_response_json):
        expected_dir = Path(
            response_dir
            / diff_request_json.content_type.as_dir_name()
            / diff_request_json.dirname()
        )
        diff = Diff(response_dir, diff_request_json, diff_response_json)
        actual_dir = diff.dirpath()
        assert(expected_dir == actual_dir)

    def test_htmldiff_path_json(self, response_dir, diff_request_json, diff_response_json):
        expected_path = Path(
            response_dir
            / diff_request_json.content_type.as_dir_name()
            / diff_request_json.dirname()
            / f"{diff_request_json.common_name()}{DIFF_HTML_FILENAME_SUFFIX}"
        )
        diff = Diff(response_dir, diff_request_json, diff_response_json)
        actual_path = diff.htmldiff_path()
        assert(expected_path == actual_path)

    def test_dirpath_xml(self, response_dir, diff_request_xml, diff_response_xml):
        expected_dir = Path(
            response_dir
            / diff_request_xml.content_type.as_dir_name()
            / diff_request_xml.dirname()
        )
        diff = Diff(response_dir, diff_request_xml, diff_response_xml)
        actual_dir = diff.dirpath()
        assert(expected_dir == actual_dir)

    def test_htmldiff_path_xml(self, response_dir, diff_request_xml, diff_response_xml):
        expected_path = Path(
            response_dir
            / diff_request_xml.content_type.as_dir_name()
            / diff_request_xml.dirname()
            / f"{diff_request_xml.common_name()}{DIFF_HTML_FILENAME_SUFFIX}"
        )
        diff = Diff(response_dir, diff_request_xml, diff_response_xml)
        actual_path = diff.htmldiff_path()
        assert(expected_path == actual_path)

    def test_filepaths_json(self, response_dir, diff_request_json, diff_response_json):
        expected_one, expected_two = expected_paths(response_dir, diff_request_json)
        diff = Diff(response_dir, diff_request_json, diff_response_json)
        path_one, path_two = diff.filepaths()
        assert(expected_one == path_one)
        assert(expected_two == path_two)

    def test_save_responses_json(self, response_dir, diff_request_json, diff_response_json):
        diff = Diff(response_dir, diff_request_json, diff_response_json)
        diff.save_responses()
        path_one, path_two = diff.filepaths()
        expected_path_one, expected_path_two = expected_paths(response_dir, diff_request_json)
        assert(path_one.exists())
        expected_dict_one = diff_response_json.response_one.content
        actual_dict_one = io.load_json_file(path_one)
        assert(expected_dict_one == actual_dict_one)
        expected_dict_two = diff_response_json.response_two.content
        actual_dict_two = io.load_json_file(path_two)
        assert(expected_dict_two == actual_dict_two)