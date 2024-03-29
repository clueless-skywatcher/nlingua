from nlingua.taggers.base import BaseTagger

class SimpleTagger(BaseTagger):
    """
    Takes in a tag, and assigns the same tag to every
    word it receives.

    >>> from nlingua.taggers import SimpleTagger
    >>> s = SimpleTagger("NN")
    >>> s.tag("This is a string".split(" "))
    [('This', 'NN'), ('is', 'NN'), ('a', 'NN'), ('string', 'NN')]
    >>> s.tag_sentences(["Hi bro wassup?".split(" "), "I am all good".split(" ")])
    [[('Hi', 'NN'), ('bro', 'NN'), ('wassup?', 'NN')], [('I', 'NN'), ('am', 'NN'), ('all', 'NN'), ('good', 'NN')]]

    Params:
    tag: The tag that needs to be assigned

    """
    def __init__(self, tag) -> None:
        self._tag = tag
        super(SimpleTagger, self).__init__()

    def tag_single(self, x):
        return self._tag

