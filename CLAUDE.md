# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python web scraper that finds the intersection between NYC Restaurant Week participants and Michelin-starred restaurants in NYC. It consists of three standalone scripts that run independently.

## Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Scrape NYC Restaurant Week restaurants (requires Chrome)
python scraper.py

# Scrape Michelin-starred NYC restaurants
python scrape-michelin.py

# Find restaurants appearing in both lists
python find-intersection.py
```

## Architecture

Three independent scripts with no shared code:

- **scraper.py** - Uses Selenium with Chrome to scrape the NYC Tourism Restaurant Week page. Handles pagination through 49 pages, collecting restaurant names via CSS selectors. Outputs to stdout.

- **scrape-michelin.py** - Uses requests + BeautifulSoup to scrape the Michelin Guide. Iterates through paginated results until 404. Outputs to stdout.

- **find-intersection.py** - Reads `all-restaurants.txt` and `michelin-restaurants.txt`, normalizes names (lowercase, removes common words like "steakhouse"/"restaurant"), finds matches, and writes results to `intersection.txt`.

## Data Flow

1. Run `scraper.py` and redirect output to `all-restaurants.txt`
2. Run `scrape-michelin.py` and redirect output to `michelin-restaurants.txt`
3. Run `find-intersection.py` to generate `intersection.txt`

## Dependencies

Python 3.13 with packages: selenium, webdriver-manager, requests, beautifulsoup4, python-dotenv
