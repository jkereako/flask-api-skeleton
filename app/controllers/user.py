#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app.controllers.user
    ~~~~~~~~~~~~~~~
    The user controller module.

    :author: Jeff Kereakoglow
    :date: 2014-11-14
    :copyright: (c) 2014 by Alexis Digital
    :license: MIT, see LICENSE for more details
"""
from flask import abort, Blueprint, request, jsonify, g, url_for
from app.utils import *
from app.models.user import User
from app import db, auth

mod = Blueprint("user", __name__, url_prefix="/api")

@mod.route("/users", methods=["GET"])
def all():
    return jsonify(
        prepare_json_response(
            message=None,
            success=True,
            data=[i.serialize for i in User.query.all()]
        )
    )

@mod.route("/user", methods=["POST"])
def create():
    """
    $ curl -i -X POST -H "Content-Type: application/json" -d '{"username":"user","password":"python"}' http://localhost:5000/api/user
    """
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        abort(400)    # missing arguments

    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user

    a_user = User(username=username)
    a_user.hash_password(password)
    db.session.add(a_user)
    db.session.commit()

    return jsonify(
        prepare_json_response(
            message="User created",
            success=True,
            data={"username": a_user.username}
        )
    ), 201, {"Location": url_for("user.single", id=a_user.id)}

@mod.route("/users/<int:id>", methods=["GET"])
def single(id):
    user = User.query.get(id)
    if not user:
        abort(400)

    return jsonify(
        prepare_json_response(
            message="User found",
            success=True,
            data={"username": user.username}
        )
    )

@mod.route("/resource", methods=["GET"])
@auth.login_required
def resource():
    return jsonify(
        prepare_json_response(
            message="Hi there, %s! This is a protected resource." % g.user.username,
            success=True,
            data={"username": g.user.username}
        )
    )

@mod.route("/token", methods=["GET"])
@auth.login_required
def token():
    token = g.user.generate_auth_token(600)

    return jsonify(
        prepare_json_response(
            message=None,
            success=True,
            data={"token": token.decode("ascii"), "duration":600}
        )
    )

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
