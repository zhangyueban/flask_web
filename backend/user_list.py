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

@user_list.route('/api/user/remove', methods=['GET'])
@http_auth.login_required
def remove_user():
    remove_id = request.args.get('id', type=int)
    if remove_id:
        db = get_db()
        cursor = db.cursor()
        sql = "delete from joininfos where id = {}".format(remove_id)
        cursor.execute(sql)
        db.commit()
        return jsonify({'code': 200, 'msg': "删除成功"})
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})

@user_list.route('/api/user/bathremove', methods=['GET'])
@http_auth.login_required
def bathremove_user():
    remove_ids = request.args.get('ids',type=str)
    remove_ids = tuple(eval(remove_ids))
    print(remove_ids)
    if remove_ids:
        db = get_db()
        cursor = db.cursor()
        sql = "delete from joininfos where id in {}".format(remove_ids)
        cursor.execute(sql)
        db.commit()
        return jsonify({'code': 200, 'msg': "删除成功"})
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})
