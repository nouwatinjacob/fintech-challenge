from marshmallow import fields, Schema


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    amount = fields.Float(required=True)
    date = fields.DateTime(required=True)
    account_id = fields.Int(dump_only=True)


class AccountSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    user_id = fields.Int(dump_only=True)
    transactions = fields.Nested(TransactionSchema, many=True, dump_only=True)
