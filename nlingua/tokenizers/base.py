class BaseTokenizer:
    def __init__(self, split_string = ' '):
        self._split_string = split_string

    def tokenize(self, s):
        pass