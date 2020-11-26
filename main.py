from flask import Flask, request
from Services import get_data_from_api, save_to_database

app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/movies', methods = ['GET'])
def process_movie():
    get_data_from_api(request.args)
    save_to_database()

    return (request.args)


if __name__ == '__main__':
   app.run()