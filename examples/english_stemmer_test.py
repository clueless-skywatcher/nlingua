from nlingua.stemmers import EnglishSnowballStemmer
from nltk.stem.snowball import EnglishStemmer

if __name__ == "__main__":
    snw = EnglishSnowballStemmer()

    l1 = '''
        knack
        knackeries
        knacks
        knag
        knave
        knaves
        knavish
        kneaded
        kneading
        knee
        kneel
        kneeled
        kneeling
        kneels
        knees
        knell
        knelt
        knew
        knick
        knif
        knife
        knight
        knightly
        knights
        knit
        knits
        knitted
        knitting
        knives
        knob
        knobs
        knock
        knocked
        knocker
        knockers
        knocking
        knocks
        knopp
        knot
        knots
        consign
        consigned
        consigning
        consignment
        consist
        consisted
        consistency
        consistent
        consistently
        consisting
        consists
        consolation
        consolations
        consolatory
        console
        consoled
        consoles
        consolidate
        consolidated
        consolidating
        consoling
        consolingly
        consols
        consonant
        consort
        consorted
        consorting
        conspicuous
        conspicuously
        conspiracy
        conspirator
        conspirators
        conspire
        conspired
        conspiring
        constable
        constables
        constance
        constancy
        constant
    '''

    l2 = '''
        knack
        knackeri
        knack
        knag
        knave
        knave
        knavish
        knead
        knead
        knee
        kneel
        kneel
        kneel
        kneel
        knee
        knell
        knelt
        knew
        knick
        knif
        knife
        knight
        knight
        knight
        knit
        knit
        knit
        knit
        knive
        knob
        knob
        knock
        knock
        knocker
        knocker
        knock
        knock
        knopp
        knot
        knot
        consign
        consign
        consign
        consign
        consist
        consist
        consist
        consist
        consist
        consist
        consist
        consol
        consol
        consolatori
        consol
        consol
        consol
        consolid
        consolid
        consolid
        consol
        consol
        consol
        conson
        consort
        consort
        consort
        conspicu
        conspicu
        conspiraci
        conspir
        conspir
        conspir
        conspir
        conspir
        constabl
        constabl
        constanc
        constanc
        constant
    '''

    total = len(l1.split())
    correct = 0
    for x, y in zip(l1.split(), l2.split()):
        s1 = snw.stem(x)
        if s1 == y:
            correct += 1
    print(f"{correct}/{total} correct")

    s1 = EnglishSnowballStemmer().stem_sentence("The quick brown fox jumped over the lazy dog")
    from nlingua.tokenizers import StringTokenizer

    stemmer = EnglishStemmer()
    s2 = StringTokenizer().tokenize("The quick brown fox jumped over the lazy dog")

    for i in range(len(s2)):
        w = stemmer.stem(s2[i])
        s2[i] = w

    s2 = " ".join(s2)

    print(s1 == s2)