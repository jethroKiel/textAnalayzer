import sys
from typing import Optional
from colorama import init, Fore, Style
from applications.parser import TextParser
from applications.word_counter import WordCounter

# Initialize colorama for cross-platform color support
init()

# Unicode symbols for better visualization
SYMBOLS = {
    'bullet': '•',
    'arrow': '→',
    'check': '✓',
    'cross': '✗',
    'diamond': '♦',
    'star': '★',
    'section': '§',
    'bracket_left': '❲',
    'bracket_right': '❳',
    'horizontal_line': '─',
    'vertical_line': '│',
    'corner_top_left': '╭',
    'corner_top_right': '╮',
    'corner_bottom_left': '╰',
    'corner_bottom_right': '╯'
}

def print_header(text: str, width: int = 60):
    """Print a beautifully formatted header."""
    padding = (width - len(text) - 2) // 2
    print(f"\n{Fore.CYAN}{SYMBOLS['corner_top_left']}{SYMBOLS['horizontal_line'] * padding} {text} {SYMBOLS['horizontal_line'] * padding}{SYMBOLS['corner_top_right']}{Style.RESET_ALL}")

def print_footer(width: int = 60):
    """Print a beautifully formatted footer."""
    print(f"{Fore.CYAN}{SYMBOLS['corner_bottom_left']}{SYMBOLS['horizontal_line'] * width}{SYMBOLS['corner_bottom_right']}{Style.RESET_ALL}")

def print_stat(label: str, value: str):
    """Print a statistic with consistent formatting."""
    print(f"{Fore.BLUE}{SYMBOLS['diamond']} {label}:{Style.RESET_ALL} {value}")

def analyze_file(filename: str) -> Optional[str]:
    """
    Analyze a text file using both TextParser and WordCounter.
    Returns the file content if successful, None otherwise.
    """
    try:
        counter = WordCounter(filename)
        counter.read_file()
        counter.count_words()
        return counter.text

    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"{Fore.RED}{SYMBOLS['cross']} Error: {str(e)}{Style.RESET_ALL}")
        return None

def display_combined_analysis(parser: TextParser, counter: WordCounter):
    """Display the combined analysis results with enhanced formatting."""
    # Syntax Analysis Section
    print_header("Syntax Analysis")
    if not parser.errors:
        print(f"{Fore.GREEN}{SYMBOLS['check']} No syntax errors found.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Syntax errors found:{Style.RESET_ALL}")
        for line_num, error_msg in parser.errors:
            print(f"{SYMBOLS['arrow']} Line {line_num}: {error_msg}")
    print_footer()

    # Text Statistics Section
    print_header("Text Statistics")
    stats = parser.statistics
    print_stat("Lines", str(stats['line_count']))
    print_stat("Characters", str(stats['char_count']))
    print_stat("Words", str(stats['word_count']))
    print_stat("Average word length", f"{stats['avg_word_length']:.2f}")
    print_stat("Unique words", str(stats['unique_words']))
    print_footer()

    # Word Frequency Analysis Section
    print_header("Word Frequency Analysis")
    top_words = counter.get_top_words(10)
    if top_words:
        max_count = max(count for _, count in top_words)
        for word, count in top_words:
            bar_length = int((count / max_count) * 20)
            bar = SYMBOLS['horizontal_line'] * bar_length
            print(f"{Fore.YELLOW}{SYMBOLS['star']}{Style.RESET_ALL} {word:<15} {count:>5} {Fore.BLUE}{bar}{Style.RESET_ALL}")
    else:
        print(f"{SYMBOLS['bullet']} No words found in text.")
    print_footer()

    # Balance Check Section
    print_header("Balance Check")
    if parser.balanced:
        print(f"{Fore.GREEN}{SYMBOLS['check']} All brackets and parentheses are properly balanced.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{SYMBOLS['cross']} Warning: Unbalanced brackets or parentheses detected.{Style.RESET_ALL}")
    print_footer()

def main():
    if len(sys.argv) != 2:
        print(f"{Fore.RED}{SYMBOLS['cross']} Usage: python main.py <filename>{Style.RESET_ALL}")
        sys.exit(1)

    filename = sys.argv[1]
    print(f"\n{Fore.CYAN}{SYMBOLS['section']} Analyzing file: {filename}{Style.RESET_ALL}")

    text_content = analyze_file(filename)

    if text_content is not None:
        parser = TextParser()
        counter = WordCounter(filename)

        parser.analyze(text_content)
        counter.read_file()
        counter.count_words()

        display_combined_analysis(parser, counter)

if __name__ == "__main__":
    main()
