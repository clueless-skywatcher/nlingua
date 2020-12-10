from nlingua.stemmers import GermanStemmer
from nltk.stem.snowball import GermanStemmer as NLTKGermanStemmer
import codecs

if __name__ == '__main__':
    l = []
    with codecs.open("german_words.txt", encoding = "utf-8", mode = "r") as f:
        words = f.readlines()

    words = [x[:-1] for x in words]

    correct = 0
    stemmer = GermanStemmer()
    stemmer2 = NLTKGermanStemmer()
    for word in words:
        a = stemmer.stem(word)
        b = stemmer2.stem(word)
        if a == b:
            correct += 1
        else:
            print(word, a, b)

    print(f"{correct}/{len(words)} correct")