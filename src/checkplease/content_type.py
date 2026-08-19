from enum import Enum
from checkplease.constants import DEFAULT_PATH_SUFFIX

class ContentType(Enum):
    JSON = "JSON"
    XML = "XML"

    @classmethod
    def from_string(cls, s):
        for member in cls:
            if member.value == s:
                return member
        raise ValueError(f"'{s}' is not a valid ContentType")

    def as_dir_name(self) -> str:
        return self.value.lower()

    def as_uri_path(self) -> str:
        if self == ContentType.JSON:
            return DEFAULT_PATH_SUFFIX
        else:
            return f".{self.value.lower()}"

    def as_file_extension(self) -> str:
        return f".{self.value.lower()}"