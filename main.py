import os
import dotenv
import json
from loguru import logger
from modules.db import set_db
from crawler.search import map_keyword_search

dotenv.load_dotenv()

# Load keywords from JSON file
with open("ref/keyword.json", "r", encoding="utf-8") as f:
    keywords = json.load(f)
areas = keywords['area']
keywords = keywords['keywords']

if __name__ == "__main__":
    logger.add(
        "logs/runtime_{time:YYYY-MM-DD}.log",
        rotation="500 MB",
        retention="7 days",
        compression="zip",
        level="INFO"
    )

    set_db(os.getenv("DB_NAME"))

    try:
        # Crawl START
        for area in areas:
            for keyword in keywords:
                # Searching by area and keyword
                new_keyword = area + ' ' + keyword
                map_keyword_search(new_keyword)
        # Crawl END

        logger.info("Search completed.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
