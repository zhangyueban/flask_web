#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020.05.08
# @Author  : hyper zhang

import os
import re
import json
from datetime import datetime

from flask import Flask, g, jsonify, make_response, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context
from db import get_db
from flask_login import LoginManager
from flask_login import UserMixin
from werkzeug.security import check_password_hash

def create_app():
    app = Flask(__name__)
    # r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
    CORS(app, resources=r'/*')
    app.config['SECRET_KEY'] = 'hard to guess string'
    CSRF_ENABLED = True
    app.debug = True

    @app.route('/hello')
    def hello_world():
        return "hello world"

    import db
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    return app

app = create_app()
auth = HTTPBasicAuth()
app.app_context().push()  # 推送应用上下文环境
db = get_db()

class User(UserMixin):
    pass

auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(name_or_token, password):
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    admin = None #获取token
    if not admin:
        db = get_db()
        sql = "select name, password from admins where name ='{}'".format(name_or_token)
        cursor = db.cursor()
        cursor.execute(sql)
        user = cursor.fetchall()[0]
        admin = user[0]
        password_hash = user[1]
        print(custom_app_context.verify(password, password_hash))
        if not admin or not custom_app_context.verify(password, password_hash):
            return False
    g.admin = admin
    return True

def generate_auth_token(expiration=600):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'name': g.admin})



@app.route('/api/login', methods=['POST'])
@auth.login_required()
def get_auth_token():
    token = generate_auth_token()
    print(token)
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token, 'name': g.admin})


if __name__ == '__main__':
    app.run(host='0.0.0.0')