#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020.05.08
# @Author  : hyper zhang
from flask import Flask
from flask_cors import CORS
from auth import auth


def create_app():
    app = Flask(__name__)
    # r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
    CORS(app, resources=r'/*')
    app.config['SECRET_KEY'] = 'hard to guess string'
    app.debug = True

    @app.route('/hello')
    def hello_world():
        return "hello world"

    import db
    db.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.register_blueprint(auth)
    app.run(host='0.0.0.0')