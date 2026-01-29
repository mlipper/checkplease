"""Encapsulates the diff of the responses from two REST requests."""

from pathlib import Path

from checkplease import io
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

    def filepaths(self) -> tuple[Path, Path]:
        return (
            Path(
                self.response_dir
                / self.diff_request.content_type.as_dir_name()
                / self.diff_request.dirname()
                / self.diff_request.file_id_one()
            ),
            Path(
                self.response_dir
                / self.diff_request.content_type.as_dir_name()
                / self.diff_request.dirname()
                / self.diff_request.file_id_two()
            ),
        )

    def save_responses(self) -> None:
        file_one, file_two = self.filepaths()
        if self.diff_request.content_type == ContentType.JSON:
            io.save_json_response(self.diff_response.response_one, file_one)
            io.save_json_response(self.diff_response.response_two, file_two)
        else:
            io.save_xml_response(self.diff_response.response_one, file_one)
            io.save_xml_response(self.diff_response.response_two, file_two)
