import sys
import string
from collections import Counter
from typing import Dict, List, Tuple

class WordCounter:
    def __init__(self, filename: str):
        self.filename = filename
        self.text = ""
        self.word_counts: Counter = Counter()

    def read_file(self) -> None:
        """Read the contents of the file."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                self.text = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{self.filename}' not found.")
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"Error: Unable to read '{self.filename}'. Make sure it's a text file.")

    def count_words(self) -> None:
        """Count words in the text."""
        if not self.text.strip():
            print("The file is empty.")
            return

        for line in self.text.split('\n'):
            words = self._tokenize(line)
            self.word_counts.update(words)

    def _tokenize(self, line: str) -> List[str]:
        """Tokenize a line into words."""
        words = []
        for word in line.split():
            normalized_word = self._normalize_word(word)
            if normalized_word:
                words.append(normalized_word)
        return words

    def _normalize_word(self, word: str) -> str:
        """Normalize a word by removing punctuation and converting to lowercase."""
        normalized = word.strip(string.punctuation + '`').lower()
        return normalized if normalized and not normalized.isspace() else ''

    def get_unique_words(self) -> int:
        """Get the count of unique words (words that appear only once)."""
        return sum(1 for count in self.word_counts.values() if count == 1)

    def get_top_words(self, n: int = 10) -> List[Tuple[str, int]]:
        """Get the top N words by frequency."""
        return self.word_counts.most_common(n)

    def display_results(self, num_top: int = 10) -> None:
        """Display word statistics results."""
        print(f"Total words: {sum(self.word_counts.values())}")
        print(f"Unique words: {len(self.word_counts)}")
        print(f"Words appearing only once: {self.get_unique_words()}")
        print("\nTop words:")
        for word, count in self.get_top_words(num_top):
            print(f"{word}: {count}")
