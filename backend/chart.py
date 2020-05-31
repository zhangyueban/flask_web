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
    Infos = user_query()
    profess_value = set()
    grade_value = set()
    grade_data = dict()
    for i in Infos:
        profess_value.add(i[3])
        grade_value.add(i[4])
    profess_value = list(profess_value)
    grade_value = list(grade_value)
    for i in grade_value:
        grade_data[i] = [0] *len(profess_value)
    for i in Infos:
        for grade in grade_value:
            for profess_num in range(len(profess_value)):
                if i[3] == profess_value[profess_num] and i[4] == grade:
                    grade_data[grade][profess_num] += 1
    
    return jsonify({'code': 200, 'profess_value': profess_value, 'grade_value': grade_value, 'grade_data': grade_data})




