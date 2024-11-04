import unittest
from text_analyzer.analyzer import TextAnalyzer

class TestTextAnalyzer(unittest.TestCase):
    """Tests for the functionality of the TextAnalyzer class."""

    def setUp(self):
        """Setup a new TextAnalyzer object before each test method is run."""
        self.analyzer = TextAnalyzer("Hello world. This is a test.")

    def test_word_count(self):
        """Test that word count returns the correct total number of words."""
        self.assertEqual(self.analyzer.word_count(), 6)

    def test_char_count_with_spaces(self):
        """Test that character count with spaces matches expected total."""
        self.assertEqual(self.analyzer.char_count(), 28)

    def test_sentence_count(self):
        """Test that sentence count returns the correct number of sentences."""
        self.assertEqual(self.analyzer.sentence_count(), 2)

    def test_empty_input(self):
        """Test analyzer behavior with an empty string."""
        empty_analyzer = TextAnalyzer("")
        self.assertEqual(empty_analyzer.word_count(), 0)
        self.assertEqual(empty_analyzer.char_count(), 0)
        self.assertEqual(empty_analyzer.char_count(include_spaces=False), 0)
        self.assertEqual(empty_analyzer.sentence_count(), 0)

    def test_input_with_only_spaces(self):
        """Test analyzer behavior with a string consisting only of spaces."""
        space_analyzer = TextAnalyzer("    ")
        self.assertEqual(space_analyzer.word_count(), 0)
        self.assertEqual(space_analyzer.char_count(), 4)
        self.assertEqual(space_analyzer.char_count(include_spaces=False), 0)
        self.assertEqual(space_analyzer.sentence_count(), 0)

# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main()
