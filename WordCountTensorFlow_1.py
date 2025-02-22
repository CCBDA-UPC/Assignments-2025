import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Download the tokenizer only if not available
nltk.download('punkt_tab', quiet=True)


def get_tokens(file_path):
    """
    Reads the content of a file, tokenizes the text, and returns the tokens.

    Args:
        file_path (str): The path to the text file.

    Returns:
        list: A list of tokens extracted from the file.
    """
    try:
        logger.info("Attempting to read the file: %s", file_path)
        with open(file_path, 'r', encoding='utf-8') as file:  # Explicit encoding for better compatibility
            text = file.read()
            logger.info("File read successfully. Preprocessing text...")
            text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
            tokens = word_tokenize(text)
            logger.info("Text tokenized successfully. Number of tokens: %d", len(tokens))
            return tokens
    except FileNotFoundError:
        logger.error("File not found: %s", file_path)
        return []
    except Exception as e:
        logger.error("An unexpected error occurred while processing the file: %s", e)
        return []


def get_most_common_words(tokens, n=10):
    """
    Counts the frequency of tokens and returns the most common ones.

    Args:
        tokens (list): List of tokens.
        n (int): Number of most common words to return.

    Returns:
        list: A list of tuples containing the n most common tokens and their counts.
    """
    try:
        logger.info("Counting token frequencies...")
        count = Counter(tokens)
        most_common = count.most_common(n)
        logger.info("Successfully retrieved the %d most common words.", n)
        return most_common
    except Exception as e:
        logger.error("An unexpected error occurred while counting tokens: %s", e)
        return []


def main():
    """
    Main function to tokenize a file and display the most common words.
    """
    logger.info("Starting the program...")

    # Tokenize the file
    tokens = get_tokens('FirstContactWithTensorFlow.txt')

    if tokens:
        # Get the 10 most common words
        most_common_words = get_most_common_words(tokens)
        print("The 10 most common words are:")
        for word, freq in most_common_words:
            print(f"'{word}' appears {freq} times.")
    else:
        logger.warning("No tokens found. Please check the file or input.")

    logger.info("Program completed.")


if __name__ == "__main__":
    main()
