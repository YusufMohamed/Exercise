from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from Services import get_data_from_api, top_five_genres
from secrets import *

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/{}'.format(USR, PWD, DATABASE_HOST_IP, DATABASE_HOST_PORT, DATABASE_NAME)
engine = create_engine(SQLALCHEMY_DATABASE_URI)


@app.route('/movies', methods=['GET'])
def process_movie():
    response = get_data_from_api(request.args.to_dict(), engine)
    return jsonify(response)


@app.route('/compute', methods=['GET'])
def compute():
    result = top_five_genres(engine)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host=WEBAPP_IP, port=WEPAPP_PORT)
