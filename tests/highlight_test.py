import os
from unittest import TestCase

from ruamel.yaml.error import StringMark
from ruamel.yaml.tokens import Token
from ruamel.yaml.scanner import ScannerError

from vim_yaml.highlight import Highlighter


class HighlightTest(TestCase):

    def setUp(self):
        self.highlighter = Highlighter()

    def split_region(self, start_line, start_column, end_line, end_column):
        token = Token(StringMark(None, 0, start_line, start_column, None, None),
                      StringMark(None, 0, end_line, end_column, None, None))
        return list(self.highlighter.split_region(token))

    @staticmethod
    def read_yaml_file(f):
        with open(os.path.join('tests/samples', f), encoding='utf-8') as src:
            return src.read()

    def test_select_token(self):
        # 1 line
        self.assertEqual([(0, 1, 5)],
                         self.split_region(0, 1, 0, 5))
        # 2 lines
        self.assertEqual([(0, 1, -1), (1, 0, 5)],
                         self.split_region(0, 1, 1, 5))
        # 3 lines
        self.assertEqual([(0, 1, -1), (1,), (2, 0, 5)],
                         self.split_region(0, 1, 2, 5))

    def test_scan_simple_dictionary(self):
        document = self.read_yaml_file('dict.yml')
        self.highlighter.end = len(document.splitlines())
        try:
            print(list(self.highlighter.highlight(document)))
        except ScannerError as e:
            print(e)
