from flask import Flask, request, jsonify
import sys
import json
import os
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from DataBaseConnector import DataBaseConnector
from preference import Preference
from User_token import User_token
import Crawler
from preference import PreferenceEncoder
import push_notification
from PasswordChecher import PasswordChecher

app = Flask(__name__)

db = DataBaseConnector()
pw_checker = PasswordChecher(db)

jwt = JWTManager()

# 設定 JWT 密鑰
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt.init_app(app)


@app.route('/api/v1/signUp', methods=['POST'])
def sign_up():
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    hashed_pw = pw_checker.hash_password(password).decode('utf-8')
    phone = request.json.get('phone', None)

    if db.get_user_id(email) is None:
        user_id = db.register_user(username, email, hashed_pw, phone)

        if user_id is not None:
            ret = {
                'access_token': create_access_token(identity=user_id),
                'refresh_token': create_refresh_token(identity=user_id),
                'user_id': user_id
            }
            return jsonify(ret), 200
        else:
            return jsonify({'error': "some user info missing."}), 400

    else:
        return jsonify({'error': "email already registed."}), 400

@app.route('/api/v1/login', methods=['POST'])
def login():
    email = str(request.json.get('email', None))
    password = str(request.json.get('password', None))

    user_id = pw_checker.check(email, password)

    if user_id is not None:
        # Use create_access_token() and create_refresh_token() to create our
        # access and refresh tokens
        ret = {
            'access_token': create_access_token(identity=user_id),
            'refresh_token': create_refresh_token(identity=user_id)
        }
        return jsonify(ret), 200
    else:
        return jsonify({'error': "user not found or password incorrect."}), 400


@app.route('/api/v1/refreshUpdate', methods=['POST'])
@jwt_refresh_token_required
def refresh_update():
    current_user = get_jwt_identity()
    ret = {
        'refresh_token': create_refresh_token(identity=current_user)
    }
    return jsonify(ret), 200


@app.route('/api/v1/access', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@app.route('/', methods=['POST'])
@jwt_required
def index():
    current_user = get_jwt_identity()
    return f"Hello, World! {current_user}"


# @app.route('/api/v1/user/token', methods=['GET'])
def fetch_user_token(user_id: str):
    token = db.get_user_token(user_id)
    return token


@app.route('/api/v1/user/uploadToken', methods=['POST'])
@jwt_required
def get_user_token():
    request_data = request.json
    device_token = request_data.get('device_token')
    print(device_token)

    if device_token is not None and type(device_token) is str:
        user = User_token(
            "fa210389-a8f6-402c-8681-ce8b628fbd88", str(device_token))
        db.update_user_token(user)
        return jsonify({'message': "success"}), 200
    else:
        return jsonify({'error': "device_token not provided or is not string"}), 400


@app.route('/api/v1/user/preference', methods=['GET'])
@jwt_required
def fetch_tasks():
    user_id = request.args.get('user_id')
    try:
        result = db.get_user_preference(user_id)
    except TypeError:
        return jsonify({'message': "type not correct"}), 500

    if result is None:
        return jsonify({'message': "preference not set yet"}), 200
    else:
        jsonData = json.dumps(result, indent=4, cls=PreferenceEncoder)
        return jsonify(json.loads(jsonData)), 200


@app.route('/api/v1/user/uploadPreference', methods=['POST'])
@jwt_required
def get_tasks():
    request_data = request.json
    if isinstance(request_data, list):
        prs = []
        for element in request_data:
            user_id = element.get('user_id')
            filter_type = element.get('filter_type')
            value = element.get('filter_value')

            if not user_id:
                return jsonify({'error': "user_id in one of element not provided."}), 400
            if not filter_type:
                return jsonify({'error': "filter_type in one of element not provided."}), 400
            if not value:
                return jsonify({'error': "filter_value in one of element not provided."}), 400
            prs.append(Preference(user_id, filter_type, value))

        db.update_user_preference(prs)
    else:
        return jsonify({'error': "request body is not array."}), 400

    return jsonify({'message': "success"}), 200


if __name__ == '__main__':
    # Crawler.start_crawl(db)
    app.run(host='127.0.0.1', debug=True)
    push_notification.send_push_notification(db)
