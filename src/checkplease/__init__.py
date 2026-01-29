from pathlib import Path

from . import config, io
from ._version import __version__

__all__ = [
    '__version__',
    'app',
    'config',
    'constants',
    'content_type',
    'diff',
    'io',
    'requests',
    'rest_client'
]

import logging
import sys


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr
)
log = logging.getLogger(__name__)
log.info("%s initialized.", log)


def load_config():
    config_file_path = Path(__file__).parent / "config.yaml"
    data = io.load_yaml_file(config_file_path)
    return config.load_config(data)
