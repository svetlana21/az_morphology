# -*- coding: utf-8 -*-

import os
import csv
import json
import pickle
import codecs
from collections import OrderedDict
from pprint import pprint

file_path = os.path.split(os.path.abspath(__file__))[0]
tables_lcss_path = os.path.abspath(file_path + '/../wiki_tables/tables_lcss')
types_path = os.path.abspath(file_path + '/../corpus/corpus_types')
changed_tables_path = os.path.abspath(file_path + '/changed_tables')
form_lists_path = os.path.abspath(file_path + '/form_lists')
csv_path = os.path.abspath(file_path + '/../words_with_border.csv')
signatures_path = os.path.abspath(file_path + '/../linguistica/dump')


def load_json(json_path):
    '''
	Загрузка файла json.
	:param filename: имя файла json
	:return: загруженный словарь
	'''
    print('Loading {}...'.format(json_path))
    with open(json_path, encoding='utf-8-sig') as f:
        dct = json.load(codecs.open(json_path, 'r', 'utf-8-sig'), object_pairs_hook=OrderedDict)
    return dct


def load_list(path):
    '''
	Загрузка списка.
	:param filename:
	:return:
	'''
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    form_list = txt.split('\n')
    return form_list


class PrepareData:
    '''
	Подготовительный этап перед оценкой.
	Оставляем в парадигмах только те формы, что встретились в корпусе.
	Составление списка всех форм из викисловаря.
	'''

    def change_morphodict(self, corpus, morphodict, filename):
        '''
		Оставляем в парадигмах только те формы, что встретились в корпусе.
		:param corpus: список тайпов
		:param morphodict: таблицы словоизменения
		:param filename: файл для записи изменённого словаря
		:return:
		'''
        print('Changing the tables...')
        new_morphodict = []
        for sublist in morphodict:
            new_paradigm = []
            for i in range(len(sublist[1])):
                if list(sublist[1][i].keys())[0] in set(corpus):
                    new_paradigm.append(sublist[1][i])
            if new_paradigm != []:
                new_morphodict.append([sublist[0], new_paradigm])
        with open(os.path.abspath(changed_tables_path + filename), 'w', encoding='utf-8-sig') as f:
            json.dump(new_morphodict, f, ensure_ascii=False)
        return new_morphodict

    def make_form_list(self, morphodict, filename):
        '''
		Составление списка всех форм из викисловаря.
		:param morphodict: таблицы в виде словаря
		:param filename: имя файла для записи
		:return:
		'''
        print('Making a form list...')
        form_list = []
        for word_tuple in morphodict:  # для каждого слова
            forms = [list(el.keys())[0] for el in word_tuple[1]]  # список всех форм
            form_list.extend(forms)
        with open(os.path.abspath(form_lists_path + filename), 'w', encoding='utf-8-sig') as f:
            for form in form_list:
                f.write(form + '\n')


class Evaluate:
    '''
	Оценка результатов FST_morphology и библиотеки Linguistica.
	'''

    def __init__(self):
        self.noun_forms = load_list(os.path.abspath(form_lists_path + '/new_noun_forms.txt'))
        self.verb_forms = load_list(os.path.abspath(form_lists_path + '/new_verb_forms.txt'))
        self.morphodict_nouns = load_json(os.path.abspath(changed_tables_path + '/new_nouns_lcs.json'))
        self.morphodict_verbs = load_json(os.path.abspath(changed_tables_path + '/new_verbs_lcs.json'))

    def load_csv(self, filename):
        '''
		Загрузка файла csv с результатами.
		:param filename: имя файла csv
		:return: список списков вида:
		[
		[məntiqlə, mən<>tiqlə], [keçisi, keç<>is<>i], ...
		]
		'''
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            word_list = [row for row in reader]
        word_list.pop(0)
        return word_list

    def get_lemma(self, word, morphodict):
        '''
		Найти лемму для определённой формы.
		:param word:
		:param morphodict:
		:return:
		'''
        for word_tuple in morphodict:
            for i in range(len(word_tuple[1])):
                if word in word_tuple[1][i].keys():
                    lemma = word_tuple[0]
                    break
        return lemma

    def correct_paradigms(self, morphodict, correct_forms):
        correct_paras = 0
        for par in morphodict:
            count_correct_forms = 0
            for el in par[1]:
                if list(el.keys())[0] in correct_forms:
                    count_correct_forms += 1

            if count_correct_forms == len(par[1]):
                correct_paras += 1
        return correct_paras

    def evaluate(self, word_list):
        '''
		Оценка результатов FST_morphology.
		:param word_list:
		:return:
		'''
        print('FST_morphology evaluation starts...')
        count_all = 0
        count_correct = 0
        correct_forms = []
        for word in word_list:
            lemma = ''
            if word[0] in self.verb_forms:
                count_all += 1
                lemma = self.get_lemma(word[0], self.morphodict_verbs)
            elif word[0] in self.noun_forms:
                count_all += 1
                lemma = self.get_lemma(word[0], self.morphodict_nouns)
            if lemma != '':
                if lemma + '<>' in word[1]:
                    count_correct += 1
                    correct_forms.append(word[0])

        count_correct_paradigms = self.correct_paradigms(self.morphodict_nouns, correct_forms) \
                                  + self.correct_paradigms(self.morphodict_verbs, correct_forms)

        print('All: {}'.format(count_all))
        print('Correct forms: {}'.format(count_correct))
        print('Correct paradigms: {}'.format(count_correct_paradigms))
        print('Errors: {}%'.format((1 - count_correct / count_all) * 100))

    def lxa_evaluation(self, signatures):
        '''
		Оценка результатов библиотеки Linguistica.
		:param signatures: 
		:return: 
		'''
        print('LXA evaluation starts...')
        count_all = 0
        count_correct = 0
        correct_forms = []
        for sig in signatures.keys():
            forms = []
            divided_forms = []
            for el in signatures[sig]:
                for i in range(len(el)):
                    if el[i] != 'NULL':
                        if len(sig + el[i]) <= 22:
                            forms.append(sig + el[i])
                            divided_forms.append(sig + '<>' + el[i])
                    else:
                        if len(sig + el[i]) <= 22:
                            forms.append(sig)
                            divided_forms.append(sig + '<>')

            for i, form in enumerate(forms):
                lemma = ''
                if form in self.verb_forms:
                    count_all += 1
                    lemma = self.get_lemma(form, self.morphodict_verbs)
                elif form in self.noun_forms:
                    count_all += 1
                    lemma = self.get_lemma(form, self.morphodict_nouns)
                if lemma != '':
                    if lemma + '<>' in divided_forms[i]:
                        # print('+: ', lemma, divided_forms[i], divided_forms)
                        count_correct += 1
                        correct_forms.append(form)
                    # else:
                    # 	print('-: ', lemma, divided_forms[i], divided_forms)

        count_correct_paradigms = self.correct_paradigms(self.morphodict_nouns, correct_forms) \
                                  + self.correct_paradigms(self.morphodict_verbs, correct_forms)

        print('All: {}'.format(count_all))
        print('Correct forms: {}'.format(count_correct))
        print('Correct paradigms: {}'.format(count_correct_paradigms))
        print('Errors: {}%'.format((1 - count_correct / count_all) * 100))


if __name__ == '__main__':
    morphodict_nouns = load_json(os.path.abspath(tables_lcss_path + '/nouns_lcs_list.json'))
    morphodict_verbs = load_json(os.path.abspath(tables_lcss_path + '/verbs_lcs_list.json'))
    corpus = load_list(os.path.abspath(types_path + '/corpus_types.txt'))

    prep = PrepareData()
    new_morphodict_verbs = prep.change_morphodict(corpus, morphodict_verbs, '/new_verbs_lcs.json')
    new_morphodict_nouns = prep.change_morphodict(corpus, morphodict_nouns, '/new_nouns_lcs.json')
    prep.make_form_list(new_morphodict_verbs, '/new_verb_forms.txt')
    prep.make_form_list(new_morphodict_nouns, '/new_noun_forms.txt')

    eval = Evaluate()
    word_list = eval.load_csv(csv_path)
    eval.evaluate(word_list)

    signatures_name = '/signatures_msl=3_mal=2_msc=2.pickle'
    with open(os.path.abspath(signatures_path + signatures_name), 'rb') as f:
        signatures = pickle.load(f)
    eval.lxa_evaluation(signatures)
