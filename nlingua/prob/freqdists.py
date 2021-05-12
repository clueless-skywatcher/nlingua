import itertools
import re

class FrequencyDist:
    def __init__(self, text, case_sensitive = False) -> None:
        self.text = text
        self.case_sensitive = case_sensitive
        self._construct_freqdict(text)

    def _construct_freqdict(self, text):
        WORD_REGEX = r"[a-zA-Z]+"
        d = {}
        text = re.findall(WORD_REGEX, text, flags = re.IGNORECASE)
        for word in text:
            d[word] = d.get(word, 0) + 1
        self._freq_dict = d
        self._freq_dict_concise = dict(itertools.islice(self._freq_dict.items(), 10))
        self._freq_dict_concise = f"{{{*self._freq_dict_concise,}, ...}})"
    
    def keys(self):
        return list(self._freq_dict.keys())

    def values(self):
        return list(self._freq_dict.values())

    def __repr__(self) -> str:
        return f"FrequencyDist({self._freq_dict_concise})"

    def __str__(self) -> str:
        return f"<FrequencyDist: {len(self._freq_dict)} entries>"

    def __getitem__(self, key):
        return self._freq_dict[key]

    def most_common(self, n = 10):
        return sorted(self._freq_dict.items(), key = lambda x: x[1], reverse = True)[:n]
