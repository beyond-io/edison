
from flask_jwt_extended import jwt_required, get_jwt_identity
from edison import db, app
import edison.models as models

from flask_restful import Resource, reqparse


class NewPolicy(Resource):
    # RequestParser enforces arguments in requests.
    # If one of the arguments not exists, client gets an error response.
    parser = reqparse.RequestParser()
    parser.add_argument(
        'policy_name',
        type=str,
        required=True
    )
    parser.add_argument(
        'room',
        type=str,
        required=True
    )
    parser.add_argument(
        'conditions',
        type=str,
        required=True
    )
    parser.add_argument(
        'commands',
        type=str,
        required=True
    )

    @jwt_required
    def post(self):
        data = NewPolicy.parser.parse_args()
        status = 200
        response = {}
        username = get_jwt_identity()
        current_user = models.User.query.filter_by(username=username).first()
        policy_to_add = models.Policy(**data, user_id=current_user.id)
        filters = {'policy_name': data['policy_name'], 'user_id': current_user.id}

        if models.Policy.query.filter_by(**filters).first() is None:
            try:
                policy_to_add = models.Policy(**data, user_id=current_user.id)
                db.session.add(policy_to_add)
                db.session.commit()

                response = {'msg': 'policy added successfully'}

            except KeyError:
                response = {'msg': 'Update failed. Json missing keys.'}
                status = 400

        else:
            status = 400
            response = {'msg': f"User {username} already have policy named {data['policy_name']}"}

        return response, status

    def __request_is_legal(self, username: str):
        return get_jwt_identity() == username