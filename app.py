from flask import Flask, request, jsonify

from DataBaseConnector import DataBaseConnector
from preference import Preference

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/v1/user/preference', methods=['POST'])
def get_tasks():
    request_data = request.get_json()
    print("request_data: ")
    print(request_data)
    user_id = request_data['user_id']
    filter_type = request_data['filter_type']
    value = request_data['filter_value']

    if not user_id:
        return jsonify({'error': "not user_id provided."}), 400
    if not filter_type:
        return jsonify({'error': "not filter_type provided."}), 400
    if not value:
        return jsonify({'error': "not filter_value provided."}), 400

    print(f"user_id: {user_id}")
    print(f"filter_type: {filter_type}")
    print(f"value: {value}")

    pr = Preference(user_id, filter_type, value)
    db.update_user_preference([pr])

    # exec(open("./main.py").read())

    return jsonify({}), 200


if __name__ == '__main__':
    db = DataBaseConnector()
    app.run(host='127.0.0.1', debug=True)
