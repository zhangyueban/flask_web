from flask import Blueprint, jsonify,request
from auth import http_auth
from db import get_db


user_list = Blueprint('user_list', __name__)

def user_query(name,page):
    db = get_db()
    curr = db.cursor()
    sql_name = "select * from joininfos where name like '%{}%' limit {}, 4".format(name, page)
    sql_all = "select * from joininfos limit {},4;".format(page)
    if name:
        curr.execute(sql_name)
    else:
        curr.execute(sql_all)
    return curr.fetchall()

def user_query_count(name):
    db = get_db()
    curr = db.cursor()
    sql_name = "select count(1) from joininfos where name like '%{}%'".format(name)
    sql_all = "select count(1) from joininfos;"
    if name:
        curr.execute(sql_name)
    else:
        curr.execute(sql_all)
    count = curr.fetchall()
    return count[0][0]


@user_list.route('/api/users/listpage', methods=['GET'])
@http_auth.login_required
def get_user_list():
    page_size = 4
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '')
    index = ['id','name','phone','profess','grade','email','group','power','pub_date']
    if name:
        Infos = user_query(name,(page-1)*page_size)
        count = user_query_count(name)
    else:
        Infos = user_query(None,(page-1)*page_size)
        count = user_query_count(None)
    ans = []
    for i in Infos:
        ans.append(dict(zip(index, list(i))))
    return jsonify({
        'code': 200,
        'total': count,
        'page_size': page_size,
        'infos': ans
    })
