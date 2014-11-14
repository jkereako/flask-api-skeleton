#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app.models.user
    ~~~~~~~~~~~~~~~
    The User model.

    :author: Jeff Kereakoglow
    :date: 2014-11-14
    :copyright: (c) 2014 by Alexis Digital
    :license: MIT, see LICENSE for more details
"""
from app import app, db
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {"id":self.id,"username":self.username}

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data["id"])
        return user
