# -*- coding: utf-8 -*-

import os
import csv
import json
from collections import OrderedDict
from pprint import pprint

def load_json(filename):
	'''
	Загрузка файла json.
	:param filename: имя файла json
	:return: загруженный словарь
	'''
	with open(filename, encoding='utf-8-sig'):
		dct = json.load(open(filename), object_pairs_hook=OrderedDict)
	return dct

def load_list(filename):
	'''
	Загрузка списка.
	:param filename:
	:return:
	'''
	with open(filename, encoding='utf-8') as f:
		txt = f.read()
	form_list = txt.split('\n')
	return form_list

def write_json(filename, dct):
	'''
	Запись файла json.
	:param filename: имя файла json
	:param dct: словарь для записи
	:return: 
	'''
	with open(filename, 'w', encoding='utf-8-sig') as f:
		json.dump(dct, f, ensure_ascii=False)

def change_morphodict(corpus, morphodict):
	'''
	Оставляем в парадигмах только те формы, что встретились в корпусе.
	:param corpus: 
	:param morphodict: 
	:return: 
	'''
	new_morphodict = []
	for sublist in morphodict:
		new_paradigm = []
		for i in range(len(sublist[1])):
			if list(sublist[1][i].keys())[0] in set(corpus):
				new_paradigm.append(sublist[1][i])
		if new_paradigm != []:
			new_morphodict.append([sublist[0], new_paradigm])
	return new_morphodict

def make_form_list(morphodict, filename):
	'''
	Составление списка всех форм из викисловаря.
	:param morphodict: таблицы в виде словаря
	:param filename: имя файла для записи
	:return: 
	'''
	form_list = []
	for word_tuple in morphodict:  # для каждого слова
		forms = [list(el.keys())[0] for el in word_tuple[1]]  # список всех форм
		form_list.extend(forms)
	with open(filename, 'w', encoding='utf-8-sig') as f:
		for form in form_list:
			f.write(form + '\n')

# morphodict_nouns = load_json('nouns_lcs_list.json')
# morphodict_verbs = load_json('verbs_lcs_list.json')
# corpus = load_list('corpus_types.txt')
# new_morphodict_verbs = change_morphodict(corpus, morphodict_verbs)
# new_morphodict_nouns = change_morphodict(corpus, morphodict_nouns)
# write_json('new_verbs_lcs.json', new_morphodict_verbs)
# write_json('new_nouns_lcs.json', new_morphodict_nouns)
# make_form_list(new_morphodict_verbs, 'new_verb_forms.txt')
# make_form_list(new_morphodict_nouns, 'new_noun_forms.txt')

def load_csv(filename):
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

def get_lemma(word, morphodict):
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

def evaluate(word_list):
	'''
	Оценка.
	:param word_list: 
	:return: 
	'''
	noun_forms = load_list('new_noun_forms.txt')
	verb_forms = load_list('new_verb_forms.txt')
	morphodict_nouns = load_json('new_nouns_lcs.json')
	morphodict_verbs = load_json('new_verbs_lcs.json')
	count_all = len(noun_forms) + len(verb_forms)
	count_correct = 0
	for word in word_list:
		lemma = ''
		if word[0] in verb_forms:
			lemma = get_lemma(word[0], morphodict_verbs)
		elif word[0] in noun_forms:
			lemma = get_lemma(word[0], morphodict_nouns)
		if lemma != '':
			if lemma + '<>' in word[1]:
				count_correct += 1
	print('All: {}'.format(count_all))
	print('Correct: {}'.format(count_correct))
	print('Errors: {}%'.format((1 - count_correct / count_all) * 100))

file_path = os.path.split(os.path.abspath(__file__))[0]
csv_path = os.path.abspath(file_path + '/../termpaper/FST_morphology-master/FST_morphology/data/result/words_with_border.csv')

word_list = load_csv(csv_path)
evaluate(word_list)