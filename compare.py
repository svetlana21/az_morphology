# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

def load_corp(filename):
	'''
	Загрузка списка слов.
	:param filename: 
	:return: 
	'''
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
	with open(filename, encoding='utf-8-sig') as f:
		dct = json.load(open(filename), object_pairs_hook=OrderedDict)
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

corpus = load_corp('corpus_types.txt')

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
lexeme_comparison(corpus,all_lemmas)
