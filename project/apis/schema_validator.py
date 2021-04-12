#<==================================================================================================>
#                                         IMPORTS
#<==================================================================================================>
from jsonschema import validate
from jsonschema.exceptions import SchemaError
from jsonschema.exceptions import ValidationError


#<==================================================================================================>
#                                 CREATE GAME SCHEMA
#<==================================================================================================>
create_game_schema = {
    "type": "object",
    "properties": {
        "players": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "columns": {
            "type": "integer",
            "minimum": 4,
            "maximum": 4
        },
        "rows": {
            "type": "integer",
            "minimum": 4,
            "maximum": 4
        },
    },
    "required": ["players", "columns", "rows"],
    "additionalProperties": False
}

def validate_game_schema(data):
    try:
        validate(instance=data, schema=create_game_schema)
    except ValidationError as e:
        return {'result': False, 'error': e.message}
    except SchemaError as e:
        return {'result': False, 'error': e.message}
    return {'result': True, 'data': data}


#<==================================================================================================>
#                                        MOVES SCHEMA
#<==================================================================================================>
moves_schema = {
    "type": "object",
    "properties": {
        "column": {
            "type": "integer",
            "minimum": 0,
            "maximum": 3
        },
    },
    "required": ["column"],
    "additionalProperties": False
}

def validate_move_schema(data):
    try:
        validate(instance=data, schema=moves_schema)
    except ValidationError as e:
        return {'result': False, 'error': e.message}
    except SchemaError as e:
        return {'result': False, 'error': e.message}
    return {'result': True, 'data': data}