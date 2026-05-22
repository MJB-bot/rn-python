from marshmallow import Schema, fields, validate, validates, ValidationError
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


class EmployeeSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=20),
        error_messages={'required': '姓名不能为空', 'invalid': '姓名长度1~20'}
    )
    age = fields.Integer(
        required=True,
        validate=validate.Range(min=18, max=60),
        error_messages={'required': '年龄不能为空', 'invalid': '年龄范围18~60'}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式不正确'}
    )

    @validates('email')
    def validate_email_format(self, value, **kwargs):
        if not EMAIL_REGEX.match(value):
            raise ValidationError('邮箱格式不正确')


class EmployeeUpdateSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=20)
    )
    age = fields.Integer(
        required=True,
        validate=validate.Range(min=18, max=60)
    )
    email = fields.Email(required=True)

    @validates('email')
    def validate_email_format(self, value, **kwargs):
        if not EMAIL_REGEX.match(value):
            raise ValidationError('邮箱格式不正确')


class EmployeeQuerySchema(Schema):
    page = fields.Integer(load_default=1, validate=validate.Range(min=1))
    page_size = fields.Integer(load_default=10, validate=validate.Range(min=1, max=100))
    name = fields.String(load_default=None)
