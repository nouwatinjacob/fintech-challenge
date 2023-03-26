from flask import request
from flask_restful import Resource
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models.account import AccountModel
from ..schemas.account import AccountSchema
from ..utils.auth import auth_required

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)

class AccountResource(Resource):
    @auth_required
    def get(self, account_id=None):
        if account_id:
            account = AccountModel.query.filter_by(id=account_id).first()
            if not account:
                return {'message': 'Account not found'}, HTTPStatus.NOT_FOUND
            return account_schema.dump(account), HTTPStatus.OK
        else:
            accounts = AccountModel.query.all()
            return accounts_schema.dump(accounts), HTTPStatus.OK

    @auth_required
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, HTTPStatus.BAD_REQUEST

        try:
            account = account_schema.load(json_data)
            account.save_to_db()
            return account_schema.dump(account), HTTPStatus.CREATED
        except IntegrityError as e:
            return {'message': 'Account with name already exists'}, HTTPStatus.CONFLICT

    @auth_required
    def put(self, account_id):
        account = AccountModel.query.filter_by(id=account_id).first()
        if not account:
            return {'message': 'Account not found'}, HTTPStatus.NOT_FOUND

        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, HTTPStatus.BAD_REQUEST

        try:
            account = account_schema.load(json_data)
            account.id = account_id
            account.save_to_db()
            return account_schema.dump(account), HTTPStatus.OK
        except IntegrityError as e:
            return {'message': 'Account with name already exists'}, HTTPStatus.CONFLICT

    @auth_required
    def delete(self, account_id):
        account = AccountModel.query.filter_by(id=account_id).first()
        if not account:
            return {'message': 'Account not found'}, HTTPStatus.NOT_FOUND

        account.delete_from_db()
        return '', HTTPStatus.NO_CONTENT
