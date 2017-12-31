import pickle
import os
import nltk
from pylab import *
from tqdm import tqdm
import csv
import random


WORD_LEN_THRESHOLD = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
WORDS_WITH_BORDER = []

file_path = os.path.split(os.path.abspath(__file__))[0]
words_with_arcs_data_path = os.path.abspath(file_path + '/../data/data_from_fst/words_with_arcs.txt')

with open(os.path.abspath(file_path + '/../data/raw_data/vertex/states_with_peaks_4.pkl'), 'rb') as f:
    states_with_peaks = list(pickle.load(f))
numbers_of_st_with_peaks = set([int(el[1]) for el in states_with_peaks])
print(numbers_of_st_with_peaks)


def data_prepare(length_word):
    # Загружаем характеристики вершин (степени, средняя позиция, частота).
    # Загружаем слова с переходами и вершинами.
    with open(os.path.abspath(file_path + '/../data/raw_data/vertex/vertex_degree_pos_word_betw_info.pkl'), 'rb') as f:
        vertex_degree_pos_word_info = pickle.load(f)
    words_with_arcs = list()
    f = open(words_with_arcs_data_path, encoding='utf8')
    for line in f.readlines():
        line_without_str = line.strip()
        words_with_arcs.append(line_without_str.split(' '))
    words_with_arcs = words_with_arcs
    print('loading_files done.')

    # Из массива убираем короткие слова.
    print("count words_with_arcs before filter:", len(words_with_arcs))
    words_with_arcs = [words for words in words_with_arcs if len(words[0]) == length_word]
    print("count words_with_arcs after filter:", len(words_with_arcs))

    # Создания словаря вершин и их характеристик.
    dict_vertex = dict()
    for elements in vertex_degree_pos_word_info:
        dict_vertex[elements[0][1]] = dict_vertex.setdefault(elements[0][1], list()) + [
            [elements[0][0], elements[0][2]], elements[1], elements[2]]
    print("dictionary_vertex done.")

    # Добавления инф. о вершинах к словам.
    with tqdm(total=len(words_with_arcs)) as pbar:
        for words in words_with_arcs:
            words.append([[vertex, list()] for vertex in words[1].split('-')])
            for components in words[-1]:
                for vertex_key in dict_vertex:
                    if vertex_key == components[0]:
                        components[1].append(dict_vertex[vertex_key])
            pbar.update(1)
    # pprint(words_with_arcs)
    file = os.path.abspath(
        file_path + '/../data/data_for_splitting/words_with_vertex_all_info_len_%s.pkl' % (str(length_word),))
    f = open(file, 'wb')
    pickle.dump(words_with_arcs, f)
    f.close()


def splitter(length_word, option='freq'):
    """"
    option: 'freq' - разбиение по частотам
            'vertex' - разбиение по вершинам с пиками степеней
            'freq_vertex' - учёт обоих критериев

    ['аура', '0-32-310-1812-8472', [['0', []], 
                                    ['32', [[['1', '31'], ['1'], [176324]]]], 
                                    ['310', [[['1', '16'], ['2'], [2136]]]], 
                                    ['1812', [[['1', '7'], ['3'], [388]]]], 
                                    ['8472', [[['1', '3'], ['4'], [24]]]]]]
    ['ауре', '0-32-310-1812-8474', [['0', []], 
                                    ['32', [[['1', '31'],  ['1'], [176324]]]], 
                                    ['310', [[['1', '16'], ['2'], [2136]]]], 
                                    ['1812', [[['1', '7'], ['3'], [388]]]], 
                                    ['8474', [[['1', '3'], ['4'], [205]]]]]]
    ['ауру', '0-32-310-1812-8477', [['0', []], 
                                    ['32', [[['1', '31'],  ['1'], [176324]]]], 
                                    ['310', [[['1', '16'], ['2'], [2136]]]], 
                                    ['1812', [[['1', '7'], ['3'], [388]]]], 
                                    ['8477', [[['1', '1'], ['11'], [24]]]]]]
    ['ауры', '0-32-310-1812-135452', [['0', []], 
                                      ['32', [[['1', '31'], ['1'], [176324]]]], 
                                      ['310', [[['1', '16'], ['2'], [2136]]]], 
                                      ['1812', [[['1', '7'], ['3'], [388]]]], 
                                      ['135452', []]]]
    """

    VERTEX_MAX_FREQ_POSITION_IN_WORD = 3
    VERTEX_FREQ = 80
    NUMBER_VERTEX = 3

    with open(os.path.abspath(file_path + '/../data/data_for_splitting/words_with_vertex_all_info_len_%s.pkl' % (
    str(length_word),)), 'rb') as f:
        words_with_vertex_all_info = pickle.load(f)

    for tokens in words_with_vertex_all_info:
        vertex_split = []
        for index, vertex in enumerate(tokens[-1]):
            if vertex[-1] != []:
                # фильтр вершин;
                if index + 1 != len(tokens[-1]):
                    if int(vertex[1][0][1][0]) >= VERTEX_MAX_FREQ_POSITION_IN_WORD:
                        if option == 'freq':
                            if int(vertex[1][0][2][0]) >= VERTEX_FREQ:
                                # сохраняем вершину и ее частоту;
                                vertex_split.append((vertex[0], int(vertex[1][0][2][0])))
                        elif option == 'vertex':
                            if int(vertex[0]) in numbers_of_st_with_peaks:
                                # сохраняем вершину и её степени;
                                vertex_split.append((vertex[0], vertex[1][0][0]))
                        elif option == 'freq_vertex':
                            if int(vertex[1][0][2][0]) >= VERTEX_FREQ:
                                if int(vertex[0]) in numbers_of_st_with_peaks:
                                    # сохраняем вершину и её степени;
                                    vertex_split.append((vertex[0], vertex[1][0][0]))
                        else:
                            print('Unknown option')
        tokens.append(vertex_split)

    for words in words_with_vertex_all_info:
        symbols_with_vertex = list(zip(list(words[0]), list(nltk.bigrams(words[1].split('-')))))
        word_with_border = []
        if words[-1] != []:
            if option == 'freq' or option == 'freq_vertex':
                # берем n самых частотных вершин;
                vertex_spl = sorted(words[-1], key=lambda x: x[-1], reverse=True)[:NUMBER_VERTEX]
            elif option == 'vertex':
                # берем n вершин с наибольшими перепадами степеней;
                vertex_spl = sorted(words[-1], key=lambda x: math.fabs(int(x[-1][0]) - int(x[-1][1])), reverse=True)[
                             :NUMBER_VERTEX]
            for s_v in symbols_with_vertex:
                symbol_border_check = s_v[0]
                for v in vertex_spl:
                    if v[0] == s_v[1][1]:
                        symbol_border_check = symbol_border_check + '<'
                    if v[0] == s_v[1][0]:
                        symbol_border_check = '>' + symbol_border_check
                word_with_border.append(symbol_border_check)
        if word_with_border != []:
            WORDS_WITH_BORDER.append([words[0], ''.join(word_with_border)])

for i in WORD_LEN_THRESHOLD:
    # data_prepare(i)
    splitter(i, 'freq_vertex')

random.shuffle(WORDS_WITH_BORDER)

columns_names = ["initial_token", "token_with_border"]
with open(os.path.abspath(file_path + '/../data/result/words_with_border_vertex_freq.csv'), 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',',  quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(columns_names)
    for el in WORDS_WITH_BORDER:
        writer.writerow(el)