from nlingua.taggers.base import BaseTagger

class SimpleTagger(BaseTagger):
    """
    Takes in a tag, and assigns the same tag to every
    word it receives.

    >>> from nlingua.taggers import SimpleTagger
    >>> s = SimpleTagger("ADV")
    >>> s.tag("This is a string".split(" "))
    [('This', 'NN'), ('is', 'NN'), ('a', 'NN'), ('string', 'NN')]

    Params:
    tag: The tag that needs to be assigned

    """
    def __init__(self, tag) -> None:
        self._tag = tag
        super(SimpleTagger, self).__init__()

    def tag_single(self, x):
        return self._tag

