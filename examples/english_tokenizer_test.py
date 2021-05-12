from nlingua.tokenizers import WordTokenizer

if __name__ == '__main__':
    tok = WordTokenizer(' ')
    print(tok.tokenize("The quick brown fox jumped over the lazy dog"))