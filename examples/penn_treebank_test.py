import sys

sys.path.insert(0, "../nlingua")

from nlingua.corpora.penn_treebank import PennTreebankCorpus

if __name__ == '__main__':
    p = PennTreebankCorpus(download = False)
    x = p.files()[:2]
    print(x)
    import pprint
    pprint.pprint(p.tagged_words(['wsj.pos', 'wsj_0002.pos']))