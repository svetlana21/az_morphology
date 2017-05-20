# -*- coding: <utf-8> -*-

import requests
import lxml.html
import pprint as pp
from collections import OrderedDict
import json
import re
from bs4 import BeautifulSoup

class TableExtractor():
	'''
	Класс для скачивания таблиц словоизменения из азербайджанского викисловаря и преобразования их в словарь вида
	{лемма: [{форма_1:{грамматическая информация}}
				...
			{форма_n:{грамматическая информация}}]}.
	На выходе - файл json.
	'''
	def __init__(self):
		self.s = requests.Session()
		self.s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'})
		self.cases = ['Adlıq','Yiyəlik','Yönlük','Təsirlik','Yerlik','Çıxışlıq']
		self.pronouns = ['Mən','Sən','O','Biz','Siz','Onlar']
		self.possessive_pronouns = ['Mənim','Sənin','Onun','Bizim','Sizin','Onların']
		self.verb_grammems = {'Forms':['-mişdi_past', '-di_past','present','fut_def','fut_indef',
									   'imp','arzu','vacib','lazım','şərt','inf'],
							  'Person-Number':['1_sing','2_sing','3_sing',
											   '1_plur','2_plur','3_plur'],
							  'Cases':['nom','gen','dat','acc','loc','abl']}
		self.noun_grammems = {'Numbers':['sing','plur'],
							  'Cases':['nom','gen','dat','acc','loc','abl'],
							  'Person-Number_psor': ['1_sing', '2_sing', '3_sing',
												'1_plur', '2_plur', '3_plur'],
							  'Possession':['pos']}

	def load_wordlist(self,filename):
		'''
		Загрузка заранее подготовленного списка слов определённой части речи.
		:param filename: имя файла со списком слов интересующей части речи
		:return: список слов
		'''
		with open(filename, encoding='utf-8') as f:
			txt = f.read()
		wordlist = txt.split('\n')
		return wordlist

	def download_verb_tables(self, wordlist):
		'''
		Функция для скачивания таблиц словоизменения глаголов и преобразования их в словарь.
		:param wordlist: список глаголов
		:return: словарь из всех полученных таблиц
		'''
		morphodict_verbs = OrderedDict()
		for word in wordlist:       # для каждого глагола в списке загружаем текст его страницы
			url = 'https://az.wiktionary.org/wiki/{}'.format(requests.utils.quote(word, safe=''))
			t = self.s.get(url).text
			root = lxml.html.fromstring(t)
			trs = root.xpath('//table[@class="wikitable"]/tr')      # таблица с атрибутом class="wikitable" -
																	# это таблица словоизменения; извлекаем её строки
			strings = [trs[i].xpath('th/text()|th/a/text()') for i in range(3,len(trs))]    # первые 3 строки таблицы - это заголовки.
																							# Поэтому получаем текст только оставшихся строк.
			if len(strings) == 6 and len(strings[0]) == 13:     # если таблица правильного формата, то продолжаем с ней работу,
																# иначе говорим, что таблица неверна.
				form_list = []
				for i, st in enumerate(strings):        # для каждой формы составляем словари с грам.значениями
					st.remove(self.cases[i])  # убираем из строк таблицы названия падежей
					st.remove(self.pronouns[i])  # убираем из строк таблицы местоимения
					for j, el in enumerate(st):
						form_dict = OrderedDict([('Form',self.verb_grammems['Forms'][j])])
						if j < 10:
							form_dict.update({'Person-Number': self.verb_grammems['Person-Number'][i]})
						else:
							form_dict.update({'Case': self.verb_grammems['Cases'][i]})
						form_list.append(OrderedDict([(el, form_dict)]))    # список словарей для всех форм слова
				morphodict_verbs.update({word:form_list})   # словарь лемм
			else:
				if len(strings) != 0:
					print(word,': Wrong table')
		return morphodict_verbs

	def extract_infl(self, inflection):
		'''
		Функция для составления словаря из таблицы изменения существительных по падежам и числам.
		:param inflection: таблица изменения существительных по падежам и числам, извлеченная из викисловаря
		:return: список всех форм слова
		'''
		form_list = []
		for i, st in enumerate(inflection):
			st.remove(st[0])  				# убираем из строк таблицы местоимения
		for i, st in enumerate(inflection):  # для каждой формы составляем словари с грам.значениями
			for j, el in enumerate(st):
				form_dict = OrderedDict([('Number', self.noun_grammems['Numbers'][j]),
										 ('Case', self.noun_grammems['Cases'][i])])
				form_list.append(OrderedDict([(el, form_dict)]))  # список словарей для всех форм слова
		return form_list

	def extract_poss(self,possessives,form_list=[]):
		'''
		Функция для составления словаря из таблицы притяжательных форм существительных (ana - мать, anam - моя мать).
		:param form_list: список форм, уже созданный предыдущей функцией; в него добавляем новые формы
		:param possessives: таблица притяжательных форм, извлеченная из викисловаря
		:return: обновлённый список форм
		'''
		for i, st in enumerate(possessives):
			st.remove(self.possessive_pronouns[i])  # убираем из строк таблицы местоимения
		for i, st in enumerate(possessives):  # для каждой формы составляем словари с грам.значениями
			for j, el in enumerate(st):
				form_dict = OrderedDict([('Person-Number_psor', self.noun_grammems['Person-Number_psor'][i]),
										 ('Possession', self.noun_grammems['Possession'][0])])
				if len(possessives) == 6 and len(possessives[0]) == 6:							# если есть только формы ед.ч.
					form_dict.update(OrderedDict([('Number', self.noun_grammems['Numbers'][0]),
												  ('Case', self.noun_grammems['Cases'][j])]))
				else:
					if j%2 == 0:																# если есть все формы
						form_dict.update({'Number': self.noun_grammems['Numbers'][0]})
					else:
						form_dict.update({'Number': self.noun_grammems['Numbers'][1]})
					form_dict.update({'Case': self.noun_grammems['Cases'][j//2]})
				form_list.append(OrderedDict([(el, form_dict)]))  # список словарей для всех форм слова
		return form_list

	def delete_fonts(self,html):
		'''
		В таблицах встречается выделение цветом отдельных морфем с помощью тега <font>.
		Это приводит к тому, что слово оказывается разделённым этими тегами на несколько частей.
		Функция удаляет теги <font> и </font> во избежание ошибок.
		:param html: текст страницы
		:return: текст страницы без тегов <font> и </font>
		'''
		flags = re.IGNORECASE | re.MULTILINE
		html = re.sub('<font\s*([^\>]+)>', '', html, flags=flags)	# удаление начального тега
		html = re.sub('</font\s*>', '', html, flags=flags)			# удаление конечного тега
		return html

	def download_noun_tables(self, wordlist):
		'''
		Функция для скачивания таблиц словоизменения существительных и преобразования их в словарь.
		:param wordlist: список существительных
		:return: словарь из всех полученных таблиц
		'''
		morphodict_nouns = OrderedDict()
		other_lang_id = re.compile('.+_dili')	# шаблон для поиска языка, отличного от az
		for word in wordlist:  # для каждого существительного в списке загружаем текст его страницы
			print(word)
			url = 'https://az.wiktionary.org/wiki/{}'.format(requests.utils.quote(word, safe=''))
			t = self.s.get(url).text			# получение текстра страницы
			t = self.delete_fonts(t)			# удаление тегов <font> и </font>
			# таблицы склонения существительных можно определить по двум типам атрибутов: rules="all" или "class": "inflection-table"
			# извлекаем все подходящие под это условие таблицы
			all_tables = text.findAll('table', rules="all")
			all_tables.extend(text.findAll('table', attrs={"class": "inflection-table"}))
			# проверка языка: оставляем только таблицы, относящиеся к азербайджанскому
			text = BeautifulSoup(t, 'lxml')
			languages = text.findAll('span', id=other_lang_id)	# находим элементы с id языков
			other_lang = None
			for l in languages:					# находим первый не азербайджанский id, запоминаем
				if l['id'] != "Az.C9.99rbaycan_dili":
					other_lang = l.parent
					break
			tables = []
			if other_lang is not None:			# рекурсивно проходимся по всем тегам до элемента с "нехорошим" id,
												# оставляя только те таблицы, которые встретились до него
				for child in text.descendants:
					if child != other_lang:
						for table in all_tables:
							if child == table:
								tables.append(child)
					else:
						break
			else:
				tables = all_tables
			# извлечение содержимого таблиц
			inflection = []
			new_tables = []
			for table in tables:
				tab = lxml.html.fromstring(str(table))
				trs = tab.xpath('//table/tr')
				strings = [tr.xpath('th/text()|th/*/text()|th/*/*/text()|td/text()|td/*/text()|td/*/*/text()') for
						   tr in trs]
				if len(strings) == 9 and len(strings[2]) == 3 \
						or len(strings) == 8 and len(strings[2]) == 3 \
						or len(strings) == 7 and len(strings[2]) == 3 \
						or len(strings) == 8 and len(strings[2]) == 7 \
						or len(strings) == 8 and len(strings[2]) == 13:  # если таблица правильного формата, то продолжаем с ней работу,
																		# иначе говорим, что таблица неверна.
					new_tables.append(strings)
				else:
					if len(strings) != 4:
						print(word, ': Wrong table (len = {})'.format(len(strings)))
			if len(new_tables) == 2:			# если со страницы получено 2 таблицы, то это таблица склонения по падежам и числам и таблица притяжательных форм
				possessives = []
				for table in new_tables:
					if ['Mənsubiyyətə görə'] in table:		# находим таблицу притяжательных форм по заголовку
						possessives = table[2:]				# удаляем заголовки
					else:
						inflection = table[-6:]				# находим таблицу склонения по падежам и числам и удаляем заголовки
				form_list_infl = self.extract_infl(inflection)		# извлекаем таблицу склонения по падежам и числам
				full_form_list = self.extract_poss(possessives,form_list_infl)		# извлекаем таблицу притяжательных форм
				morphodict_nouns.update({word: full_form_list})  # словарь лемм
			elif len(new_tables) == 1:				# если со страницы получена 1 таблица, то проверяем, какая, и извлекаем
				if ['Mənsubiyyətə görə'] in new_tables[0]:
					full_form_list = self.extract_poss(new_tables[0][2:])
				else:
					full_form_list = self.extract_infl(new_tables[0][-6:])
				morphodict_nouns.update({word: full_form_list})  # словарь лемм
			elif len(new_tables) > 2:				# если было найдено > 2 таблиц, то что-то пошло не так
				print('Wrong number of tables ({}).'.format(len(new_tables)))
			#pp.pprint(morphodict_nouns)

		return morphodict_nouns

	def write_json(self, filename, dct):
		'''
		Запись файла json.
		:param filename: имя файла json
		:param dct: словарь для записи
		:return: 
		'''
		with open(filename, 'w', encoding='utf-8') as f:
			json.dump(dct, f, ensure_ascii=False)

if __name__ == '__main__':
	extractor = TableExtractor()
	verbs_list = extractor.load_wordlist('verbs.txt')
	morphodict_verbs = extractor.download_verb_tables(verbs_list)
	extractor.write_json('verbs.json', morphodict_verbs)
	nouns_list = extractor.load_wordlist('nouns.txt')
	morphodict_nouns = extractor.download_noun_tables(nouns_list)
	extractor.write_json('nouns.json', morphodict_nouns)
