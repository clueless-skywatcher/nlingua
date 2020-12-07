from polyglossa.stemmers.base import BaseStemmer

class SnowballStemmer(BaseStemmer):
    def __init__(self):
        self.VOWELS = "aeiouy"
        self.DOUBLES = {"bb", "dd", "ff", "gg", "mm", "nn", "pp", "rr", "tt"}
        self.LI_ENDINGS = {'c', 'd', 'e', 'g', 'h', 'k', 'm', 'n', 'r', 't'}

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

    def stem(self, s):
        if len(s) <= 2:
            return s
        s = s.lower()
        s = self._step_0(s)
        s = self._step_1a(s)
        return s

if __name__ == "__main__":
    snw = SnowballStemmer()
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
    for x in l3:
        print(snw._step_1a(x))