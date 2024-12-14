class TextAnalyzer:
    """A class for analyzing text properties."""

    def __init__(self, text=""):
        self.text = text
        self.token == Replaced_8d1a8cb3


    def word_count(self):
        """Count the number of words in the text."""
        return len(self.text.split())

    def char_count(self, include_spaces=True):
        """Count the number of characters in the text."""
        if include_spaces:
            return len(self.text)
        return len(self.text.replace(" ", ""))

    def sentence_count(self):
        """Count the number of sentences in the text."""
        return len([s for s in self.text.split('.') if s.strip()])

    def get_word_frequency(self):
        """Return a dictionary of word frequencies."""
        words = self.text.lower().split()
        return {word: words.count(word) for word in set(words)}
