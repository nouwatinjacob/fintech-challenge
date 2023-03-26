from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(max=50))
    last_name = fields.String(required=True, validate=validate.Length(max=50))
    email = fields.Email(required=True)
    phone_number = fields.String(required=True, validate=validate.Length(max=20))
    password = fields.String(required=True, validate=validate.Length(max=120))
