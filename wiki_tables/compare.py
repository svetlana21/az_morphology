# -*- coding: utf-8 -*-
import json
import os
import pprint as pp
from collections import OrderedDict

file_path = os.path.split(os.path.abspath(__file__))[0]
types_name = 'corpus_types.txt'
types_path = os.path.abspath(file_path + '/../corpus/corpus_types/' + types_name)

def load_corp(filename):
	'''
	Загрузка списка слов.
	:param filename: 
	:return: 
	'''
	print('Loading the corpus...')
	with open(filename, encoding='utf-8-sig') as f:
		c = f.read()
		corpus = c.split('\n')
	return corpus

def load_json(filename):
	'''
	Загрузка файла json.
	:param filename: имя файла json
	:return: загруженный словарь
	'''
	print('Loading {}...'.format(filename))
	json_path = os.path.abspath(file_path + '/tables/' + filename)
	with open(json_path, encoding='utf-8-sig') as f:
		dct = json.load(open(json_path), object_pairs_hook=OrderedDict)
	return dct

def list_wiki_forms(morphodict):
	'''
	Создание списка всех словоформ.
	:param morphodict: словарь с таблицами
	:return: 
	'''
	all_forms = []
	for word_tuple in morphodict.items():						# для каждого слова
		forms = [list(el.keys())[0] for el in word_tuple[1]]	# список всех форм
		all_forms.extend(forms)
	return all_forms

def simple_comparison(corpus, wiki_forms):
	'''
	Подсчёт числа форм из викисловаря, которые встречаются в корпусе.
	:param corpus: 
	:param wiki_forms: 
	:return: 
	'''
	print('Simple comparison...')
	in_corp = []
	for word in wiki_forms:
		if word in set(corpus):
			in_corp.append(word)
	print('Слов в корпусе: {}'.format(len(corpus)))
	print('Словоформ в wiki: {}'.format(len(wiki_forms)))
	print('Словоформ из wiki, которые есть в корпусе: {}'.format(len(in_corp)))
	print(in_corp[:10])

def lexeme_comparison(corpus, morphodict):
	'''
	Подсчёт числа лексем из викисловаря, которые встречаются в корпусе.
	(если хоть одна форма лексемы встретилась в корпусе, считаем, что встретилась лексема)
	:param corpus: 
	:param morphodict: 
	:return: 
	'''
	print('Lexeme comparison...')
	lexeme_in_corp = []
	for word_tuple in morphodict.items():  # для каждого слова
		forms = [list(el.keys())[0] for el in word_tuple[1]]	# список всех форм
		for form in forms:
			if form in set(corpus):
				lexeme_in_corp.append(word_tuple[0])
				break
	print('Лексем в wiki: {}'.format(len(morphodict)))
	print('Лексем из wiki, которые есть в корпусе: {}'.format(len(lexeme_in_corp)))
	print(lexeme_in_corp[:10])

def paradigm_comparison(corpus, morphodict):
	'''
	Подсчёт полных парадигм в корпусе.
	:param corpus: 
	:param morphodict: 
	:return: 
	'''
	print('Paradigm comparison...')
	par_in_corp = []
	for word_tuple in morphodict.items():  # для каждого слова
		forms = [list(el.keys())[0] for el in word_tuple[1]]  # список всех форм
		count = 0
		for form in forms:
			if form in set(corpus):
				count += 1
		if len(forms) == count:
			par_in_corp.append(word_tuple[0])
	print('Полных парадигм из wiki, которые есть в корпусе: {}'.format(len(par_in_corp)))
	print('Парадигмы: \n')
	pp.pprint(par_in_corp)

corpus = load_corp(types_path)

verbs_dict = load_json('verbs.json')
nouns_dict = load_json('nouns.json')

verbs_list = list_wiki_forms(verbs_dict)
nouns_list = list_wiki_forms(nouns_dict)

all_wiki_words = list(verbs_list)
all_wiki_words.extend(nouns_list)
simple_comparison(corpus, all_wiki_words)

all_lemmas = OrderedDict()
all_lemmas.update(verbs_dict)
all_lemmas.update(nouns_dict)
lexeme_comparison(corpus, all_lemmas)
paradigm_comparison(corpus, all_lemmas)