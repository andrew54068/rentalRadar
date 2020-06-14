from flask import Flask, request, jsonify
import sys
import json

from DataBaseConnector import DataBaseConnector
from preference import Preference
from User_token import User_token
import Crawler

from preference import PreferenceEncoder
import push_notification

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/v1/user/token', methods=['GET'])
def fetch_user_token():
    user_id = request.args.get('user_id')
    token = db.get_user_token(user_id)
    if token is None:
        return jsonify({'error': "device_token not found"}), 400
    else:
        return jsonify({'device_token': f"{token}"}), 200


@app.route('/api/v1/user/uploadToken', methods=['POST'])
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
    db = DataBaseConnector()
    # Crawler.start_crawl(db)
    app.run(host='127.0.0.1', debug=True)
    push_notification.send_push_notification(db)
