from flask import Flask
from flask import url_for, render_template, request, redirect
from pymystem3 import Mystem

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


@app.route('/', methods=['get', 'post'])
def index():
    if request.form:
        text = request.form['text']
        res1, res2 = verbs_info(text)
        return render_template('index.html', input=text, toprint1=res1, toprint2=res2)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
