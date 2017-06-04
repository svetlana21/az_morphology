import unittest
import pprint as pp
from collections import OrderedDict

from lemmas_to_lcss import LCS


class TestLCS(unittest.TestCase):

	def setUp(self):
		self.test_lcss = LCS()

	def test_lcs_as_lemmas(self):
		'''
		Тест функции lcs_as_lemmas.
		:return: 
		'''
		test_data = OrderedDict([('abadlıq',
									[OrderedDict([('abadlıq', OrderedDict([('Number', 'sing'), ('Case', 'nom')]))]),
									 OrderedDict([('abadlıqlar', OrderedDict([('Number', 'plur'), ('Case', 'nom')]))]),
									 OrderedDict([('abadlığın', OrderedDict([('Number', 'sing'), ('Case', 'gen')]))]),
									 OrderedDict([('abadlıqların', OrderedDict([('Number', 'plur'), ('Case', 'gen')]))]),
									 OrderedDict([('abadlığa', OrderedDict([('Number', 'sing'), ('Case', 'dat')]))]),
									 OrderedDict([('abadlıqlara', OrderedDict([('Number', 'plur'), ('Case', 'dat')]))]),
									 OrderedDict([('abadlığı', OrderedDict([('Number', 'sing'), ('Case', 'acc')]))]),
									 OrderedDict([('abadlıqları', OrderedDict([('Number', 'plur'), ('Case', 'acc')]))]),
									 OrderedDict([('abadlıqda', OrderedDict([('Number', 'sing'), ('Case', 'loc')]))]),
									 OrderedDict([('abadlıqlarda', OrderedDict([('Number', 'plur'), ('Case', 'loc')]))]),
									 OrderedDict([('abadlıqdan', OrderedDict([('Number', 'sing'), ('Case', 'abl')]))]),
									 OrderedDict([('abadlıqlardan', OrderedDict([('Number', 'plur'), ('Case', 'abl')]))])
									 ]
									)])
		true_result = OrderedDict([('abadlı',
									[OrderedDict([('abadlıq', OrderedDict([('Number', 'sing'), ('Case', 'nom')]))]),
									 OrderedDict([('abadlıqlar', OrderedDict([('Number', 'plur'), ('Case', 'nom')]))]),
									 OrderedDict([('abadlığın', OrderedDict([('Number', 'sing'), ('Case', 'gen')]))]),
									 OrderedDict([('abadlıqların', OrderedDict([('Number', 'plur'), ('Case', 'gen')]))]),
									 OrderedDict([('abadlığa', OrderedDict([('Number', 'sing'), ('Case', 'dat')]))]),
									 OrderedDict([('abadlıqlara', OrderedDict([('Number', 'plur'), ('Case', 'dat')]))]),
									 OrderedDict([('abadlığı', OrderedDict([('Number', 'sing'), ('Case', 'acc')]))]),
									 OrderedDict([('abadlıqları', OrderedDict([('Number', 'plur'), ('Case', 'acc')]))]),
									 OrderedDict([('abadlıqda', OrderedDict([('Number', 'sing'), ('Case', 'loc')]))]),
									 OrderedDict([('abadlıqlarda', OrderedDict([('Number', 'plur'), ('Case', 'loc')]))]),
									 OrderedDict([('abadlıqdan', OrderedDict([('Number', 'sing'), ('Case', 'abl')]))]),
									 OrderedDict([('abadlıqlardan', OrderedDict([('Number', 'plur'), ('Case', 'abl')]))])
									 ]
									)])
		fact_result = self.test_lcss.lcs_as_lemmas(test_data)
		self.assertDictEqual(true_result, fact_result)