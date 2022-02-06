import sys

sys.path.insert(0, "../nlingua")

from nlingua.taggers import SimpleTagger

if __name__ == '__main__':
    s = SimpleTagger("NN")
    print(s.tag("This is a string".split(" ")))