from utils import logger
logger.configure_logger(True)
import logging
from client import Client
from settings import PROFILES, POST_LINK

def main():
    for profile in PROFILES:
        try:
            client = Client(profile)
            client.share_to_groups(
                POST_LINK
            )
            del client
        except Exception as e:
            logging.error(f"[{profile}] Client crashed. {e}")
    logging.info("Done. Exiting...")

if __name__ == "__main__":
    logging.info("Started!")
    main()
