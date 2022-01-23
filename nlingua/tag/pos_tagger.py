class PartOfSpeechTagger:
    def __init__(self, corpus) -> None:
        self._dataset = None
        self.corpus = corpus

    def _extract_features(self, sentence, idx):
        return {
            "word": "a"
        }
