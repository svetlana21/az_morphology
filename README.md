# azwiktionary
Извлечение таблиц словоизменения из азербайджанского викисловаря. Работа с корпусом предложений на азербайджанском языке.

/corpus:

corpus_processing.py - обработка корпуса предложений (чистка и создание корпуса слов (types))

corpus_types.txt - корпус уникальных слов

/evaluation_v1 - скрипт и данные для оценки результатов.

/evaluation_v2 - скрипт и данные для оценки результатов (с изменением исходных таблиц словоизменения: оставлены только те словоформы, что встретились в корпусе), позволяет оценить количество правильных парадигм (неполных, так как не все формы могут быть представлены в корпусе)

/linguistica - скрипт для получения сигнатур с помощью библиотеки Linguistica

/wiki_tables - скрипты и данные для выкачивания таблиц словоизменения из Викисловаря:

download_tables.py - скрипт для загрузки таблиц

verbs.txt - список всех глаголов, статьи о которых есть в викисловаре

nouns.txt - список существительных

verbs.json - таблицы в формате json
    
nouns.json - таблицы в формате json

Статистика:

Глаголы (леммы): 433

Глаголы (формы): 28578

Существительные (леммы): 1286

Существительные (формы): 19776

lemmas_to_lcss.py - замена лемм на наибольшие общие подстроки форм в словарях, созданных с помощью download_tables.py

verbs_lcs.json - словари из verbs.json с НОП вместо лемм

nouns_lcs.json - словари из nouns.json с НОП вместо лемм

compare.py - скрипт для сравнения корпуса с таблицами - сколько словоформ встретилось, сколько лемм.

Результаты:

Уникальных слов в корпусе: 117158

Словоформ в wiki: 48354

Словоформ из wiki, которые есть в корпусе: 7093

Лексем в wiki: 1717

Лексем из wiki, которые есть в корпусе: 1279

Полных парадигм из wiki, которые есть в корпусе: 41


words_with_arcs.txt - данные из дампа fst.

words_with_border.csv - результаты FST_morphology.
