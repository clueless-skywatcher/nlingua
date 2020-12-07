from polyglossa.stemmers.porter import PorterStemmer
from polyglossa.stemmers.snowball import SnowballStemmer
from nltk.stem import porter
from nltk.stem.snowball import EnglishStemmer

if __name__ == "__main__":
    snw = SnowballStemmer()
    snw2 = EnglishStemmer()

    l2 = [
        "bed",
        "shred",
        "shed",
        "bead",
        "embed",
        "beds"
    ]

    l3 = [
        "ties",
        "cries",
        "gas",
        "this",
        "gaps",
        "kiwis",
        "lasses",
        "curried",
        "melodious",
        "ass"
    ]

    l4 = [
        "agreed",
        "disagreedly",
        "guaranteed",
        "luxuriated",
        "hopping",
        "hoped",
        "hurriedly"
    ]

    l5 = [
        "cry",
        "by",
        "say",
        "bY",
        "crY",
        "warranty"
    ]

    l6 = [
        "emotional",
        "excellency",
        "reluctancy",
        "remarkably",
        "intelligently",
        "energizer",
        "latinization",
        "elevational",
        "generation",
        "operator",
        "nationalism",
        "criticality",
        "finally",
        "forgetfulness",
        "seriously",
        "obnoxiousness",
        "responsiveness",
        "positivity",
        "responsibility",
        "possibly",
        "homology",
        "gleefully",
        "carelessly",
        "exactly",
        "generate",
        "general",
        "generic"
    ]
    for x in l6:
        s1 = snw.stem(x)
        s2 = snw2.stem(x)
        if s1 != s2:
            print(s1, s2)