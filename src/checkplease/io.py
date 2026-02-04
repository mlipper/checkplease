import json
import yaml
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from checkplease.constants import FORMAT_JSON_INDENT, FORMAT_XML_STRING

def load_json_file(filepath: str) -> Any:
    with open(filepath, 'r') as f:
        return json.load(f)

def load_yaml_file(filepath: str) -> Any:
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def readlines_from_file(filepath: str) -> list[str]:
    with open(filepath, 'r') as f:
        return f.readlines()

def save_json_response(response, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding=response.apparent_encoding) as f:
        json.dump(response.json(), f, indent=FORMAT_JSON_INDENT)

def save_xml_response(response, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    root = ET.fromstring(response.text)
    ET.indent(root, space=FORMAT_XML_STRING)
    ET.ElementTree(root).write(filepath, encoding=response.apparent_encoding, xml_declaration=False)

def write_string_to_file(content: str, filepath: Path) -> int:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        return f.write(content)