from nlingua.tokenizers.base import BaseTokenizer

class StringTokenizer(BaseTokenizer):
    def tokenize(self, s: str):
        return s.split(self._split_string)