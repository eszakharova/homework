from flask import Flask
from flask import render_template, request
from pymystem3 import Mystem
import json
import requests

m = Mystem()
app = Flask(__name__)


def verbs_info(text):
    ana = m.analyze(text)
    verb_cnt = 0
    word_cnt = 0
    imperf = 0
    tran = 0
    lem_freq_dict = {}
    for i in ana:
        if i['text'].strip() and 'analysis' in i and i['analysis']:
            word_cnt += 1
            if 'V' in i['analysis'][0]['gr']:
                verb_cnt += 1
                if i['analysis'][0]['lex'] not in lem_freq_dict:
                    lem_freq_dict[i['analysis'][0]['lex']] = 1
                else:
                    lem_freq_dict[i['analysis'][0]['lex']] += 1
                if 'несов' in i['analysis'][0]['gr']:
                    imperf += 1
                if 'пе=' in i['analysis'][0]['gr']:
                    tran += 1
    if word_cnt == 0:
        word_cnt += 1
    res_names = ['Всего глаголов в тексте: ', 'Доля глаголов в тексте: ', 'Переходных глаголов: ',
                 "Непереходных глаголов: ", 'Совершенного вида: ', 'Несовершенного вида: ']
    res_values = [verb_cnt, verb_cnt / word_cnt, tran, verb_cnt - tran, verb_cnt - imperf, imperf]

    res1 = []
    res2 = []
    for i in range(len(res_names)):
        res1.append(res_names[i] + str(res_values[i]))
    for j in sorted(lem_freq_dict.keys(), key=lambda x: lem_freq_dict[x], reverse=True):
        res2.append(j + ': ' + str(lem_freq_dict[j]))
    return res1, res2


def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)


def get_all_members(group_id, count):
    member_ids = []
    off = 0
    while off < count:
        current_ids = vk_api(method='groups.getMembers', group_id=group_id, offset=off, count=1000)
        # print(current_ids)
        member_ids.extend(current_ids['response']['users'])
        off += 1000
    return set(member_ids)


def get_members_info(id1, id2):
    id1_members_cnt = 0
    id2_members_cnt = 0
    closed = False
    id1_ = vk_api(method='groups.getById', group_id=id1, fields='members_count')
    id2_ = vk_api(method='groups.getById', group_id=id2, fields='members_count')
    if id1_['response'][0]['is_closed'] == 1 or id2_['response'][0]['is_closed'] == 1:
        closed = True
        intersection = 0
    else:
        id1_members_cnt = id1_['response'][0]['members_count']
        id2_members_cnt = id2_['response'][0]['members_count']
        member_ids1 = get_all_members(id1, id1_members_cnt)
        member_ids2 = get_all_members(id2, id2_members_cnt)
        intersection = len(member_ids1.intersection(member_ids2))
    return [id1_members_cnt, id2_members_cnt, intersection, closed]


@app.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')


@app.route('/verbs', methods=['get', 'post'])
def verbs():
    if request.form:
        text = request.form['text']
        res1, res2 = verbs_info(text)
        return render_template('verbs.html', input=text, toprint1=res1, toprint2=res2)
    return render_template('verbs.html')


@app.route('/vk', methods=['get', 'post'])
def vk():
    if request.form:
        group_id1 = request.form['group_id1']
        group_id2 = request.form['group_id2']
        result = get_members_info(group_id1, group_id2)
        return render_template('vk.html', result=result, group_id1 = group_id1, group_id2 = group_id2)
    return render_template('vk.html')


if __name__ == '__main__':
    app.run(debug=True)
