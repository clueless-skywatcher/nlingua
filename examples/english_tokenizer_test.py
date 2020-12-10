from nlingua.tokenizers import StringTokenizer

if __name__ == '__main__':
    tok = StringTokenizer(' ')
    print(tok.tokenize("The quick brown fox jumped over the lazy dog"))