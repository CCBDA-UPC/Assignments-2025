import os
import logging
from atproto import Client, client_utils
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def login_to_client():
    """
    Log in to the AT Proto client using environment variables.
    Returns:
        Client: Logged-in AT Proto client instance.
        Profile: Profile object for the logged-in user.
    """
    try:
        email = os.getenv("ATP_EMAIL")
        password = os.getenv("ATP_PASSWORD")
        if not email or not password:
            raise ValueError("Missing ATP_EMAIL or ATP_PASSWORD in environment variables.")

        client = Client()
        profile = client.login(email, password)
        logger.info("Login successful. Welcome, %s!", profile.display_name)
        return client, profile
    except Exception as e:
        logger.error("Failed to log in: %s", e)
        raise


def create_and_post_text(client):
    """
    Build and send a post using the AT Proto client.
    Args:
        client (Client): Logged-in AT Proto client instance.
    """
    try:
        text = client_utils.TextBuilder().text("Hello World from ").link("Python SDK", "https://atproto.blue")
        post = client.send_post(text)
        logger.info("Post sent successfully: %s", post.uri)
        return post
    except Exception as e:
        logger.error("Failed to send post: %s", e)
        raise


def like_post(client, post):
    """
    Like a post using the AT Proto client.
    Args:
        client (Client): Logged-in AT Proto client instance.
        post: Post object to like.
    """
    try:
        client.like(post.uri, post.cid)
        logger.info("Post liked successfully: %s", post.uri)
    except Exception as e:
        logger.error("Failed to like post: %s", e)
        raise


def main():
    """
    Main entry point for the script.
    Handles login, posting, and liking a post.
    """
    try:
        client, profile = login_to_client()
        post = create_and_post_text(client)
        like_post(client, post)
    except Exception as e:
        logger.error("An error occurred: %s", e)


if __name__ == "__main__":
    main()
