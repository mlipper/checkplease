"""Encapsulates the diff of the responses from two REST requests."""

import sys
#import filecmp
import difflib
from difflib import HtmlDiff
from pathlib import Path

from checkplease import io
from checkplease.config import DiffConfig
from checkplease.constants import DIFF_HTML_FILENAME_SUFFIX, DIFF_PATCH_FILENAME_SUFFIX
from checkplease.content_type import ContentType
from checkplease.requests import DiffRequest
from checkplease.rest_client import DiffResponse

"""
In addition holding references to the DiffRequest/DiffResponse pair, the
Diff class is responsible for naming and saving the responses to files.
"""
class Diff:
    def __init__(
        self, response_dir: Path, diff_request: DiffRequest, diff_response: DiffResponse, diff_config: DiffConfig
    ):
        self.response_dir = response_dir
        self.diff_request = diff_request
        self.diff_response = diff_response
        self.diff_config = diff_config

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

    def unified_diff_path(self) -> Path:
        return Path(
            self.dirpath() / f"{self.diff_request.common_name()}{DIFF_PATCH_FILENAME_SUFFIX}"
        )

    def save(self) -> None:
        self.save_responses()
        differ = HtmlDiff()
        self.save_htmldiff(differ)
        if self.diff_config.patch:
            self.save_unified_diff()

    def save_unified_diff(self) -> None:
        file_one, file_two = self.filepaths()
        lines_of_file_one = io.readlines_from_file(file_one)
        lines_of_file_two = io.readlines_from_file(file_two)
        udiff = difflib.unified_diff(lines_of_file_one, lines_of_file_two, fromfile=file_one.name, tofile=file_two.name)
        udiff_path = self.unified_diff_path()
        io.writelines(udiff, udiff_path)

    def save_htmldiff(self, differ: HtmlDiff) -> int:
        file_one, file_two = self.filepaths()
        lines_of_file_one = io.readlines_from_file(file_one)
        lines_of_file_two = io.readlines_from_file(file_two)
        html_diff = differ.make_file(
            lines_of_file_one,
            lines_of_file_two,
            fromdesc=file_one.name,
            todesc=file_two.name,
            context=self.diff_config.short,
        )
        diff_path = self.htmldiff_path()
        return io.write_string_to_file(html_diff, diff_path)

    def htmldiff_table(self, differ: HtmlDiff) -> str:
        file_one, file_two = self.filepaths()
        lines_of_file_one = io.readlines_from_file(file_one)
        lines_of_file_two = io.readlines_from_file(file_two)
        html_table = differ.make_table(
            lines_of_file_one,
            lines_of_file_two,
            fromdesc=file_one.name,
            todesc=file_two.name,
            context=self.diff_config.short,
        )
        return html_table

    def save_responses(self) -> None:
        file_one, file_two = self.filepaths()
        if self.diff_request.content_type == ContentType.JSON:
            io.save_json_response(self.diff_response.response_one, file_one)
            io.save_json_response(self.diff_response.response_two, file_two)
        else:
            io.save_xml_response(self.diff_response.response_one, file_one)
            io.save_xml_response(self.diff_response.response_two, file_two)

class FileContext:
    def __init__(self, file_one: Path, file_two: Path):
        self.file_one = file_one
        self.file_two = file_two
        self.lines_file_one = None
        self.lines_file_two = None

    def lines_of_file_one(self) -> list[str]:
        if self.lines_file_one is None:
            self.lines_file_one = io.readlines_from_file(self.file_one)
        return self.lines_file_one

    def lines_of_file_two(self) -> list[str]:
        if self.lines_file_two is None:
            self.lines_file_two = io.readlines_from_file(self.file_two)
        return self.lines_file_two

    def name_of_file_one(self) -> str:
        return self.file_one.name

    def name_of_file_two(self) -> str:
        return self.file_two.name

class Summary:

    def __init__(self):
        self.tables = list()
        self.diff_files = list()

    def add(self, table: str, diff_file: Path) -> None:
        self.tables.append(table)
        self.diff_files.append(diff_file)

    def summarize(self) -> str:
        html = self.body_begin
        for t in self.tables:
            html = html + t
        html = html + self.body_end
        return html

    def body_begin(self) -> str:
        return """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>

<head>
    <meta http-equiv="Content-Type"
          content="text/html; charset=utf-8" />
    <title></title>
    <style type="text/css">
        :root {color-scheme: light dark}
        table.diff {font-family: Menlo, Consolas, Monaco, Liberation Mono, Lucida Console, monospace; border:medium}
        .diff_header {background-color:#e0e0e0}
        td.diff_header {text-align:right}
        .diff_next {background-color:#c0c0c0}
        .diff_add {background-color:palegreen}
        .diff_chg {background-color:#ffff77}
        .diff_sub {background-color:#ffaaaa}

        @media (prefers-color-scheme: dark) {
            .diff_header {background-color:#666}
            .diff_next {background-color:#393939}
            .diff_add {background-color:darkgreen}
            .diff_chg {background-color:#847415}
            .diff_sub {background-color:darkred}
        }
    </style>
</head>

<body>
"""

    def body_end(self) -> str:
        return """
</body>
"""