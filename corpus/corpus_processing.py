
# Обработка корпуса предложений (чистка и создание корпуса слов (types)).

import re
import os
from pprint import pprint

file_path = os.path.split(os.path.abspath(__file__))[0]
corpus_name = 'corpus.txt'
corpus_path = os.path.abspath(file_path + '/raw_corpus/' + corpus_name)
types_name = 'corpus_types.txt'
types_path = os.path.abspath(file_path + '/corpus_types/' + types_name)


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
	types.remove('')		# удаление пустых строк
	return types

def clean(types):
	'''
	Очистка корпуса от некорректных дефисных написаний типа "-azerbaycan" и "azerbaycan-".
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

with open(corpus_path, encoding='utf-8') as f:
	corpus = f.read().split('\n')

types = sents2types(corpus)
types = clean(types)
print('Number of types: {}'.format(len(types)))

with open(types_path, 'w', encoding='utf-8') as f:
	for type in types:
		f.write('{}\n'.format(type))
