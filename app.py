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
from preference import PreferenceEncoder
from PasswordChecher import PasswordChecher
from rrError import (SqlError)

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

    if db.get_user_id_with_password_hash(email) is None:
        user_id = db.register_user(username, email, hashed_pw, phone)

        if user_id != None:
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

    if user_id != None:
        # Use create_access_token() and create_refresh_token() to create our
        # access and refresh tokens
        ret = {
            'access_token': create_access_token(identity=user_id),
            'refresh_token': create_refresh_token(identity=user_id)
        }
        return jsonify(ret), 200
    else:
        return jsonify({'error': "user not found or password incorrect."}), 400


@app.route('/api/v1/anonymousLogin', methods=['POST'])
def anonymousLogin():
    deviceUUID = request.headers.get('deviceUUID', None)

    if deviceUUID != None:
        # Use create_access_token() and create_refresh_token() to create our
        # access and refresh tokens
        user_id = db.register_user(user_name='', email='', password='', phone='', isAnonymous=True)
        ret = {
            'access_token': create_access_token(identity=str(user_id), expires_delta=False),
        }
        return jsonify(ret), 200
    else:
        return jsonify({'error': "deviceUUID not found."}), 400


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
# @jwt_required
def index():
    host = os.getenv("DB_HOST")
    return f"Hello, World! {host}"


# @app.route('/api/v1/user/token', methods=['GET'])
def fetch_user_token(user_id: str):
    token = db.get_user_token(user_id)
    return token


@app.route('/api/v1/user/uploadFcmToken', methods=['POST'])
@jwt_required
def get_user_token():
    request_data = request.json
    fcm_token = request_data.get('fcm_token')
    current_user = get_jwt_identity()
    print(fcm_token)

    if fcm_token != None and type(fcm_token) is str:
        user = User_token(current_user, str(fcm_token))
        db.update_user_token(user)
        return jsonify({'message': "success"}), 200
    else:
        return jsonify({'error': "fcm_token not provided or != string"}), 400


@app.route('/api/v1/user/preference', methods=['GET'])
@jwt_required
def fetch_tasks():
    user_id = get_jwt_identity()
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
def update_preference():
    request_data = request.json

    user_id = get_jwt_identity()
    region = request_data.get('region')
    section = request_data.get('section')
    kind = request_data.get('kind')

    rent_price = request_data.get('rent_price')
    pattern = request_data.get('pattern')
    space = request_data.get('space')

    # if not user_id:
    #     return jsonify({'error': "user_id not provided."}), 400

    if not region:
        return jsonify({'error': "region not provided."}), 400

    pref = Preference(
        user_id=user_id,
        region=region,
        section=section,
        kind=(kind if kind != None else ''),
        rent_price=(rent_price if rent_price != None else 0),
        pattern=(pattern if pattern != None else ''),
        space=(space if space != None else '')
    )

    try:
        db.update_user_preference(pref)
    except SqlError as error:
        return jsonify({'error': error.message}), 400

    return jsonify({'message': "success"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, load_dotenv=True)

    # docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' rental-server
    # app.run(host='172.17.0.3', debug=False)
