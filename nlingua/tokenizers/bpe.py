import re
import collections
import string

class BPETokenizer():
    def __init__(self, corpus_file, num_merges = 10, case_sensitive = True, remove_punct = True):
        self.num_merges = num_merges
        self.corpus_file = corpus_file
        self.case_sensitive = case_sensitive
        self.remove_punct = remove_punct
        self._prepare_vocab()

    def _prepare_vocab(self):
        vocab = collections.defaultdict(int)
        with open(self.corpus_file, 'r', encoding='utf-8') as f:
            for line in f:
                if self.remove_punct:
                    for c in string.punctuation:
                        line = line.replace(c, '')
                words = [word.lower() if self.case_sensitive else word for word in line.strip().split()]
                for word in words:
                    vocab[' '.join(list(word)) + ' </w>'] += 1
        self.vocab = vocab

    def _get_stats(self):
        pairs = collections.defaultdict(int)
        for word, freq in self.vocab.items():
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[symbols[i], symbols[i + 1]] += freq
        return pairs

    def _merge_vocab(self, pair, v_in):
        v_out = {}
        bigram = re.escape(' '.join(pair))
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')

        for word in v_in:
            w_out = p.sub(''.join(pair), word)
            v_out[w_out] = v_in[word]

        self.vocab = v_out

    def tokenize(self):
        self._prepare_vocab()
        final_tokens = {}

        for _ in range(self.num_merges):
            pairs = self._get_stats()
            best = max(pairs, key=pairs.get)

            self._merge_vocab(best, self.vocab)      
            tokens = collections.defaultdict(int)
            for word, freq in self.vocab.items():
                word_tokens = word.split()
                for token in word_tokens:
                    tokens[token] += freq
                final_tokens = tokens

        self.token_dict = final_tokens

        return sorted(
            list(self.token_dict.keys()), 
            key = lambda x: self.token_dict[x], 
            reverse = True
        )

if __name__ == '__main__':
    import json
    bpe = BPETokenizer('sample.txt', 50)
    tokens = bpe.tokenize()
    print(tokens)
    