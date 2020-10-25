import os
from eventlet import wsgi
import eventlet
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from mongoengine import connect, disconnect
from Q2.User.service import init_user

from routes import ROUTES

load_dotenv()


def create_app(PORT, ENV):
    print(PORT, ENV)
    app = Flask(__name__, template_folder="Q1")

    for route in ROUTES:
        app.register_blueprint(route)

    app.secret_key = os.getenv('APP_SECRETE')
    base_path = os.path.dirname(os.path.realpath(__file__))
    app.config['BASE_PATH'] = base_path
    app.config['UPLOAD_FOLDER'] = os.path.join(base_path, 'uploads')

    @app.before_first_request
    def first_request():
        connect('TrolleyApp', host='localhost', port=27017)
        init_user()


    @app.before_request
    def hook():
        # connect to database
        connect('TrolleyApp', host='localhost', port=27017)
        print("Db connected @ port 27017")

        print('endpoint: %s, url: %s,  method: %s, path: %s, body %s' % (
            request.endpoint,
            request.url,
            request.method,
            request.path,
            request.get_json() or request.form
        ))

    @app.after_request
    def teardown_company_db_connection(response):
        disconnect("TrolleyApp")

        return response

    @app.route('/')
    def main():
        return render_template('Login.html')

    @app.errorhandler(500)
    def http_500_handler(error):
        print(error)
        err = str(error)
        return jsonify(message="something went wrong", error=err, statusCode=400)

    if ENV == 'dev':
        app.run(port=PORT, debug=True)
    else:
        # run on http
        wsgi.server(eventlet.listen(('', int(PORT))), app)


PORT = os.getenv('PORT')
ENV = os.getenv('ENV')

if __name__ == "__main__":  # on running python app.py

    create_app(PORT, ENV)
