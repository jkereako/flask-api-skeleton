#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app.controllers.api
    ~~~~~~~~~~~~~~~
    The controllers module.

    :author: Jeff Kereakoglow
    :date: 2014-11-14
    :copyright: (c) 2014 by Alexis Digital
    :license: MIT, see LICENSE for more details
"""
from flask import Blueprint, request, jsonify, g, url_for
from app.utils import cache_data, fetch_cached_data
from app.models import user
from app import auth

mod = Blueprint("api", __name__, url_prefix="/api")

@mod.route("users", methods=['POST'])
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})

@mod.route("users/<int:id>")
def user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@mod.route("/token")
@auth.login_required
def token():
    token = g.user.generate_auth_token(600)
    return jsonify({"token": token.decode('ascii'), 'duration': 600})

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
