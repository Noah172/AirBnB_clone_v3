#!/usr/bin/python3
"""displays app status"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close_session(resp_or_excep):
    storage.close()


@app.errorhandler(404)
def not_found(err):
    return jsonify(('error', 'Not found')), 404


if __name__ == '__main__':
    if getenv('HBNB_API_HOST'):
        app.run(host=getenv('HBNB_API_HOST'),
                port=getenv('HBNB_API_PORT'), threaded=True)
    else:
        app.run(host='0.0.0.0', threaded=True)
