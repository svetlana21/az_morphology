
# Скрипт для получения сигнатур с помощью библиотеки Linguistica

import linguistica as lxa
import pickle
import os

file_path = os.path.split(os.path.abspath(__file__))[0]
corpus_name = 'corpus.txt'
corpus_path = os.path.abspath(file_path + '/../corpus/raw_corpus/' + corpus_name)

def linguistica_data(pickle_name):
	print('Getting lexicon...')
	lex = lxa.read_corpus(corpus_path, min_stem_length=3, max_affix_length=2, min_sig_count=2)
	print('Stems to signatures...')
	signatures = lex.stems_to_signatures()
	print('Pickling...')
	dump_path = os.path.abspath(os.path.split(os.path.abspath(__file__))[0] + '/dump/' + pickle_name)
	with open(dump_path, 'wb') as f:
		pickle.dump(signatures, f)
	return signatures

pickle_name = 'signatures_msl=3_mal=2_msc=2.pickle'
linguistica_data(pickle_name)