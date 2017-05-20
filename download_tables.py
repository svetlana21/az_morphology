# -*- coding: <utf-8> -*-

import requests
import lxml.html
import pprint as pp
from collections import OrderedDict
import json
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
		form_list = []
		for i, st in enumerate(inflection):  # для каждой формы составляем словари с грам.значениями
			st.remove(st[0])  # убираем из строк таблицы местоимения
		for i, st in enumerate(inflection):  # для каждой формы составляем словари с грам.значениями
			for j, el in enumerate(st):
				form_dict = OrderedDict([('Number', self.noun_grammems['Numbers'][j]),
										 ('Case', self.noun_grammems['Cases'][i])])
				form_list.append(OrderedDict([(el, form_dict)]))  # список словарей для всех форм слова
		return form_list

	def extract_poss(self,form_list,possessives):
		'''
		
		:param form_list: 
		:param possessives: 
		:return: 
		'''
		for i, st in enumerate(possessives):  # для каждой формы составляем словари с грам.значениями
			st.remove(self.possessive_pronouns[i])  # убираем из строк таблицы местоимения
			for j, el in enumerate(st):
				form_dict = OrderedDict([('Person-Number_psor', self.noun_grammems['Person-Number_psor'][i]),
										 ('Possession', self.noun_grammems['Possession'][0])])
				if len(possessives) == 6 and len(possessives[0]) == 6:
					form_dict.update(OrderedDict([('Number', self.noun_grammems['Numbers'][0]),
												  ('Case', self.noun_grammems['Cases'][j])]))
				else:
					if j%2 == 0:
						form_dict.update({'Number': self.noun_grammems['Numbers'][0]})
					else:
						form_dict.update({'Number': self.noun_grammems['Numbers'][1]})
					form_dict.update({'Case': self.noun_grammems['Cases'][j//2]})
				form_list.append(OrderedDict([(el, form_dict)]))  # список словарей для всех форм слова
		return form_list

	def download_noun_tables(self, wordlist):
		'''
		Функция для скачивания таблиц словоизменения существительных и преобразования их в словарь.
		:param wordlist: список существительных
		:return: словарь из всех полученных таблиц
		'''
		morphodict_nouns = OrderedDict()

		for word in wordlist:       # для каждого существительного в списке загружаем текст его страницы
			url = 'https://az.wiktionary.org/wiki/{}'.format(requests.utils.quote(word, safe=''))
			t = self.s.get(url).text
			text = BeautifulSoup(t, 'lxml')
			first_el = text.findAll('span',id="Az.C9.99rbaycan_dili")[0]
			transl_table = first_el.findNext('table',attrs={"class":"translations"})
			tables = []
			while first_el.findNext('table') != transl_table:
				tables.append(first_el.findNext('table',rules="all"))
				first_el = first_el.findNext('table',rules="all")
			inflection = []
			new_tables = []
			for table in tables:
				tab = lxml.html.fromstring(str(table))
				trs = tab.xpath('//table/tr')
				strings = [tr.xpath('th/text()|th/*/text()|th/*/*/text()|td/text()|td/*/text()|td/*/*/text()') for
						   tr in trs]
				if len(strings) == 8 and len(strings[2]) == 3 \
						or len(strings) == 7 and len(strings[2]) == 3 \
						or len(strings) == 8 and len(strings[2]) == 7 \
						or len(strings) == 8 and len(strings[2]) == 13:  # если таблица правильного формата, то продолжаем с ней работу,
																		# иначе говорим, что таблица неверна.
					new_tables.append(strings)
				else:
					print(word, ': Wrong table')
				if len(new_tables) == 2:
					possessives = []
					for table in new_tables:
						if ['Mənsubiyyətə görə'] in table:
							possessives = table[2:]
						else:
							inflection = table[-6:]
					form_list_infl = self.extract_infl(inflection)
					full_form_list = self.extract_poss(form_list_infl,possessives)
					morphodict_nouns.update({word: full_form_list})  # словарь лемм
				elif len(tables) == 1:
					inflection = strings[-6:]
					full_form_list = self.extract_infl(inflection)
					morphodict_nouns.update({word: full_form_list})  # словарь лемм
				elif len(tables) > 2:
					print('Wrong number of tables.')
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
	# verbs_list = extractor.load_wordlist('verbs.txt')
	# morphodict_verbs = extractor.download_verb_tables(verbs_list)
	# extractor.write_json('verbs.json', morphodict_verbs)
	extractor.download_noun_tables(['ana'])
