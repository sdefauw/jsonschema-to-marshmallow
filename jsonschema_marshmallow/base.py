import re

from jsonschema.validators import Draft7Validator
from marshmallow import validate, fields, Schema
from marshmallow_oneofschema import OneOfSchema


def enum_validator(**kwargs):
    validator = validate.OneOf(
        choices=kwargs.get('enum'),
        labels=kwargs.get('enumNames')
    )
    del kwargs['enum']
    del kwargs['enumNames']
    return 'validate', validator


def pattern_validator(**kwargs):
    validator = validate.Regexp(re.compile(kwargs['pattern']))
    del kwargs['pattern']
    return 'validate', validator


TYPE_MAPPING = {
    ('string', None): fields.String,
    ('string', 'uuid'): fields.UUID,
    ('string', 'date'): fields.Date,
    ('string', 'date-time'): fields.DateTime,
    ('number', None): fields.Number,
    ('number', 'decimal'): fields.Decimal,
    ('number', 'float'): fields.Float,
    ('integer', None): fields.Integer,
    ('boolean', None): fields.Boolean,
    ('object', None): fields.Nested,
    ('array', None): fields.List,
}
FIELD_MAPPING = {
    'required': 'required',
    'readOnly': 'dump_only',
    'default': 'dump_default',
    'enum': enum_validator,
    'pattern': pattern_validator,
}
SKIP_FIELD = ("$ref", 'items')


class MarshmallowJsonSchema:

    def __init__(self, schema):
        self.json_schema = Draft7Validator(schema).schema

    def _field_arguments(self, type, **kwargs):
        # TODO improve with more fields
        d = {}
        metadata = {}
        for key, value in kwargs.items():
            if key in SKIP_FIELD:
                continue
            new_key = FIELD_MAPPING.get(key)
            if not new_key:
                metadata[key] = value
            elif isinstance(new_key, str):
                d[new_key] = value
            else:
                k, v = new_key(**kwargs)
                d[k] = v
        if metadata:
            d['metadata'] = metadata
        print("F2F", d)
        return d

    def _field_argument_type(self, schema, type, **kwargs):

        if type == 'array':
            items = kwargs.get('items')
            ref = items.get("$ref")
            if ref:
                return [fields.Nested(self._get_object(ref, schema))]

        ref = kwargs.get("$ref")
        if ref:
            return [self._get_object(ref=ref, schema=schema)]
        return []

    def _get_marsmallow_type(self, content, *args, **kwargs):
        if content.get('const'):
            # TODO
            return fields.Constant(content.get('const'))
        return TYPE_MAPPING[(content['type'], content.get('format'))](
            *args,
            **kwargs
        )

    def _get_object(self, schema, ref=None, obj=None):

        if ref:
            ref_link = ref.split('/')
            if ref_link[0] != '#':
                raise NotImplementedError()

            obj = schema
            for p in ref_link[1:]:
                obj = obj.get(p)

        if obj.get('type') != "object":
            raise NotImplementedError()

        one_of = obj.get('oneOf')
        if one_of:
            return type(f"OneOfSchema", (OneOfSchema,), {
                "type_schemas": {
                    "TODO": self._get_object(
                        schema=schema,
                        obj=sch
                    )
                    for sch in one_of
                }
            })

        required = obj.get('required', [])

        # TODO support const
        return type(f"{ref_link[-1] if ref else obj.get('title')}", (Schema,), {
            name: self._get_marsmallow_type(
                content,
                *self._field_argument_type(schema, **content),
                **self._field_arguments(required=(name in required), **content)
            )
            for name, content in obj.get('properties').items() if content.get('type')
        })

    def load(self):
        return self._get_object(
            ref=self.json_schema.get('$ref'),
            obj=self.json_schema,
            schema=self.json_schema
        )
