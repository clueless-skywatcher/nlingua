from nlingua.stemmers.base import BaseStemmer

class EnglishHarmanSStemmer(BaseStemmer):
    def stem(self, s):
        if s.endswith("ies") and not (s.endswith("eies") or s.endswith("aies")):
            self._replace_suffix(s, "ies", "y")
        elif s.endswith("es") and not (s.endswith("aes") or s.endswith("ees") or s.endswith("oes")):
            self._replace_suffix(s, "es", "e")
        elif s.endswith("s") and not (s.endswith("us") or s.endswith("ees") or s.endswith("ss")):
            self._replace_suffix(s, "s", "")

        return s