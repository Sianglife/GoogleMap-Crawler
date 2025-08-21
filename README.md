# GoogleMap-Crawler

## Instructions
### Environment Variables
Open `.env` file and set the following variables:
- `MONGO_URI`: MongoDB connection string
- `DB_NAME`: Database name
- `COMMENT_LIMIT`: Maximum number of comments to scrape
- `WAIT_TIMEOUT_DEFAULT`: Default wait timeout for Selenium
There's also a sample `.env` file included in the repository for reference.

### Keyword
Open `ref/keyword.json` file and set the area/keywords for scraping.
By default, the keywords are set to "旗津" with spots regarding religious places in Kaohsiung, Taiwan.
``` json
{
    "area": [
        "旗津"
    ],
    "keywords": [
        "宗教",
        "信仰",
        "寺廟",
        "神壇",
        "教堂",
        "聖地",
        "道觀"
    ]
}
```

### Run
Execute `main.py` to start crawling.
```bash
python main.py
```

## Database instructions
Make sure to set up your MongoDB database before running the crawler. The crawler will use MongoDB to store the scraped data.

