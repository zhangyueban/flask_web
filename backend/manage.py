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

    #app.add_url_rule("/", endpoint="index")

    return app

app = create_app()
auth = HTTPBasicAuth()
app.app_context().push()  # 推送应用上下文环境
db = get_db()


class Admin():
    # 密码加密
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    # 密码解析
    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    # 获取token，有效时间10min
    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        admin = Admin.query.get(data['id'])
        return admin


@auth.verify_password
def verify_password(name_or_token, password):
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    admin = Admin.verify_auth_token(name_or_token)
    if not admin:
        admin = Admin.query.filter_by(name=name_or_token).first()
        if not admin or not admin.verify_password(password):
            return False
    g.admin = admin
    return True


@app.route('/api/login', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = g.admin.generate_auth_token()
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.admin.name})


if __name__ == '__main__':
    app.run(host='0.0.0.0')