class BaseStemmer():
    def _ends_with(self, s: str, ends: str):
        return s[-len(ends):] == ends

    def _replace_suffix(self, s: str, ends_with: str, rep_with: str):
        if self._ends_with(s, ends_with):
            s = s[:-len(ends_with)] + rep_with
        return s

    def _replace_char(self, s, rep, pos):
        return s[:pos] + rep + s[pos + 1:]

    def _apply_rule(self, s, rule_list):
        for rule in rule_list:
            condition = rule[0]
            suffix_check = rule[1]
            suffix_replace = rule[2]
            if condition is None:
                if self._ends_with(s, suffix_check):
                    return self._replace_suffix(s, suffix_check, suffix_replace)
            else:
                if all(condition) == True:
                    return self._replace_suffix(s, suffix_check, suffix_replace)
        return s

    def stem(self, s):
        pass

    def stem_sentence(self, sentence: str, use_tokenizer: bool = False):
        words = sentence.split(" ")
        for i in range(len(words)):
            words[i] = self.stem(words[i])
        return " ".join(words)