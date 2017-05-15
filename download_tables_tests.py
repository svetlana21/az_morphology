import unittest
from collections import OrderedDict

from download_tables import TableExtractor

class TestTableExtractor(unittest.TestCase):

    def setUp(self):
        self.test_extractor = TableExtractor()

    def test_download_verb_tables(self):
        '''
        'getmək' - cлучай, когда на странице есть таблица и она нужная.
        'asmaq' - случай, когда на странице нет таблицы.
        'aprel' - случай, когда таблица есть, но она неподходящего формата (т.е., вероятнее всего, та, которую извлекать не нужно).
        :return: 
        '''
        test_data = ['getmək','asmaq','aprel']
        true_result = OrderedDict([("getmək",
            [OrderedDict([("getmişdim", OrderedDict([("Form","-mişdi_past"),("Person-Number","1_sing")]))]),
             OrderedDict([("getdim", OrderedDict([("Form", "-di_past"), ("Person-Number", "1_sing")]))]),
             OrderedDict([("gedirəm", OrderedDict([("Form", "present"), ("Person-Number", "1_sing")]))]),
             OrderedDict([("gedəcəyəm", OrderedDict([("Form", "fut_def"), ("Person-Number", "1_sing")]))]),
             OrderedDict([("gedərəm", OrderedDict([("Form", "fut_indef"), ("Person-Number", "1_sing")]))]),
             OrderedDict([("gedim", OrderedDict([("Form", "imp"), ("Person-Number", "1_sing")]))]),
             OrderedDict([("gedəm", OrderedDict([("Form", "arzu"), ("Person-Number", "1_sing")]))]),
             OrderedDict([("getməliyəm", OrderedDict([("Form", "vacib"), ("Person-Number", "1_sing")]))]),
             OrderedDict([("gedəsiyəm", OrderedDict([("Form", "lazım"), ("Person-Number", "1_sing")]))]),
             OrderedDict([("getsəm", OrderedDict([("Form", "şərt"), ("Person-Number", "1_sing")]))]),
             OrderedDict([("getmək", OrderedDict([("Form", "inf"), ("Case", "nom")]))]),
             OrderedDict([("getmişdin", OrderedDict([("Form", "-mişdi_past"), ("Person-Number", "2_sing")]))]),
             OrderedDict([("getdin", OrderedDict([("Form", "-di_past"), ("Person-Number", "2_sing")]))]),
             OrderedDict([("gedirsən", OrderedDict([("Form", "present"), ("Person-Number", "2_sing")]))]),
             OrderedDict([("gedəcəksən", OrderedDict([("Form", "fut_def"), ("Person-Number", "2_sing")]))]),
             OrderedDict([("gedərsən", OrderedDict([("Form", "fut_indef"), ("Person-Number", "2_sing")]))]),
             OrderedDict([("get", OrderedDict([("Form", "imp"), ("Person-Number", "2_sing")]))]),
             OrderedDict([("gedəsən", OrderedDict([("Form", "arzu"), ("Person-Number", "2_sing")]))]),
             OrderedDict([("getməlisən", OrderedDict([("Form", "vacib"), ("Person-Number", "2_sing")]))]),
             OrderedDict([("gedəsisən", OrderedDict([("Form", "lazım"), ("Person-Number", "2_sing")]))]),
             OrderedDict([("getsən", OrderedDict([("Form", "şərt"), ("Person-Number", "2_sing")]))]),
             OrderedDict([("getməyin", OrderedDict([("Form", "inf"), ("Case", "gen")]))]),
             OrderedDict([("getmişdi", OrderedDict([("Form", "-mişdi_past"), ("Person-Number", "3_sing")]))]),
             OrderedDict([("getdi", OrderedDict([("Form", "-di_past"), ("Person-Number", "3_sing")]))]),
             OrderedDict([("gedir", OrderedDict([("Form", "present"), ("Person-Number", "3_sing")]))]),
             OrderedDict([("gedəcək", OrderedDict([("Form", "fut_def"), ("Person-Number", "3_sing")]))]),
             OrderedDict([("gedər", OrderedDict([("Form", "fut_indef"), ("Person-Number", "3_sing")]))]),
             OrderedDict([("getsin", OrderedDict([("Form", "imp"), ("Person-Number", "3_sing")]))]),
             OrderedDict([("gedə", OrderedDict([("Form", "arzu"), ("Person-Number", "3_sing")]))]),
             OrderedDict([("getməlidir", OrderedDict([("Form", "vacib"), ("Person-Number", "3_sing")]))]),
             OrderedDict([("gedəsidir", OrderedDict([("Form", "lazım"), ("Person-Number", "3_sing")]))]),
             OrderedDict([("getsə", OrderedDict([("Form", "şərt"), ("Person-Number", "3_sing")]))]),
             OrderedDict([("getməyə", OrderedDict([("Form", "inf"), ("Case", "dat")]))]),
             OrderedDict([("getmişdik", OrderedDict([("Form", "-mişdi_past"), ("Person-Number", "1_plur")]))]),
             OrderedDict([("getdik", OrderedDict([("Form", "-di_past"), ("Person-Number", "1_plur")]))]),
             OrderedDict([("gedirik", OrderedDict([("Form", "present"), ("Person-Number", "1_plur")]))]),
             OrderedDict([("gedəcəyik", OrderedDict([("Form", "fut_def"), ("Person-Number", "1_plur")]))]),
             OrderedDict([("gedərik", OrderedDict([("Form", "fut_indef"), ("Person-Number", "1_plur")]))]),
             OrderedDict([("gedək", OrderedDict([("Form", "imp"), ("Person-Number", "1_plur")]))]),
             OrderedDict([("gedək", OrderedDict([("Form", "arzu"), ("Person-Number", "1_plur")]))]),
             OrderedDict([("getməliyik", OrderedDict([("Form", "vacib"), ("Person-Number", "1_plur")]))]),
             OrderedDict([("gedəsiyik", OrderedDict([("Form", "lazım"), ("Person-Number", "1_plur")]))]),
             OrderedDict([("getsək", OrderedDict([("Form", "şərt"), ("Person-Number", "1_plur")]))]),
             OrderedDict([("getməyi", OrderedDict([("Form", "inf"), ("Case", "acc")]))]),
             OrderedDict([("getmişdiniz", OrderedDict([("Form", "-mişdi_past"), ("Person-Number", "2_plur")]))]),
             OrderedDict([("getdiniz", OrderedDict([("Form", "-di_past"), ("Person-Number", "2_plur")]))]),
             OrderedDict([("gedirsiniz", OrderedDict([("Form", "present"), ("Person-Number", "2_plur")]))]),
             OrderedDict([("gedəcəksiniz", OrderedDict([("Form", "fut_def"), ("Person-Number", "2_plur")]))]),
             OrderedDict([("gedərsiniz", OrderedDict([("Form", "fut_indef"), ("Person-Number", "2_plur")]))]),
             OrderedDict([("gedəsiniz", OrderedDict([("Form", "imp"), ("Person-Number", "2_plur")]))]),
             OrderedDict([("gedəsiniz", OrderedDict([("Form", "arzu"), ("Person-Number", "2_plur")]))]),
             OrderedDict([("getməlisiniz", OrderedDict([("Form", "vacib"), ("Person-Number", "2_plur")]))]),
             OrderedDict([("gedəsisiniz", OrderedDict([("Form", "lazım"), ("Person-Number", "2_plur")]))]),
             OrderedDict([("getsəniz", OrderedDict([("Form", "şərt"), ("Person-Number", "2_plur")]))]),
             OrderedDict([("getməkdə", OrderedDict([("Form", "inf"), ("Case", "loc")]))]),
             OrderedDict([("getmişdilər", OrderedDict([("Form", "-mişdi_past"), ("Person-Number", "3_plur")]))]),
             OrderedDict([("getdilər", OrderedDict([("Form", "-di_past"), ("Person-Number", "3_plur")]))]),
             OrderedDict([("gedirlər", OrderedDict([("Form", "present"), ("Person-Number", "3_plur")]))]),
             OrderedDict([("gedəcəklər", OrderedDict([("Form", "fut_def"), ("Person-Number", "3_plur")]))]),
             OrderedDict([("gedərlər", OrderedDict([("Form", "fut_indef"), ("Person-Number", "3_plur")]))]),
             OrderedDict([("getsinlər", OrderedDict([("Form", "imp"), ("Person-Number", "3_plur")]))]),
             OrderedDict([("gedələr", OrderedDict([("Form", "arzu"), ("Person-Number", "3_plur")]))]),
             OrderedDict([("getməlidirlər", OrderedDict([("Form", "vacib"), ("Person-Number", "3_plur")]))]),
             OrderedDict([("gedəsidirlər", OrderedDict([("Form", "lazım"), ("Person-Number", "3_plur")]))]),
             OrderedDict([("getsələr", OrderedDict([("Form", "şərt"), ("Person-Number", "3_plur")]))]),
             OrderedDict([("getməkdən", OrderedDict([("Form", "inf"), ("Case", "abl")]))])
             ]
                                    )])
        fact_result = self.test_extractor.download_verb_tables(test_data)
        self.assertEqual(true_result, fact_result)

if __name__ == '__main__':
    unittest.main()