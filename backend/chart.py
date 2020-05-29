from flask import Blueprint, jsonify
from auth import http_auth
from db import get_db
from user_list import user_query_count
from collections import Counter


chart = Blueprint('chart', __name__)

def user_query():
    db = get_db()
    curr = db.cursor()
    sql_all = "select * from joininfos;"
    curr.execute(sql_all)
    return curr.fetchall()


@chart.route('/api/getdrawPieChart', methods=['GET'])
@http_auth.login_required
def getdrawPieChart():
    Infos = user_query()
    interest = ''
    for i in Infos:
        interest += i[6]+','
    interest = interest.split(',')
    total = user_query_count(None)
    data_value = [0, 0, 0, 0, 0, 0, 0]  # 和下面组别一一对应
    group_value = ['视觉', '视频', '前端', '办公', '后端', '运营', '移动']
    for num in range(0, 7):
        data_value[num] = Counter(interest)[group_value[num]]

    return jsonify({'code': 200, 'value': data_value, 'total': total})

@chart.route('/api/getdrawLineChart', methods=['GET'])
@http_auth.login_required
def getdrawLineChart():
     pass #TODO
