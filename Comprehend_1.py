import json
import boto3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def initialize_comprehend_client():
    """
    Initializes the AWS Comprehend client.

    Returns:
        boto3.client: The AWS Comprehend client instance.
    """
    try:
        logger.info("Initializing AWS Comprehend client...")
        return boto3.client('comprehend')
    except Exception as e:
        logger.error(f"An unexpected error occurred during AWS client initialization: {e}")
        raise


def detect_entities(comprehend_client, text, language='en'):
    """
    Calls AWS Comprehend's detect_entities API to extract entities from the text.

    Args:
        comprehend_client (boto3.client): The AWS Comprehend client instance.
        text (str): The input text to analyze.
        language (str): Language code for the input text. Default is 'en'.

    Returns:
        dict: A dictionary containing detected entities.
    """
    try:
        logger.info("Calling AWS Comprehend detect_entities API...")
        response = comprehend_client.detect_entities(Text=text, LanguageCode=language)
        logger.info("Successfully detected entities in the text.")
        return response
    except Exception as e:
        logger.error(f"An unexpected error occurred while detecting entities: {e}")
        raise


def print_entity_results(entity_list):
    """
    Prints the detected entities and their properties in a user-friendly format.

    Args:
        entity_list (dict): The output from AWS Comprehend detect_entities API.
    """
    if 'Entities' in entity_list and entity_list['Entities']:
        logger.info("Processing and printing entity results...")
        for entity in entity_list['Entities']:
            print(f"{entity['Text']}: {entity['Type']}, {entity['Score']:.2f}")
            logger.debug(f"Entity details: {entity}")
    else:
        logger.warning("No entities found in the text.")


def read_text_from_file(file_path):
    """
    Reads text content from a file.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: The text content of the file.
    """
    try:
        logger.info(f"Reading text from file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        logger.info("Successfully read text from file.")
        return text
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise


def main():
    """
    Main function to execute the AWS Comprehend entity detection process.
    """
    file_path = 'MachineLearning.txt'  # File containing text to analyze

    try:
        # Read text from input file
        text = read_text_from_file(file_path)

        # Initialize AWS Comprehend client
        comprehend_client = initialize_comprehend_client()

        # Detect entities
        logger.info("Starting entity detection...")
        entity_list = detect_entities(comprehend_client, text, language='en')

        # Optional: Print the full JSON response
        print(json.dumps(entity_list, indent=4))

        # Print entity results
        print_entity_results(entity_list)

    except Exception as e:
        logger.error(f"Error during execution: {e}")


if __name__ == "__main__":
    main()
