from nlingua.tokenizers.base import BaseTokenizer

class WordTokenizer(BaseTokenizer):
    def tokenize(self, s: str):
        return s.split(self._split_string)