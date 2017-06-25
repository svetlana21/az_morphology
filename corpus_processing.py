# -*- coding: utf-8 -*-
import re

def sents2types(corpus):
	'''
	Функция, преобразующая корпус предложений в корпус слов (types).
	:param corpus: 
	:return: 
	'''
	tokens = []
	for sent in corpus:
		tokens.extend(sent.lower().split(' '))
	types = list(set(tokens))
	types.sort()
	types.remove('<s>')		# удаление тегов начала и конца предложения, которые расставлены в корпусе
	types.remove('</s>')
	types.remove('')		# удаление пустых строк
	clear_types = []
	for type in types:		# удаление символа U+0307, часто встречающегося в словах
		if '̇' in type:
			type = type.replace('̇', '')
		clear_types.append(type)
	return clear_types

def clear(types):
	'''
	Функция, очищающая корпус от некорректных дефисных написаний типа "-azerbaycan" и "azerbaycan-".
	:param types: 
	:return: 
	'''
	bad_types = []
	hyphen_before = re.compile('-.+')
	hyphen_after = re.compile('.*-')
	for type in types:
		if hyphen_before.match(type) or hyphen_after.match(type)\
				or len(type) == 1 or len(type) > 22:
			bad_types.append(type)
	for type in bad_types:
		types.remove(type)
	return types

with open('tokens.txt', encoding='utf-8') as f:
	corpus = f.read().split('\n')

types = sents2types(corpus)
types = clear(types)
print(len(types))

with open('corpus_types.txt', 'w', encoding='utf-8') as f:
	for type in types:
		f.write('{}\n'.format(type))

