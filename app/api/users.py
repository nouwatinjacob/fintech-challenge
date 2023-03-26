from flask import request
from flask_restful import Resource
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flasgger import swag_from

from ..models.user import UserModel
from ..schemas.user import UserSchema
from ..utils.auth import auth_required


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UsersResource(Resource):
    @auth_required
    @swag_from('yml')
    def get(self, user_id=None):
        if user_id:
            user = UserModel.query.filter_by(id=user_id).first()
            if not user:
                return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
            return user_schema.dump(user), HTTPStatus.OK
        else:
            users = UserModel.query.all()
            return users_schema.dump(users), HTTPStatus.OK

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, HTTPStatus.BAD_REQUEST

        try:
            user = user_schema.load(json_data)
            user.save_to_db()
            return user_schema.dump(user), HTTPStatus.CREATED
        except IntegrityError as e:
            return {'message': 'User with email already exists'}, HTTPStatus.CONFLICT

    def put(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, HTTPStatus.BAD_REQUEST

        try:
            user = user_schema.load(json_data)
            user.id = user_id
            user.save_to_db()
            return user_schema.dump(user), HTTPStatus.OK
        except IntegrityError as e:
            return {'message': 'User with email already exists'}, HTTPStatus.CONFLICT

    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        user.delete_from_db()
        return '', HTTPStatus.NO_CONTENT
