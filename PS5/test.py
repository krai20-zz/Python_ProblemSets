import string

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

class WordTrigger(Trigger):
    def __init__ (self, word):
        self.word = word

    def is_word_in(self,text):
        list_text = []
        for character in string.punctuation:
            text = text.replace(character,' ')

        for element in text.split():
            if self.word == element.lower():
                return True
        return False

class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story)

check = TitleTrigger('koala')

print check.evaluate('Koala bears are soft and cuddly')