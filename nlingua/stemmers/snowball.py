from nlingua.stemmers.base import BaseStemmer
from nlingua.constants import ENGLISH_STOPWORDS, GERMAN_STOPWORDS

class SnowballStemmer(BaseStemmer):
    def __init__(self, language = 'en'):
        self.language = language
        self.VOWELS = {}

    def _find_longest_suffix_of(self, s, suffixes):
        suffixes = sorted(suffixes, key = len, reverse = True)
        for suffix in suffixes:
            if self._ends_with(s, suffix):
                return suffix
        return ""

    def _r1(self, s):
        for i in range(len(s) - 2):
            if self._is_vowel(s[i]) and self._is_consonant(s[i + 1]):
                return s[i + 2:]
        return None

    def _r2(self, s):
        r1 = self._r1(s)
        return None if r1 == None else self._r1(r1)

    def _r1_r2(self, s):
        return self._r1(s), self._r2(s)

    def _preceding_part(self, s, suffix):
        return s[:-len(suffix)]

    def _is_consonant(self, c):
        return not c in self.VOWELS

    def _is_vowel(self, c):
        return not self._is_consonant(c)

    def _has_vowel(self, s):
        for c in s:
            if c in self.VOWELS:
                return True
        return False


class EnglishStemmer(SnowballStemmer):
    def __init__(self):
        super().__init__(language = 'en')
        self.VOWELS = "aeiouy"
        self.DOUBLES = {"bb", "dd", "ff", "gg", "mm", "nn", "pp", "rr", "tt"}
        self.LI_ENDINGS = "cdeghkmnrt"

        self.EXCEPTION_1 = {
            "ski" : ["skis"],
            "sky" : ["skies"],
            "die" : ["dying"],
            "lie" : ["lying"],
            "tie" : ["tying"],
            "idl" : ["idly"],
            "earli" : ["early"],
            "onli" : ["only"],
            "singl" : ["singly"]
        }

        self.EXCEPTION_2 = {"inning", "canning", "herring", "exceed", "succeed", "proceed", "outing"}

        self.INVARIANT_FORMS = {"sky", "atlas", "howe", "news", "bias", "andes"}

        self.SPECIAL_P1_PREFIXES = {"gener", "commun", "arsen"}

    def _is_short(self, s):
        if (
            self._is_consonant(s[len(s) - 3])
            and self._is_vowel(s[len(s) - 2])
            and self._is_consonant(s[len(s) - 1])
            and s[len(s) - 1] not in "wxY"
            and self._r1(s) == None
        ):
            return True
        return False

    def _is_short_syllable(self, s, i):
        return (
            self._is_vowel(s[i])
            and i == 0
            and not self._is_vowel(s[i + 1])
        ) or (
            self._is_vowel(s[i])
            and max(i, -i) > 0
            and max(i, -i) < len(s)
            and not self._is_vowel(s[i - 1])
            and not self._is_vowel(s[i + 1])
            and s[i + 1] not in "wxY"
        )

    def _remove_init_apos(self, s):
        if s[0] == '\'':
            return s[1:]
        return s

    def _set_y(self, s):
        if s[0] == 'y':
            return 'Y' + s[1:]
        for i in range(1, len(s)):
            if self._is_vowel(s[i - 1]) and s[i] == 'y':
                s = s[:i] + 'Y' + s[i + 1:]
        return s

    def _step_0(self, s):
        return self._replace_suffix(s, self._find_longest_suffix_of(s, ["\'", "\'s", "\'s\'"]), "")

    def _step_1a(self, s):
        suffixes = ["sses", "ied", "ies", "s", "us", "ss"]
        s = self._apply_rule(s, rule_list = [
                [(self._find_longest_suffix_of(s, suffixes) == "sses",), "sses", "ss"],
                [(self._find_longest_suffix_of(s, suffixes) == "ied", len(s[:-3]) > 1), "ied", "i"],
                [(self._find_longest_suffix_of(s, suffixes) == "ied", len(s[:-3]) <= 1), "ied", "ie"],
                [(self._find_longest_suffix_of(s, suffixes) == "ies", len(s[:-3]) > 1), "ies", "i"],
                [(self._find_longest_suffix_of(s, suffixes) == "ies", len(s[:-3]) <= 1), "ies", "ie"],
                [(self._find_longest_suffix_of(s, suffixes) == "s", self._has_vowel(s[:-2])), "s", ""]
            ]
        )
        return s

    def _step_1b(self, s):
        r1, r2 = self._r1_r2(s)

        for x in self.SPECIAL_P1_PREFIXES:
            if s.startswith(x):
                r1 = s[len(x):]
                break

        suffixes = ["eed", "eedly", "ee", "ed", "edly", "ing", "ingly"]
        longest_suffix = self._find_longest_suffix_of(s, suffixes)
        if longest_suffix in {"eed", "eedly"}:
            s = self._apply_rule(s, rule_list = [
                [(longest_suffix in r1,), longest_suffix, "ee"]
            ])
        elif longest_suffix in {"ed", "edly", "ing", "ingly"}:
            if self._has_vowel(self._preceding_part(s, longest_suffix)):
                s = self._replace_suffix(s, longest_suffix, "")

            if any([self._ends_with(s, "at"), self._ends_with(s, "bl"), self._ends_with(s, "iz")]):
                s = s + "e"
            elif any([self._ends_with(s, x) for x in self.DOUBLES]):
                s = self._replace_suffix(s, s[-1], "")
            elif self._is_short(s):
                s = s + "e"
        return s

    def _step_1c(self, s):
        return self._apply_rule(s, [
            [(self._ends_with(s, "y") or self._ends_with(s, "Y"), self._is_consonant(s[-2]), len(self._preceding_part(s, "y")) > 1), s[-1], "i"]
        ])

    def _step_2(self, s):
        r1 = self._r1(s)

        suffixes = [
            "tional", "enci", "anci",
            "abli", "entli", "izer",
            "ization", "ational", "ation",
            "ator", "alism", "aliti", "alli",
            "fulness", "ousli", "ousness",
            "iveness", "iviti", "biliti", "bli",
            "ogi", "fulli", "lessli", "li"
        ]

        longest_suffix = self._find_longest_suffix_of(s, suffixes)
        if r1 is not None:
            if longest_suffix in r1:
                s = self._apply_rule(s, [
                    [(longest_suffix == "tional",), "tional", "tion"],
                    [(longest_suffix == "enci",), "enci", "ence"],
                    [(longest_suffix == "anci",), "anci", "ance"],
                    [(longest_suffix == "abli",), "abli", "able"],
                    [(longest_suffix == "entli",), "entli", "ent"],
                    [(longest_suffix == "izer",), "izer", "ize"],
                    [(longest_suffix == "ization",), "ization", "ize"],
                    [(longest_suffix == "ational",), "ational", "ate"],
                    [(longest_suffix == "ation",), "ation", "ate"],
                    [(longest_suffix == "ator",), "ator", "ate"],
                    [(longest_suffix == "alism",), "alism", "al"],
                    [(longest_suffix == "aliti",), "aliti", "al"],
                    [(longest_suffix == "alli",), "alli", "al"],
                    [(longest_suffix == "fulness",), "fulness", "ful"],
                    [(longest_suffix == "ousli",), "ousli", "ous"],
                    [(longest_suffix == "ousness",), "ousness", "ous"],
                    [(longest_suffix == "iveness",), "iveness", "ive"],
                    [(longest_suffix == "iviti",), "iviti", "ive"],
                    [(longest_suffix == "biliti",), "biliti", "ble"],
                    [(longest_suffix == "bli",), "bli", "ble"],
                    [(longest_suffix == "ogi", self._preceding_part(s, "ogi")[-1] == "l"), "ogi", "og"],
                    [(longest_suffix == "fulli",), "fulli", "ful"],
                    [(longest_suffix == "lessli",), "lessli", "less"],
                    [(longest_suffix == "li", any([self._ends_with(self._preceding_part(s, "li"), x) for x in self.LI_ENDINGS])), "li", ""],
                ])

        return s

    def _step_3(self, s):
        r1, r2 = self._r1_r2(s)
        suffixes = [
            "tional", "ational",
            "alize", "icate",
            "iciti", "ical",
            "ful", "ness",
            "ative"
        ]

        longest_suffix = self._find_longest_suffix_of(s, suffixes)

        if r1 is not None:
            if longest_suffix in r1:
                s = self._apply_rule(s, rule_list = [
                    [(longest_suffix == "tional",), "tional", "tion"],
                    [(longest_suffix == "ational",), "ational", "ate"],
                    [(longest_suffix == "alize",), "alize", "al"],
                    [(longest_suffix == "icate",), "icate", "ic"],
                    [(longest_suffix == "iciti",), "iciti", "ic"],
                    [(longest_suffix == "ical",), "ical", "ic"],
                    [(longest_suffix == "ful",), "ful", ""],
                    [(longest_suffix == "ness",), "ness", ""],
                ])
                if r2 is not None:
                    s = self._apply_rule(s, rule_list = [
                        [(longest_suffix == "ative", longest_suffix in r2), "ative", ""]
                    ])

        return s

    def _step_4(self, s):
        r2 = self._r2(s)
        suffixes = [
            "al", "ance", "ence",
            "er", "ic", "able", "ible",
            "ant", "ement", "ment", "ent",
            "ism", "ate", "iti", "ous", "ive",
            "ize"
        ]

        longest_suffix = self._find_longest_suffix_of(s, suffixes + ["ion"])

        if r2 is not None:
            if longest_suffix in r2:
                if longest_suffix == "ion" and s[-4] in ("s", "t"):
                    s = self._replace_suffix(s, longest_suffix, "")
                elif longest_suffix in suffixes:
                    s = self._replace_suffix(s, longest_suffix, "")

        return s

    def _step_5(self, s):
        r1, r2 = self._r1_r2(s)
        if r2 is not None:
            s = self._apply_rule(s, rule_list = [
                [(self._ends_with(s, "e"), "e" in r2 or ("e" in r1 and not self._is_short_syllable(s, -2))), "e", ""],
                [(self._ends_with(s, "l"), "l" in r2, s[-2] == "l"), "l", ""]
            ])
        return s

    def stem(self, s):
        s = s.lower()
        if len(s) <= 2 or s in ENGLISH_STOPWORDS:
            return s

        if s in self.INVARIANT_FORMS:
            return s

        for x in self.EXCEPTION_1:
            if s in self.EXCEPTION_1[x]:
                return x

        s = self._step_0(s)

        s = self._step_1a(s)
        if s in self.EXCEPTION_2:
            return s

        s = self._step_1b(s)
        s = self._step_1c(s)
        s = self._step_2(s)
        s = self._step_3(s)
        s = self._step_4(s)
        s = self._step_5(s)

        return s.lower()

class GermanStemmer(SnowballStemmer):
    def __init__(self):
        super().__init__(language = 'de')
        self.VOWELS = "aeiouy\xE4\xF6\xFC"
        self.S_ENDINGS = "bdfghklmnrt"
        self.ST_ENDINGS = self.S_ENDINGS.replace("r", "")
        self.UMLAUT_DICT = {
            "ä" : "a",
            "ö" : "o",
            "ü" : "u"
        }
        self.ESZETT = "\xDF"

    def _replace_ss(self, s):
        i = 0
        while i < len(s):
            if s[i] == self.ESZETT:
                s = self._replace_char(s, "ss", i)
            i += 1
        return s

    def _change_uy(self, s):
        for i in range(1, len(s) - 1):
            if s[i] in {"u", "y"} and self._is_vowel(s[i - 1]) and self._is_vowel(s[i + 1]):
                s = self._replace_char(s, s[i].upper(), i)
        return s

    def _german_r1(self, s):
        r1 = self._r1(s)
        if r1 is None:
            return r1
        for i in range(1, len(s)):
            if self._is_vowel(s[i - 1]) and self._is_consonant(s[i]):
                if 0 < len(s[: i + 1]) < 3:
                    r1 = s[3:]
                elif len(s[: i + 1]) == 0:
                    return s
                break
        return r1

    def _step_1(self, s):
        r1 = self._german_r1(s)

        suffixes = {"em", "ern", "er", "e", "en", "es", "s"}
        longest_suffix = self._find_longest_suffix_of(s, suffixes)

        if r1 is not None:
            if longest_suffix in {"em", "ern", "er"} and longest_suffix in r1:
                s = self._replace_suffix(s, longest_suffix, "")
            elif longest_suffix in {"e", "en", "es"} and longest_suffix in r1:
                s = self._replace_suffix(s, longest_suffix, "")
                if self._ends_with(s, "niss"):
                    s = s[:-1]
            elif longest_suffix == "s" and longest_suffix in r1:
                if s[-2] in self.S_ENDINGS:
                    s = self._replace_suffix(s, longest_suffix, "")

        return s

    def _step_2(self, s):
        suffixes = {"en", "er", "est", "st"}
        r1 = self._german_r1(s)
        longest_suffix = self._find_longest_suffix_of(s, suffixes)
        if r1 is not None:
            s = self._apply_rule(s, [
                [(longest_suffix in {"en", "er", "est"}, longest_suffix in r1), longest_suffix, ""],
                [(longest_suffix == "st",
                  any([self._ends_with(s, x + longest_suffix) for x in self.ST_ENDINGS]),
                  len(s[:-3]) >= 3,
                  longest_suffix in r1), longest_suffix, ""]
            ])

        return s

    def _step_3(self, s):
        r1 = self._german_r1(s)
        r2 = self._r2(s)

        suffixes = {"end", "ung", "ig", "ik", "isch", "lich", "heit", "keit"}

        longest_suffix = self._find_longest_suffix_of(s, suffixes)

        if r1 is not None and r2 is not None:
            if longest_suffix in {"end", "ung"} and longest_suffix in r2:
                s = self._replace_suffix(s, longest_suffix, "")
                s = self._apply_rule(s, [
                    [(self._ends_with(s, "ig"),
                      "ig" in r2,
                      s[-3] != 'e'), "ig", ""]
                ])
            elif longest_suffix in {"ig", "ik", "isch"} and longest_suffix in r2:
                s = self._apply_rule(s, [
                    [(s[-len(longest_suffix) - 1] != "e",), longest_suffix, ""]
                ])
            elif longest_suffix in {"lich", "heit"} and longest_suffix in r2:
                s = self._replace_suffix(s, longest_suffix, "")
                preceding_suffix = s[-2:]
                s = self._apply_rule(s, [
                    [(preceding_suffix in {"er", "en"}, preceding_suffix in r1), preceding_suffix, ""]
                ])
            elif longest_suffix == "keit" and longest_suffix in r2:
                s = self._replace_suffix(s, longest_suffix, "")
                s = self._apply_rule(s, [
                    [(self._ends_with(s, "lich"), "lich" in r2), "lich", ""],
                    [(self._ends_with(s, "ig"), "ig" in r2), "ig", ""]
                ])

        return s

    def _change_umlauts(self, s):
        for i in range(len(s)):
            if s[i] in self.UMLAUT_DICT.keys():
                s = self._replace_char(s, self.UMLAUT_DICT[s[i]], i)
        return s

    def stem(self, s):
        s = s.lower()
        if len(s) <= 2 or len(s) in GERMAN_STOPWORDS:
            s = self._change_umlauts(s)
            s = self._replace_ss(s)
            return s

        s = self._replace_ss(s)
        s = self._change_uy(s)

        s = self._step_1(s)
        s = self._step_2(s)
        s = self._step_3(s)

        s = s.lower()
        s = self._change_umlauts(s)

        return s



