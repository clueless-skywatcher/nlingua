class StemmerException(Exception):
    pass

class PorterStemmer():
    '''
    Stemmer designed by Martin Porter in his paper.
    Reference: https://tartarus.org/martin/PorterStemmer/def.txt
    '''

    def __init__(self):
        self.VOWELS = "aeiou"
        self.IRREGULAR_FORMS = {
            "die" : ["dying"],
            "ski" : ["skis"],
            "sky" : ["skies", "sky"],
            "lie" : ["lying"],
            "tie" : ["tying"],
            "idl" : ["idly"],
            "gentl" : ["gently"],
            "ugli" : ["ugly"],
            "earli" : ["early"],
            "only" : ["onli"],
            "singl" : ["singly"]
        }

        self.INVARIANT_FORMS = {"sky", "news", "howe", "atlas", "cosmos", "bias", "andes"}

    def _is_consonant(self, c: str):
        if len(c) != 1:
            raise StemmerException("Input must be character")
        return c not in self.VOWELS

    def _is_vowel_in_string(self, s, index):
        if max(index, -index) > 0 and s[index] == 'y':
            return self._is_consonant(s[index - 1])
        return not self._is_consonant(s[index])

    def _has_vowel(self, s: str):
        for i in range(len(s)):
            if self._is_vowel_in_string(s, i):
                return True
        return False

    def _ends_with(self, s: str, ends: str):
        return s[-len(ends):] == ends

    def _replace_suffix(self, s: str, ends_with: str, rep_with: str):
        if self._ends_with(s, ends_with):
            s = s[:-len(ends_with)] + rep_with
        return s

    def _has_double_consonant(self, s: str):
        if len(s) > 2:
            return self._is_consonant(s[-1]) and self._is_consonant(s[-2])
        return False

    def _check_cvc(self, s: str):
        if len(s) < 3:
            return False
        condition1 = not self._is_vowel_in_string(s, -3)
        condition2 = self._is_vowel_in_string(s, -2)
        condition3 = not self._is_vowel_in_string(s, -1) and s[-1] not in ["w", "x", "y"]
        return all([condition1, condition2, condition3])

    def _apply_rule(self, s, rule_list):
        for rule in rule_list:
            condition = rule[0]
            suffix_check = rule[1]
            suffix_replace = rule[2]
            if condition is not None:
                if all(condition) == True:
                    s = self._replace_suffix(s, suffix_check, suffix_replace)
                    break
        return s

    def _step_1a(self, s: str):
        self._apply_rule(s, rule_list=[
            [None, "sses", "ss"],
            [None, "ies", "i"],
            [None, "ss", "ss"],
            [None, "s", ""]
        ])
        return s

    def _measure_count(self, s: str):
        vc = ""
        for i in range(len(s)):
            if self._is_vowel_in_string(s, i):
                vc = vc + "v"
            else:
                vc = vc + "c"
        return vc.count("vc")

    def _step_1b_a(self, s: str):
        if self._ends_with(s, "at"):
            s = self._replace_suffix(s, "at", "ate")
        elif self._ends_with(s, "bl"):
            s = self._replace_suffix(s, "bl", "ble")
        elif self._ends_with(s, "iz"):
            s = self._replace_suffix(s, "iz", "ize")
        elif self._has_double_consonant(s) and not (self._ends_with(s, "l") or self._ends_with(s, "s") or self._ends_with(s, "z")):
            s = self._replace_suffix(s, s[-2:], s[-1])
        elif self._measure_count(s) == 1 and self._check_cvc(s):
            s += "e"

        return s

    def _stem_measure_and_ends_with(self, s: str, suffix: str, min_m: int = 0, min_m_equal = False):
        if min_m_equal == True:
            return self._measure_count(s[:-len(suffix)]) == min_m and self._ends_with(s, suffix)
        return self._measure_count(s[:-len(suffix)]) > min_m and self._ends_with(s, suffix)

    def _step_1b(self, s: str):
        if self._ends_with(s, "eed"):
            stem = self._replace_suffix(s, "eed", "")
            if self._measure_count(stem) > 0:
                return stem + "ee"
            else:
                return s
        elif self._has_vowel(s[:-2]) and self._ends_with(s, "ed"):
            s = self._replace_suffix(s, "ed", "")
            s = self._step_1b_a(s)
        elif self._has_vowel(s[:-3]) and self._ends_with(s, "ing"):
            s = self._replace_suffix(s, "ing", "")
            s = self._step_1b_a(s)
        return s

    def _step_1c(self, s):
        if self._has_vowel(s[:-1]) and self._ends_with(s, "y"):
            s = self._replace_suffix(s, "y", "i")
        return s

    def _step_2(self, s):
        s = self._apply_rule(s, rule_list = [
            [(self._stem_measure_and_ends_with(s, "ational"),), "ational", "ate"],
            [(self._stem_measure_and_ends_with(s, "tional"),), "tional", "tion"],
            [(self._stem_measure_and_ends_with(s, "enci"),), "enci", "ence"],
            [(self._stem_measure_and_ends_with(s, "anci"),), "anci", "ance"],
            [(self._stem_measure_and_ends_with(s, "izer"),), "izer", "ize"],
            [(self._stem_measure_and_ends_with(s, "abli"),), "abli", "able"],
            [(self._stem_measure_and_ends_with(s, "alli"),), "alli", "al"],
            [(self._stem_measure_and_ends_with(s, "entli"),), "entli", "ent"],
            [(self._stem_measure_and_ends_with(s, "eli"),), "eli", "e"],
            [(self._stem_measure_and_ends_with(s, "ousli"),), "ousli", "ous"],
            [(self._stem_measure_and_ends_with(s, "ization"),), "ization", "ize"],
            [(self._stem_measure_and_ends_with(s, "ation"),), "ation", "ate"],
            [(self._stem_measure_and_ends_with(s, "ator"),), "ator", "ate"],
            [(self._stem_measure_and_ends_with(s, "ation"),), "ation", "ate"],
            [(self._stem_measure_and_ends_with(s, "alism"),), "alism", "al"],
            [(self._stem_measure_and_ends_with(s, "iveness"),), "iveness", "ive"],
            [(self._stem_measure_and_ends_with(s, "fulness"),), "fulness", "ful"],
            [(self._stem_measure_and_ends_with(s, "ousness"),), "ousness", "ous"],
            [(self._stem_measure_and_ends_with(s, "aliti"),), "aliti", "al"],
            [(self._stem_measure_and_ends_with(s, "iviti"),), "iviti", "ive"],
            [(self._stem_measure_and_ends_with(s, "biliti"),), "biliti", "ble"],
        ])

        return s

    def _step_3(self, s):
        s = self._apply_rule(s, rule_list = [
            [(self._stem_measure_and_ends_with(s, "icate"),), "icate", "ic"],
            [(self._stem_measure_and_ends_with(s, "ative"),), "ative", ""],
            [(self._stem_measure_and_ends_with(s, "alize"),), "alize", "al"],
            [(self._stem_measure_and_ends_with(s, "iciti"),), "iciti", "ic"],
            [(self._stem_measure_and_ends_with(s, "ical"),), "ical", "ic"],
            [(self._stem_measure_and_ends_with(s, "ful"),), "ful", ""],
            [(self._stem_measure_and_ends_with(s, "ness"),), "ness", ""],
        ])

        return s

    def _step_4(self, s):
        s = self._apply_rule(s, rule_list = [
            [(self._stem_measure_and_ends_with(s, "al", 1),), "al", ""],
            [(self._stem_measure_and_ends_with(s, "ance", 1),), "ance", ""],
            [(self._stem_measure_and_ends_with(s, "ence", 1),), "ence", ""],
            [(self._stem_measure_and_ends_with(s, "er", 1),), "er", ""],
            [(self._stem_measure_and_ends_with(s, "ic", 1),), "ic", ""],
            [(self._stem_measure_and_ends_with(s, "able", 1),), "able", ""],
            [(self._stem_measure_and_ends_with(s, "ible", 1),), "ible", ""],
            [(self._stem_measure_and_ends_with(s, "ant", 1),), "ant", ""],
            [(self._stem_measure_and_ends_with(s, "ement", 1),), "ement", ""],
            [(self._stem_measure_and_ends_with(s, "ment", 1),), "ment", ""],
            [(self._stem_measure_and_ends_with(s, "ent", 1),), "ent", ""],
            [(self._stem_measure_and_ends_with(s, "ion", 1), (self._ends_with(s, "s"), self._ends_with(s, "t"))), "ion", ""],
            [(self._stem_measure_and_ends_with(s, "ou", 1),), "ou", ""],
            [(self._stem_measure_and_ends_with(s, "ism", 1),), "ism", ""],
            [(self._stem_measure_and_ends_with(s, "ate", 1),), "ate", ""],
            [(self._stem_measure_and_ends_with(s, "iti", 1),), "iti", ""],
            [(self._stem_measure_and_ends_with(s, "ous", 1),), "ous", ""],
            [(self._stem_measure_and_ends_with(s, "ive", 1),), "ive", ""],
            [(self._stem_measure_and_ends_with(s, "ize", 1),), "ize", ""],
        ])

        return s

    def _step_5a(self, s):
        s = self._apply_rule(s, rule_list = [
            [(self._stem_measure_and_ends_with(s, "e", 1),), "e", ""],
            [(self._stem_measure_and_ends_with(s, "e", 1, True), not self._check_cvc(s[:-1])), "e", ""]
        ])
        return s

    def _step_5b(self, s):
        s = self._apply_rule(s, rule_list = [
            [(self._stem_measure_and_ends_with(s, s[-1], 1), self._has_double_consonant(s), self._ends_with(s[:-1], "l")), s[-1], ""]
        ])
        return s

    def stem(self, word: str):
        if " " in word:
            raise StemmerException("Cannot stem multiple words")
        s = word.lower()

        for x in self.IRREGULAR_FORMS:
            if s in self.IRREGULAR_FORMS[x]:
                return x

        if s in self.INVARIANT_FORMS:
            return s

        s = self._step_1a(s)
        s = self._step_1b(s)
        s = self._step_1c(s)
        s = self._step_2(s)
        s = self._step_3(s)
        s = self._step_4(s)
        s = self._step_5a(s)
        s = self._step_5b(s)

        return s
