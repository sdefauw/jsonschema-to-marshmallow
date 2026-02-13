from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("jsonschema-to-marshmallow")
except PackageNotFoundError:  # pragma: no cover
    # Not installed (e.g., running from source checkout)
    __version__ = "0.0.0"

__license__ = "MIT"

from .base import MarshmallowJsonSchema

__all__ = ["MarshmallowJsonSchema", "__version__", "__license__"]
