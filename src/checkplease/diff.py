"""Encapsulates the diff of the responses from two REST requests."""

import filecmp
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

    def identical(self) -> bool:
        file_one, file_two = self.filepaths()
        return filecmp.cmp(file_one, file_two)

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

class Summary:

    def __init__(self, response_dir: Path, diffs: list[Diff]):
        self.response_dir = response_dir
        self.diffs = diffs

    def summarize(self) -> str:
        #different = [d for d in self.diffs if not d.identical()]
        different = []
        for d in self.diffs:
            if not d.identical():
                different.append(d)
        json_section = self.section(different, ContentType.JSON)
        xml_section = self.section(different, ContentType.XML)
        html = self._html(self._css(), self.response_dir.name, json_section + xml_section)
        io.write_string_to_file(html, self.response_dir / "index.html")
        return html

    def _link(self, diff: Diff) -> str:
        relative_path = diff.htmldiff_path().relative_to(diff.response_dir)
        txt = f'<a href="{relative_path}">{diff.htmldiff_path().stem}</a>'
        return txt

    def _html(self, css: str, title: str, sections: str) -> str:
        return f"""
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>{title}</title>
    <style type="text/css">
    {css}
    </style>
</head>
<body class="diff">
    <h1>Differences</h1>
    <div>
    {sections}
    </div>
</body>
</html>
"""

    def _css (self) -> str:
        return """
        :root {color-scheme: light dark}
        .diff {font-family: Menlo, Consolas, Monaco, Liberation Mono, Lucida Console, monospace; border:medium}

        @media (prefers-color-scheme: dark) {}"""

    def section(self, diffs: list[Diff], filter: ContentType) -> str:
        section = f"""
<h2>{filter.value}</h2>
<div>
<ul>
"""
        for d in diffs:
            if d.diff_request.content_type == filter:
                section = section + f"<li>{self._link(d)}</li>"
        section = section + """
</ul>
</div>
"""
        return section
