from polyglossa.stemmers.porter import PorterStemmer
from nltk.stem import porter

if __name__ == '__main__':
    l = [
        "caresses",
        "relational",
        "conditional",
        "rational",
        "valenci",
        "hesitanci",
        "digitizer",
        "conformabli",
        "radicalli",
        "differentli",
        "vileli",
        "analogousli",
        "vietnamization",
        "predication",
        "operator",
        "feudalism",
        "decisiveness",
        "hopefulness",
        "callousness",
        "formaliti",
        "sensitiviti",
        "sensibiliti",
        "nationalism",
        "triplicate",
        "formative",
        "formalize",
        "electriciti",
        "electrical",
        "hopeful",
        "goodness",
        "revival",
        "allowance",
        "inference",
        "airliner",
        "gyroscopic",
        "adjustable",
        "defensible",
        "irritant",
        "replacement",
        "adjustment",
        "dependent",
        "adoption",
        "homologou",
        "communism",
        "activate",
        "angulariti",
        "homologous",
        "effective",
        "bowdlerize",
        "probate",
        "rate",
        "cease",
        "controll",
        "roll",
        "die",
        "skies",
        "lying",
        "dying",
        "atlas",
        "sky",
        "cosmos",
        "potatoes",
        "tomatoes",
        "grandayy",
        "ponies",
        "flies"
    ]

    stemmer = PorterStemmer()
    stemmer2 = porter.PorterStemmer()
    errors = 0

    for x in l:
        if stemmer.stem(x) != stemmer2.stem(x):
            errors += 1
            print(stemmer.stem(x), stemmer2.stem(x))
    print(errors)