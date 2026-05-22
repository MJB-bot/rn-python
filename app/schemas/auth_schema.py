from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class LoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    password = fields.String(required=True, validate=validate.Length(min=1, max=255))


class LoginResponseSchema(Schema):
    token = fields.String()
    admin = fields.Dict()
