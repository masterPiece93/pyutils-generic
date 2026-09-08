"""
An Exerpt from an Api Server

What to demonstrate ?

    - when we are writing an API we might need to add
        schema for query-param & path-param along with
        api-body

    - hence , we'll have all the codes organised at a single place
"""

from dataclasses import dataclass
from pyutils_generic.typecheck import TypeCheck
from typing import Any, List, Optional
from enum import Enum


class BadRequest(Exception):
    def __init__(self, errors=[dict()], custom_message=None, code=None):
        self.http_status_code: int = 400
        self.code: Enum = code
        self.errors: List[Any] = errors
        if custom_message:
            self.message: str = custom_message
        else:
            self.message: str = "Invalid Api Request"
        super().__init__(self.message)


class ValidationHandler:

    def __init__(self, schema_name):
        
        self.schema_name = schema_name
        self.message = "Invalid {name}"
        self.request_body_schema = {
            "age":          "AGE_RESTRICTIONS",
            "username":     "USERNAME_COMPLIANCE",
            "firstname":    "NAME_COMPLIANCE",
            "lastname":     "NAME_COMPLIANCE"
        } # TODO : in case we support multiple validators in future , we must specify <field>_<purpose>
        self.query_param_schema = {
            "filters":  "FILTER_COMPLIANCE",
            "q":        "SEARCH_COMPLIANCE"        
        }
        self.path_param_schema = {
            "date": "DATE_FORMAT_ERR"
        }

    def __call__(self, name, value, validation_name ):
        
        validation_id = validation_name.rstrip("_validator")
        raise BadRequest(
                custom_message=self.message.format(name),
                errors=[f"{value} provided must be checked"],
                code=getattr(self, self.schema_name)[validation_id]
            )

def type_check_failure_handler(name, current_type, expected_type):

        raise BadRequest(
            custom_message=f"Invalid {name}",
            errors=[
                f"Invalid Type for field - `{name}`, expected - `{expected_type}`, but got - `{current_type}`"
            ],
            code="TYPE-ERR"
        )


@dataclass(frozen=True)
class RequestBodySchema(TypeCheck):

    username: str
    firstname: str
    lastname: str
    email: str
    created_by: int
    age : Optional[int] = None

    # Constants
    MAX_AGE = 25
    
    # Field Validators
    username_validator = lambda value: value.islower()
    firstname_validator = lastname_validator = lambda value: ' ' not in value
    age_validator = lambda value: value < RequestBodySchema.MAX_AGE if value else True

    # Exceptions
    validator_exception = ValidationHandler("request_body_schema")
    type_exception = type_check_failure_handler


if __name__ == "__main__":

    data = {
        "username": "anki8290",
        "firstname": "ankit",
        "lastname": "kumar",
        "email": "ankit8290@gmail.com",
        "created_by": 7,
        "age": 25
    }

    validated_data = RequestBodySchema(**data)

    # exception will be caught by your global exception handler