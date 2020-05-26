from flask import Blueprint,g, jsonify,request
from flask_httpauth import HTTPBasicAuth
import re
from db import get_db
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app as app
from itsdangerous import BadSignature, SignatureExpired
import json


auth = Blueprint("auth",__name__)
http_auth = HTTPBasicAuth()

class User():
    id = None
    name = None
    password = None

    def get_user(self, name_or_token):
        db = get_db()
        sql = "select id, name, password from admins where name ='{}'".format(name_or_token)
        cursor = db.cursor()
        cursor.execute(sql)
        if cursor.fetchall():
            temp = cursor.fetchall()[0]
            self.id = temp[0]
            self.name = temp[1]
            self.password = temp[2]

    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)
        self.update_password()

    def dehash_password(self, password):
        return custom_app_context.verify(password, self.password)

    def update_password(self):
        db = get_db()
        sql = "update admins set password = '{}' where name ='{}'".format(self.password, self.name)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'name': self.name})

    @staticmethod
    def get_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # in
        admin = User()
        admin.get_user(data['name'])
        return admin


@http_auth.verify_password
def verify_password(name_or_token, password):
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    admin = User.get_token(name_or_token)
    if not admin:
        admin = User()
        admin.get_user(name_or_token)
        if not admin.id or not custom_app_context.verify(password, admin.password):
            return False
    g.admin = admin
    return True

@auth.route('/api/login', methods=['POST'])
@http_auth.login_required()
def get_auth_token():
    token = g.admin.generate_auth_token()
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.admin.name})

@auth.route('/api/setpwd', methods=['POST'])
@http_auth.login_required
def set_auth_pwd():
    data = json.loads(str(request.data, encoding="utf-8"))
    if g.admin and g.admin.dehash_password(data['oldpass']) and data['confirpass'] == data['newpass']:
        g.admin.hash_password(data['newpass'])
        return jsonify({'code': 200, 'msg': "密码修改成功"})
    else:
        return jsonify({'code': 500, 'msg': "请检查输入"})