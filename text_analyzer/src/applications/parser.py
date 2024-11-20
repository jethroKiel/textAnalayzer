from typing import List, Tuple, Dict
from collections import Counter
from data_structures.stack import Stack

class TextParser:
    def __init__(self):
        """ Pag initialize ng mga attributes """
        self.text = ""
        self.lines = []
        self.errors: List[Tuple[int, str]] = []
        self._balanced = False
        self._statistics: Dict[str, int] = {}

    def analyze(self, text: str):
        """ Dito ina anlayze yung text """
        self.text = text
        self.lines = text.split('\n')
        self.errors.clear()
        self._balanced = False
        self._statistics.clear()

        """ Perform analysis """
        self._check_balanced_symbols()
        self._compute_statistics()

    def _check_balanced_symbols(self):
        stack = Stack()
        opening = "({["
        closing = ")}]"
        pairs = {')': '(', '}': '{', ']': '['}

        for line_num, line in enumerate(self.lines, 1):
            for char_num, char in enumerate(line, 1):
                if char in opening:
                    stack.push((char, line_num, char_num))
                elif char in closing:
                    if stack.is_empty() or stack.peek()[0] != pairs[char]:
                        self.errors.append((line_num, f"Unmatched closing symbol '{char}' at position {char_num}"))
                    else:
                        stack.pop()

        while not stack.is_empty():
            char, line_num, char_num = stack.pop()
            self.errors.append((line_num, f"Unmatched opening symbol '{char}' at position {char_num}"))

        self._balanced = len(self.errors) == 0

    def _compute_statistics(self):
        """ Compute text statistics """
        word_count = sum(len(line.split()) for line in self.lines)
        char_count = sum(len(line) for line in self.lines)

        word_lengths = [len(word) for line in self.lines for word in line.split()]
        avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0

        self._statistics = {
            "line_count": len(self.lines),
            "word_count": word_count,
            "char_count": char_count,
            "avg_word_length": round(avg_word_length, 2),
            "unique_words": len(set(word.lower() for line in self.lines for word in line.split()))
        }

    @property
    def balanced(self) -> bool:
        """ Check at retrun kung balance ba """
        return self._balanced

    @property
    def statistics(self) -> Dict[str, int]:
        # Return the computed statistics
        return self._statistics

    def get_errors(self) -> List[Tuple[int, str]]:
        """List number ng mga errors"""
        return self.errors

    def display_errors(self):
        """ Display the syntax errors found in the text """
        if not self.errors:
            print("No syntax errors found.")
        else:
            print("Syntax errors found:")
            for line_num, error_msg in self.errors:
                print(f"Line {line_num}: {error_msg}")
