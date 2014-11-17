#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app
    ~~~~~~~~~~~
    The Flask application module.

    :author: Jeff Kereakoglow
    :date: 2014-11-14
    :copyright: (c) 2014 by Alexis Digital
    :license: MIT, see LICENSE for more details
"""
import os
from utils import prepare_json_response
from flask import Flask, jsonify, request
from werkzeug.contrib.cache import SimpleCache
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth

# Initialize core objects
app = Flask(__name__)
cache = SimpleCache(__name__)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

app.config.from_object("config")

#-- Models
from app.models import user

if not os.path.exists("db.sqlite"):
    db.create_all()

#-- Controllers
from app.controllers import default
from app.controllers import user

app.register_blueprint(default.mod)
app.register_blueprint(user.mod)

#-- Error handlers

# Override the default handlers with JSON responses
@app.errorhandler(400)
def forbidden(error):
    """
    Renders 400 response
    :returns: JSON
    :rtype: flask.Response
    """
    return jsonify(
        prepare_json_response(
            message="Error 400: Bad request",
            success=False,
            data=None
        )
    ), 400

@app.errorhandler(401)
def forbidden(error):
    """
    Renders 400 response
    :returns: JSON
    :rtype: flask.Response
    """
    return jsonify(
        prepare_json_response(
            message="Error 401: Unauthorized",
            success=False,
            data=None
        )
    ), 401

@app.errorhandler(403)
def forbidden(error):
    """
    Renders 403 response
    :returns: JSON
    :rtype: flask.Response
    """
    return jsonify(
        prepare_json_response(
            message="Error 403: Forbidden",
            success=False,
            data=None
        )
    ), 403

@app.errorhandler(404)
def not_found(error):
    """
    Renders 404 response
    :returns: JSON
    :rtype: flask.Response
    """
    return jsonify(
        prepare_json_response(
            message="Error 404: Not found",
            success=False,
            data=None
        )
    ), 404

@app.errorhandler(405)
def not_found(error):
    """
    Renders 405 response
    :returns: JSON
    :rtype: flask.Response
    """
    return jsonify(
        prepare_json_response(
            message="Error 405: Method not allowed",
            success=False,
            data=None
        )
    ), 405

@app.errorhandler(500)
def internal_server_error(error):
    """
    Renders 500 response
    :returns: JSON
    :rtype: flask.Response
    """

    return jsonify(
        prepare_json_response(
            message="Error 500: Internal server error",
            success=False,
            data=None
        )
    ), 405
