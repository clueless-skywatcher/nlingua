from polyglossa.stemmers.base import BaseStemmer

class SnowballStemmer(BaseStemmer):
    def __init__(self, language = 'en'):
        self.language = language

class EnglishStemmer(SnowballStemmer):
    def __init__(self):
        super().__init__(language = 'en')
        self.VOWELS = "aeiouy"
        self.DOUBLES = {"bb", "dd", "ff", "gg", "mm", "nn", "pp", "rr", "tt"}
        self.LI_ENDINGS = {'c', 'd', 'e', 'g', 'h', 'k', 'm', 'n', 'r', 't'}

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

    def _is_consonant(self, c):
        return not c in self.VOWELS

    def _is_vowel(self, c):
        return not self._is_consonant(c)

    def _has_vowel(self, s):
        for c in s:
            if c in self.VOWELS:
                return True
        return False

    def _r1(self, s):
        for i in range(len(s) - 2):
            if self._is_vowel(s[i]) and self._is_consonant(s[i + 1]):
                return s[i + 2:]
        return None

    def _r2(self, s):
        r1 = self._r1(s)
        return None if r1 == None else self._r1(r1)

    def _is_short(self, s):
        if (
            self._is_consonant(s[len(s) - 3])
            and self._is_vowel(s[len(s) - 2])
            and self._is_consonant(s[len(s) - 1])
            and s[len(s) - 1] not in {"w", "x", "Y"}
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
            and s[i + 1] not in ("w", "x", "Y")
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

    def _find_longest_suffix_of(self, s, suffixes):
        suffixes = sorted(suffixes, key = len, reverse = True)
        for suffix in suffixes:
            if self._ends_with(s, suffix):
                return suffix
        return ""

    def _r1_r2(self, s):
        return self._r1(s), self._r2(s)

    def _preceding_part(self, s, suffix):
        return s[:-len(suffix)]

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
        if len(s) <= 2:
            return s
        s = s.lower()

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