from pkg_resources import get_distribution

__version__ = get_distribution("jsonschema-to-marshmallow").version
__license__ = "MIT"

from .base import MarshmallowJsonSchema
