"""Tests for diff module."""

from pathlib import Path

import pytest

from checkplease import io, log
from checkplease.config import DiffConfig
from checkplease.constants import DIFF_HTML_FILENAME_SUFFIX, DIFF_PATCH_FILENAME_SUFFIX
from checkplease.content_type import ContentType
from checkplease.diff import Diff, Summary
from checkplease.requests import DiffRequest, Request
from checkplease.rest_client import DiffResponse
from tests import FIXTURE_DATE_STAMP, FIXTURE_DIR, json_files, xml_files


@pytest.fixture
def response_dir(tmp_path):
    d = tmp_path / "responses"
    d.mkdir()
    return d

def expected_paths(respdir, diffreq):
    return (
        Path(
            respdir
            / diffreq.dirname()
            / diffreq.content_type.as_dir_name()
            / diffreq.file_id_one()
        ),
        Path(
            respdir
            / diffreq.dirname()
            / diffreq.content_type.as_dir_name()
            / diffreq.file_id_two(),
        ),
    )

def expected_udiff_path(respdir, diffreq):
    return Path(
            respdir
            / diffreq.dirname()
            / diffreq.content_type.as_dir_name()
            / f"{diffreq.common_name()}{DIFF_PATCH_FILENAME_SUFFIX}")

class TestDiff:
    def test_dirpath_json(self, response_dir, diff_request_json, diff_response_json, diffconfig):
        expected_dir = Path(
            response_dir
            / diff_request_json.dirname()
            / diff_request_json.content_type.as_dir_name()
        )
        diff = Diff(response_dir, diff_request_json, diff_response_json, diffconfig)
        actual_dir = diff.dirpath()
        assert(expected_dir == actual_dir)

    def test_htmldiff_path_json(self, response_dir, diff_request_json, diff_response_json, diffconfig):
        expected_path = Path(
            response_dir
            / diff_request_json.dirname()
            / diff_request_json.content_type.as_dir_name()
            / f"{diff_request_json.common_name()}{DIFF_HTML_FILENAME_SUFFIX}"
        )
        diff = Diff(response_dir, diff_request_json, diff_response_json, diffconfig)
        actual_path = diff.htmldiff_path()
        assert(expected_path == actual_path)

    def test_dirpath_xml(self, response_dir, diff_request_xml, diff_response_xml, diffconfig):
        expected_dir = Path(
            response_dir
            / diff_request_xml.dirname()
            / diff_request_xml.content_type.as_dir_name()
        )
        diff = Diff(response_dir, diff_request_xml, diff_response_xml, diffconfig)
        actual_dir = diff.dirpath()
        assert(expected_dir == actual_dir)

    def test_htmldiff_path_xml(self, response_dir, diff_request_xml, diff_response_xml, diffconfig):
        expected_path = Path(
            response_dir
            / diff_request_xml.dirname()
            / diff_request_xml.content_type.as_dir_name()
            / f"{diff_request_xml.common_name()}{DIFF_HTML_FILENAME_SUFFIX}"
        )
        diff = Diff(response_dir, diff_request_xml, diff_response_xml, diffconfig)
        actual_path = diff.htmldiff_path()
        assert(expected_path == actual_path)

    def test_filepaths_json(self, response_dir, diff_request_json, diff_response_json, diffconfig):
        expected_one, expected_two = expected_paths(response_dir, diff_request_json)
        diff = Diff(response_dir, diff_request_json, diff_response_json, diffconfig)
        path_one, path_two = diff.filepaths()
        assert(expected_one == path_one)
        assert(expected_two == path_two)

    def test_save_responses_json(self, response_dir, diff_request_json, diff_response_json, diffconfig):
        diff = Diff(response_dir, diff_request_json, diff_response_json, diffconfig)
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
        unexpected_udiff_file = expected_udiff_path(response_dir, diff_request_json)
        assert(not unexpected_udiff_file.exists())

    def test_unified_diff(self, response_dir, diff_request_json, diff_response_json, diffconfig):
        diffconfig.patch = True
        diff = Diff(response_dir, diff_request_json, diff_response_json, diffconfig)
        diff.save()
        expected_udiff_file = expected_udiff_path(response_dir, diff_request_json)
        assert(expected_udiff_file.exists())


class TestSummary:
    @pytest.fixture
    def json_diff_requests(self, local_url, remote_url, none_params):
        version_req_one = Request(
            base_url=local_url,
            endpoint="version",
            id="different",
            params=none_params,
            content_type=ContentType.JSON
        )
        version_req_two = Request(
            base_url=remote_url,
            endpoint="version",
            id="different",
            params=none_params,
            content_type=ContentType.JSON
        )
        address_req_one = Request(
            base_url=local_url,
            endpoint="address",
            id="same",
            params=none_params,
            content_type=ContentType.JSON
        )
        address_req_two = Request(
            base_url=remote_url,
            endpoint="address",
            id="same",
            params=none_params,
            content_type=ContentType.JSON
        )
        reqs = {}
        reqs["different_requests_json"] = DiffRequest(
            request_one=version_req_one,
            request_two=version_req_two,
            date_stamp=FIXTURE_DATE_STAMP,
            content_type=ContentType.JSON
        )
        reqs["same_requests_json"] = DiffRequest(
            request_one=address_req_one,
            request_two=address_req_two,
            date_stamp=FIXTURE_DATE_STAMP,
            content_type=ContentType.JSON
        )
        return reqs

    @pytest.fixture
    def xml_diff_requests(self, local_url, remote_url, none_params):
        version_req_one = Request(
            base_url=local_url,
            endpoint="version",
            id="different",
            params=none_params,
            content_type=ContentType.XML
        )
        version_req_two = Request(
            base_url=remote_url,
            endpoint="version",
            id="different",
            params=none_params,
            content_type=ContentType.XML
        )
        address_req_one = Request(
            base_url=local_url,
            endpoint="address",
            id="same",
            params=none_params,
            content_type=ContentType.XML
        )
        address_req_two = Request(
            base_url=remote_url,
            endpoint="address",
            id="same",
            params=none_params,
            content_type=ContentType.XML
        )
        reqs = {}
        reqs["different_requests_xml"] = DiffRequest(
            request_one=version_req_one,
            request_two=version_req_two,
            date_stamp=FIXTURE_DATE_STAMP,
            content_type=ContentType.XML
        )
        reqs["same_requests_xml"] = DiffRequest(
            request_one=address_req_one,
            request_two=address_req_two,
            date_stamp=FIXTURE_DATE_STAMP,
            content_type=ContentType.XML
        )
        return reqs

    @pytest.fixture
    def diffs(self, json_diff_requests, xml_diff_requests) -> DiffResponse:
        # json_files is from this module's __init__.py
        different_json_fls = json_files("version", True)
        different_responses_json = DiffResponse(
                content_type=ContentType.JSON,
                response_one=different_json_fls[0],
                response_two=different_json_fls[1])
        same_json_fls = json_files("address", False)
        same_responses_json = DiffResponse(
                content_type=ContentType.JSON,
                response_one=same_json_fls[0],
                response_two=same_json_fls[1])
        # xml_files is from this module's __init__.py
        different_xml_fls = xml_files("version", True)
        different_responses_xml = DiffResponse(
                content_type=ContentType.XML,
                response_one=different_xml_fls[0],
                response_two=different_xml_fls[1])
        same_xml_fls = xml_files("address", False)
        same_responses_xml = DiffResponse(
                content_type=ContentType.XML,
                response_one=same_xml_fls[0],
                response_two=same_xml_fls[1])
        diffs = {}
        response_dir = FIXTURE_DIR
        log.info(f"response_dir: {type(response_dir)}")
        diffs["different_diff_json"] = Diff(
            response_dir=response_dir,
            diff_request=json_diff_requests["different_requests_json"],
            diff_response=different_responses_json,
            diff_config=DiffConfig(patch=False, short=True))
        diffs["same_diff_json"] = Diff(
            response_dir=response_dir,
            diff_request=json_diff_requests["same_requests_json"],
            diff_response=same_responses_json,
            diff_config=DiffConfig(patch=False, short=True))
        diffs["different_diff_xml"] = Diff(
            response_dir=response_dir,
            diff_request=xml_diff_requests["different_requests_xml"],
            diff_response=different_responses_xml,
            diff_config=DiffConfig(patch=False, short=True))
        diffs["same_diff_xml"] = Diff(
            response_dir=response_dir,
            diff_request=xml_diff_requests["same_requests_xml"],
            diff_response=same_responses_xml,
            diff_config=DiffConfig(patch=False, short=True))
        return diffs

    def test_summarize(self, response_dir, diffs):
        diff_list = [diffs["different_diff_json"], diffs["same_diff_json"], diffs["different_diff_xml"], diffs["same_diff_xml"]]
        summary = Summary(response_dir, diff_list)
        html = summary.summarize()
        assert(f"<title>{FIXTURE_DATE_STAMP}</title>" in html)
        assert(summary._css() in html)
        different_json_link = summary._link(diffs["different_diff_json"])
        assert(different_json_link in html)
        same_json_link = summary._link(diffs["same_diff_json"])
        assert(same_json_link not in html)
        different_xml_link = summary._link(diffs["different_diff_xml"])
        assert(different_xml_link in html)
        same_xml_link = summary._link(diffs["same_diff_xml"])
        assert(same_xml_link not in html)
