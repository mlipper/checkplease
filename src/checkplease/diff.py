"""Encapsulates the diff of the responses from two REST requests."""

from difflib import HtmlDiff
from pathlib import Path

from checkplease import io
from checkplease.constants import DIFF_HTML_FILENAME_SUFFIX
from checkplease.content_type import ContentType
from checkplease.requests import DiffRequest
from checkplease.rest_client import DiffResponse

"""
In addition holding references to the DiffRequest/DiffResponse pair, the
Diff class is responsible for naming and saving the responses to files.
"""
class Diff:
    def __init__(
        self, response_dir: Path, diff_request: DiffRequest, diff_response: DiffResponse
    ):
        self.response_dir = response_dir
        self.diff_request = diff_request
        self.diff_response = diff_response

    def dirpath(self) -> Path:
        return Path(
            self.response_dir
            / self.diff_request.content_type.as_dir_name()
            / self.diff_request.dirname()
        )

    def filepaths(self) -> tuple[Path, Path]:
        return (
            Path(self.dirpath() / self.diff_request.file_id_one()),
            Path(self.dirpath() / self.diff_request.file_id_two()),
        )

    def htmldiff_path(self) -> Path:
        return Path(
            self.dirpath() / f"{self.diff_request.common_name()}{DIFF_HTML_FILENAME_SUFFIX}"
        )

    def save(self) -> None:
        self.save_responses()
        self.save_htmldiff()

    def save_htmldiff(self) -> int:
        file_one, file_two = self.filepaths()
        lins_of_file_one = io.readlines_from_file(file_one)
        lins_of_file_two = io.readlines_from_file(file_two)
        differ = HtmlDiff()
        html_diff = differ.make_file(
            lins_of_file_one,
            lins_of_file_two,
            fromdesc=file_one.name,
            todesc=file_two.name,
        )
        diff_path = self.htmldiff_path()
        return io.write_string_to_file(html_diff, diff_path)

    def save_responses(self) -> None:
        file_one, file_two = self.filepaths()
        if self.diff_request.content_type == ContentType.JSON:
            io.save_json_response(self.diff_response.response_one, file_one)
            io.save_json_response(self.diff_response.response_two, file_two)
        else:
            io.save_xml_response(self.diff_response.response_one, file_one)
            io.save_xml_response(self.diff_response.response_two, file_two)
