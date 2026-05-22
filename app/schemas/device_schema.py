from marshmallow import Schema, fields, validate


class DeviceSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': '设备名称不能为空'}
    )
    model = fields.String(load_default=None, validate=validate.Length(max=100))
    category_id = fields.Integer(
        required=True,
        error_messages={'required': '分类ID不能为空'}
    )


class DeviceUpdateSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    model = fields.String(load_default=None, validate=validate.Length(max=100))
    category_id = fields.Integer(required=True)


class DeviceQuerySchema(Schema):
    page = fields.Integer(load_default=1, validate=validate.Range(min=1))
    page_size = fields.Integer(load_default=10, validate=validate.Range(min=1, max=100))
    category_id = fields.Integer(load_default=None)
    name = fields.String(load_default=None)
