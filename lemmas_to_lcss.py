# -*- coding: utf-8 -*-

import itertools
from collections import OrderedDict
import json
import pprint as pp

class LCS:
	'''
	Класс для изменения извлечённых словарей. Позволяет заменить леммы на наибольшие общие подстроки форм.
	'''

	def longest_common_substring(self, s1, s2):
		'''
		Функция для вычисления наибольшей общей подстроки.
		Алгоритм - динамическое программирование.
		Извлекаются только непрерывные общие подстроки.
		Источник: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python_3
		:param s1: строка 1
		:param s2: строка 2
		:return: наибольшая общая подстрока строк 1 и 2
		'''
		m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
		longest, x_longest = 0, 0
		for x in range(1, 1 + len(s1)):
			for y in range(1, 1 + len(s2)):
				if s1[x - 1] == s2[y - 1]:
					m[x][y] = m[x - 1][y - 1] + 1
					if m[x][y] > longest:
						longest = m[x][y]
						x_longest = x
				else:
					m[x][y] = 0
		return s1[x_longest - longest: x_longest]

	def lcs_as_lemmas(self, morphodict):
		'''
		Функция, которая заменяет леммы на наибольшие общие подстроки и формирует новый словарь.
		:param morphodict: исходный словарь
		:return: новый словарь, где на месте леммы НОП
		'''
		new_dict = OrderedDict()
		for word_tuple in morphodict.items():						# для каждого слова
			forms = [list(el.keys())[0] for el in word_tuple[1]]	# список всех форм
			combos = list(itertools.combinations(forms, 2))			# список всех комбинаций форм
			lcss = [self.longest_common_substring(tuple[0],tuple[1]) for tuple in combos]	# список НОП для всех пар форм
			min_string = lcss[0]
			for i in range(1,len(lcss)):
				if len(lcss[i]) < len(min_string):					# выбираем НОП наименьшей длины
					min_string = lcss[i]
			new_dict.update({min_string: word_tuple[1]})			# формируем новый словарь, где на месте леммы НОП
		return new_dict

	def load_json(self, filename):
		'''
		Загрузка файла json.
		:param filename: имя файла json
		:return: загруженный словарь
		'''
		with open(filename, encoding='utf-8-sig') as f:
			dct = json.load(open(filename), object_pairs_hook=OrderedDict)
		return dct

	def write_json(self, filename, dct):
		'''
		Запись файла json.
		:param filename: имя файла json
		:param dct: словарь для записи
		:return: 
		'''
		with open(filename, 'w', encoding='utf-8-sig') as f:
			json.dump(dct, f, ensure_ascii=False)

def cut_paradigms_nouns(morphodict):
	'''
	Удаление притяжательных форм существительных из таблиц.
	:param morphodict: 
	:return: 
	'''
	keys_to_del = []
	for key in morphodict.keys():
		for i in range(len(morphodict[key])):
			form_tuple = list(morphodict[key][i].items())[0]
			if 'Possession' in form_tuple[1].keys():
				if i == 0:
					keys_to_del.append(key)
					break
				else:
					morphodict[key] = morphodict[key][:i]
					break
	for el in keys_to_del:
		del morphodict[el]
	#pp.pprint(morphodict)
	return morphodict

def cut_paradigm_verbs(morphodict):
	'''
	Удаление форм наклонений и склонения инфинитива из таблиц глаголов.
	:param morphodict: 
	:return: 
	'''
	for key in morphodict.keys():
		morphodict[key] = morphodict[key][:5]
	return morphodict

if __name__ == '__main__':
	lcss = LCS()
	morphodict_verbs = lcss.load_json('verbs.json')
	cut_morphodict_verbs = cut_paradigm_verbs(morphodict_verbs)
	lcss.write_json('verbs_cut.json', cut_morphodict_verbs)
	new_verbs = lcss.lcs_as_lemmas(cut_morphodict_verbs)
	lcss.write_json('verbs_cut_lcs.json', new_verbs)

	morphodict_nouns = lcss.load_json('nouns.json')
	cut_morphodict_nouns = cut_paradigms_nouns(morphodict_nouns)
	lcss.write_json('nouns_cut.json', cut_morphodict_nouns)
	new_nouns = lcss.lcs_as_lemmas(cut_morphodict_nouns)
	lcss.write_json('nouns_cut_lcs.json', new_nouns)
