from pathlib import Path


FIXTURE_DIR = Path(__file__).parent / 'files'
FIXTURE_DATE_STAMP = "20260402"
JSON_FIXTURE_DIR = FIXTURE_DIR / FIXTURE_DATE_STAMP / 'json'
XML_FIXTURE_DIR = FIXTURE_DIR / FIXTURE_DATE_STAMP / 'xml'

def fixture_date_stamp():
    return FIXTURE_DATE_STAMP

def json_files(location_type: str, different: bool) -> Path:
    prefix = "different" if different else "same"
    return (Path(JSON_FIXTURE_DIR) / f"{prefix}-{location_type}-1.json",
            Path(JSON_FIXTURE_DIR) / f"{prefix}-{location_type}-2.json")

def xml_files(location_type: str, different: bool) -> Path:
    prefix = "different" if different else "same"
    return (Path(XML_FIXTURE_DIR) / f"{prefix}-{location_type}-1.xml",
            Path(XML_FIXTURE_DIR) / f"{prefix}-{location_type}-2.xml")
