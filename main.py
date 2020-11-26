from flask import Flask, request
from sqlalchemy import create_engine
from Services import get_data_from_api, save_to_database


app = Flask(__name__)
PWD = 'joest3r.95'
USR = 'ymkhalifa'
SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@localhost:3306/andela'.format(USR, PWD)
SQLALCHEMY_DATABASE_URI_2 = 'sqlite:///andela.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI_2, echo=True)

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/movies', methods = ['GET'])
def process_movie():
    get_data_from_api(request.args.to_dict(), engine)

@app.route('/compute', methods =  ['GET'])
def compute():

    return 1


if __name__ == '__main__':
    app.run()