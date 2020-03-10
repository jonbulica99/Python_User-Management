#!/usr/bin/env python3

import os
from api import UserEndpoint, GroupEndpoint, HostEndpoint, CommandEndpoint

from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

from helpers.db_manager import DatabaseManager
from utils.config import Config


# initialze config and the database manager
config = Config()
manager = DatabaseManager(config)
database = manager.create_database()

# initialize flask and the API helpers
supreme_path = os.path.join('supreme', 'dist')
app = Flask(__name__, template_folder=supreme_path)
CORS(app)
api = Api(app)


# serve the static output of vuejs
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def index(path):
    if path and '.' in path:
        # if the path doesnt contain a filename delimiter, let the vue-router handle the request.
        # This prevents various browser cache errors and page resolution errors if flask is restarted.
        return send_from_directory(supreme_path, path)
    return render_template("index.html")


api.add_resource(UserEndpoint.create(database), '/api/v1/users/<string:username>')
api.add_resource(GroupEndpoint.create(database), '/api/v1/groups/<int:id>')
api.add_resource(HostEndpoint.create(database), '/api/v1/hosts/<int:id>')
api.add_resource(CommandEndpoint.create(manager, app), '/api/v1/cmd/<string:command>')

# inject database connection to flask
database.connect(app)

if __name__ == "__main__":
    # start flask
    app.run(**config.parse_section("frontend"))
