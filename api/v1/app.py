#!/usr/bin/python3
"""App file"""


from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

import os
host = os.getenv('HBNB_API_HOST')
port = os.getenv('HBNB_API_PORT')


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exit):
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return {"error": "Not found"}, 404


if __name__ == '__main__':
    print(host or '0.0.0.0')
    print(port or 5000)
    app.run(host=(host or '0.0.0.0'),
            port=(port or 5000), threaded=True, debug=True)
