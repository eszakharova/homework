from flask import Flask
from flask import render_template, request
from pymystem3 import Mystem
import json
import requests
import nltk
from nltk.stem.snowball import SnowballStemmer
from collections import OrderedDict
from nltk.collocations import *

m = Mystem()
app = Flask(__name__)


def load_corp():
    my_corpus = nltk.corpus.PlaintextCorpusReader('./texts', '.*\.txt')
    return my_corpus


def corp_exact_search(exact, corp):
    found = []
    for sent in corp.sents():
        if exact in sent:
            found.append(sent)
    return found


def corp_stem_search(stem, corp):
    stemmer = SnowballStemmer("russian")
    stem = stemmer.stem(stem)
    found = []
    for sent in corp.sents():
        ap = False
        for word in sent:
            if stem in word and stemmer.stem(word) == stem:
                ap = True
        if ap:
            found.append(sent)
    return found


def corp_coll_search(word, corp):
    found = []
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(corp.words())
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    sorted_bigrams = sorted(bigram for bigram, score in scored)
    for pair in sorted_bigrams:
        if word in pair:
            found.append(pair)
    return found


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
    lem_freq_ordered = OrderedDict(sorted(lem_freq_dict.items(), key=lambda x: x[0], reverse=True))
    for j in lem_freq_ordered:
        res2.append(j + ': ' + str(lem_freq_dict[j]))
    return res1, res2, lem_freq_ordered


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
    return [id1_members_cnt, id2_members_cnt, intersection, closed], {id1: id1_members_cnt, id2: id2_members_cnt}

mycorp = load_corp()


@app.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')


@app.route('/verbs', methods=['get', 'post'])
def verbs():
    if request.form:
        text = request.form['text']
        res1, res2, dat = verbs_info(text)
        return render_template('verbs.html', input=text, toprint1=res1, toprint2=res2, data=dat)
    return render_template('verbs.html', data={})


@app.route('/vk', methods=['get', 'post'])
def vk():
    if request.form:
        group_id1 = request.form['group_id1']
        group_id2 = request.form['group_id2']
        result, d = get_members_info(group_id1, group_id2)
        return render_template('vk.html', result=result, group_id1=group_id1, group_id2=group_id2, data=d)
    return render_template('vk.html', data={})


@app.route('/nltk', methods=['get', 'post'])
def search_corp():
    if request.form:
        exact = request.form['exact']
        stem = request.form['stem']
        collword = request.form['coll']
        num = request.form['colls']
        if exact:
            pre_result = corp_exact_search(exact, mycorp)
            result = [' '.join(sent) for sent in pre_result]
            return render_template('nltk.html', result=result)
        elif stem:
            pre_result = corp_stem_search(stem, mycorp)
            result = [' '.join(sent) for sent in pre_result]
            return render_template('nltk.html', result=result)
        elif collword:
            pre_result = corp_coll_search(collword, mycorp)
            if not num:
                result = pre_result
            else:
                if len(pre_result) > int(num):
                    result = pre_result[:int(num)+1]
                else:
                    result = pre_result
            return render_template('nltk.html', result=result)
    return render_template('nltk.html')


if __name__ == '__main__':
    app.run(debug=True)
