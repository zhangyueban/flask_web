from flask import Blueprint,g, jsonify
from flask_httpauth import HTTPBasicAuth
import re
from db import get_db
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app as app


auth = Blueprint("auth",__name__)
http_auth = HTTPBasicAuth()

@http_auth.verify_password
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



@auth.route('/api/login', methods=['POST'])
@http_auth.login_required()
def get_auth_token():
    token = generate_auth_token()
    print(token)
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.admin})

