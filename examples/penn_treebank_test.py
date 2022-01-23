import sys

sys.path.insert(0, "../nlingua")

from nlingua.corpora.penn_treebank import PennTreebankCorpus

if __name__ == '__main__':
    p = PennTreebankCorpus(download = False)
    print(p.tagged_sentences()[10])