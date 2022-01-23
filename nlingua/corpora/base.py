import platform

class Corpus():
    pass

class TaggingCorpus():
    def __init__(self, *args, **kwargs) -> None:
        self._platform = platform.system()
        self._data = None