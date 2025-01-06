# JsonSchema to Marshmallow
jsonschema-to-marshmallow translates JSON Schema to Marshmallow class.

### Simple Example
```python
from jsonschema_marshmallow import MarshmallowJsonSchema

json_schema = {
  "type": "object",
  "properties": {
    "price": {
      "type": "number"
    },
    "name": {
      "type": "string"
    }
  }
}
Schema = MarshmallowJsonSchema(json_schema).load()

Schema().dump({'name': 'john'})
```
