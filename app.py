from flask import Flask, request, jsonify

from DataBaseConnector import DataBaseConnector
from preference import Preference
import sys

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/v1/user/preference', methods=['POST'])
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
    app.run(host='127.0.0.1', debug=True)
