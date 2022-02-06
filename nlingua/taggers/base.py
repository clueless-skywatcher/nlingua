from abc import abstractmethod


from nlingua.exceptions.tagger import TaggerException

class BaseTagger:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def tag_single(self):
        pass

    def tag(self, l):
        if not isinstance(l, list):
            raise TaggerException("Need a list for tagging")
        tags = []
        for word in l:
            tags.append((word, self.tag_single(word)))

        return tags