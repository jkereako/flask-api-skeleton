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
from flask import Flask, jsonify
from werkzeug.contrib.cache import SimpleCache
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth

# Initialize core objects
app = Flask(__name__)
cache = SimpleCache(__name__)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

if not os.path.exists("db.sqlite"):
    db.create_all()

app.config.from_object("config")

#-- Models
from app.models import user

#-- Controllers
from app.controllers import api
# from app.controllers import private

app.register_blueprint(api.mod)
# app.register_blueprint(private.mod)

#-- Error handlers
@app.errorhandler(403)
def forbidden(error):
    """
    Renders 403 page
    :returns: JSON
    :rtype: flask.Response
    """

    return jsonify({"success":False, "message":"Error 403: Forbidden"}), 403

@app.errorhandler(404)
def not_found(error):
    """
    Renders 404 page
    :returns: JSON
    :rtype: flask.Response
    """

    return jsonify({"success":False, "message":"Error 404: Not found"}), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    Renders 404 page
    :returns: JSON
    :rtype: flask.Response
    """

    return jsonify({"success":False, "message":"Error 500: Internal server error"}), 500
