import copy

class BaseSentencizer():
    def _sentencize(self):
        pass

class PlainSentencizer(BaseSentencizer):
    def __init__(self, text, split_chars = ['.', '?', '!', ';'], delimiter = '<s>'):
        self.sentence_list = []
        self.raw = str(text)
        self._split_chars = split_chars
        self.delimiter = delimiter
        self._sentence_index = 0
        self._sentencize()

    def _sentencize(self):
        sentence = self.raw
        for c in self._split_chars:
            sentence = sentence.replace(c, f"c{self.delimiter}")
            self.sentence_list = [x.strip() for x in sentence.split(self.delimiter) if len(x) > 0]

    def __iter__(self):
        return self

    def __next__(self):
        if self._sentence_index < len(self.sentence_list):
            x = self.sentence_list[self._sentence_index]
            self._sentence_index += 1
            return x
        raise StopIteration

