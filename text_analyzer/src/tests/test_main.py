import unittest
from unittest.mock import patch, mock_open
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from main import analyze_file, display_combined_analysis
from applications.parser import TextParser
from applications.word_counter import WordCounter

class TestTextAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.sample_text = """Hello World!
This is a test file.
It has (some) {balanced} [brackets].
Test test TEST different words."""

        self.parser = TextParser()
        self.counter = WordCounter('dummy.txt')

    def test_analyze_file_success(self):
        with patch('builtins.open', mock_open(read_data=self.sample_text)):
            result = analyze_file('test.txt')
            self.assertEqual(result, self.sample_text)

    def test_analyze_file_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = analyze_file('nonexistent.txt')
            self.assertIsNone(result)

    def test_text_parser_balanced(self):
        self.parser.analyze(self.sample_text)
        self.assertTrue(self.parser.balanced)
        self.assertEqual(len(self.parser.get_errors()), 0)

    def test_text_parser_unbalanced(self):
        unbalanced_text = "This (is not} balanced."
        self.parser.analyze(unbalanced_text)
        self.assertFalse(self.parser.balanced)
        self.assertGreater(len(self.parser.get_errors()), 0)

    def test_word_counter_basic(self):
        text = "test Test TEST different different"
        with patch('builtins.open', mock_open(read_data=text)):
            self.counter.text = text
            self.counter.count_words()

            # Check case-insensitive counting
            self.assertEqual(self.counter.word_counts['test'], 3)
            self.assertEqual(self.counter.word_counts['different'], 2)

    def test_text_statistics(self):
        self.parser.analyze(self.sample_text)
        stats = self.parser.statistics

        self.assertEqual(stats['line_count'], 4)
        self.assertGreater(stats['word_count'], 0)
        self.assertGreater(stats['char_count'], 0)
        self.assertIsInstance(stats['avg_word_length'], float)

    def test_display_output(self):
        self.parser.analyze(self.sample_text)
        self.counter.text = self.sample_text
        self.counter.count_words()

        # Redirect stdout to capture output
        with patch('sys.stdout') as mock_stdout:
            display_combined_analysis(self.parser, self.counter)

            # Get all calls to print
            output = ''.join(call.args[0] for call in mock_stdout.write.call_args_list)

            # Check if main sections are present in output
            self.assertIn("Syntax Analysis", output)
            self.assertIn("Text Statistics", output)
            self.assertIn("Word Frequency Analysis", output)
            self.assertIn("Balance Check", output)

    def test_empty_file(self):
        empty_text = ""
        self.parser.analyze(empty_text)
        self.counter.text = empty_text
        self.counter.count_words()

        self.assertTrue(self.parser.balanced)
        self.assertEqual(len(self.parser.get_errors()), 0)
        self.assertEqual(sum(self.counter.word_counts.values()), 0)

    def test_special_characters(self):
        special_text = "Hello! @#$% World?"
        with patch('builtins.open', mock_open(read_data=special_text)):
            self.counter.text = special_text
            self.counter.count_words()

            self.assertEqual(self.counter.word_counts['hello'], 1)
            self.assertEqual(self.counter.word_counts['world'], 1)

    def test_main_function(self):
        # Test the main function with command line arguments
        test_args = ['main.py', 'test.txt']
        with patch('sys.argv', test_args):
            with patch('builtins.open', mock_open(read_data=self.sample_text)):
                with patch('sys.stdout'):  # Suppress output
                    # Import and run main() here to avoid sys.exit()
                    from main import main
                    try:
                        main()
                    except SystemExit as e:
                        self.assertEqual(e.code, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
