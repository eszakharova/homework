import json
import re


def read_json_to_dicts(filename):
    dicts = []
    f = open(filename, 'r')
    for line in f.readlines():
        dicts.append(json.loads(line))
    return dicts


class Word:
    def __init__(self, **values):
        vars(self).update(values)


def do_frequency(*args):
    freq_list = {}
    for arg in args:
        if arg in freq_list:
            freq_list[arg] += 1
        else:
            freq_list[arg] = 1
    v = list(freq_list.values())
    k = list(freq_list.keys())
    return k[v.index(max(v))]


def make_right_dicts(pre_dicts):
    dicts = []
    for d in pre_dicts:
        rdict = {'text': d['text']}
        try:
            rdict['num_an'] = len(d['analysis'])
            rdict['freq_lemma'] = do_frequency(*(i['lex'] for i in d['analysis']))
            rdict['freq_pos'] = do_frequency(*(re.split('[,=]', i['gr'])[0] for i in d['analysis']))
        except:
            rdict['num_an'] = 0
            # rdict['freq_lemma'] = ''
            # rdict['freq_pos'] = ''

        dicts.append(rdict)
    return dicts


def create_words(arr):
    all_words = []
    texts = []
    for i in arr:
        if i['text'] not in texts:
            texts.append(i['text'])
            new = Word(**i)
            all_words.append(new)
    return all_words

for j in create_words(make_right_dicts(read_json_to_dicts('ubogiy.json'))):
    print(vars(j))
