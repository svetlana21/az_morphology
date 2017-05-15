# -*- coding: <utf-8> -*-

import requests
import lxml.html
import pprint as pp
from collections import OrderedDict
import json

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
        self.verb_grammems = {'Forms':['-mişdi_past', '-di_past','present','fut_def','fut_indef',
                                       'imp','arzu','vacib','lazım','şərt','inf'],
                              'Person-Number':['1_sing','2_sing','3_sing',
                                               '1_plur','2_plur','3_plur'],
                              'Cases':['nom','gen','dat','acc','loc','abl']}

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
                for i in range(6):
                    strings[i].remove(self.cases[i])        # убираем из строк таблицы названия падежей
                    strings[i].remove(self.pronouns[i])        # убираем из строк таблицы местоимения
                form_list = []
                for i, st in enumerate(strings):        # для каждой формы составляем словари с грам.значениями
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
                    print(word,'Wrong table')
        return morphodict_verbs

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