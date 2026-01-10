# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python web scraper that finds the intersection between NYC Restaurant Week participants and Michelin-starred restaurants in NYC. It consists of three standalone scripts that run independently.

## Commands

```bash
# Install dependencies
uv sync

# Run CLI to scrape both sources and find matches (recommended)
uv run python cli.py

# Or run scrapers individually:
uv run python scraper.py              # NYC Restaurant Week (requires Chrome)
uv run python scrape-michelin.py      # Michelin Guide
uv run python find-intersection.py    # Find matches from .txt files
```

## Architecture

Four scripts:

- **scraper.py** - Uses Selenium with Chrome to scrape the NYC Tourism Restaurant Week page. Handles pagination through 49 pages, collecting restaurant names via CSS selectors. Outputs to stdout.

- **scrape-michelin.py** - Uses requests + BeautifulSoup to scrape the Michelin Guide. Iterates through paginated results until 404. Outputs to stdout.

- **find-intersection.py** - Reads `all-restaurants.txt` and `michelin-restaurants.txt`, normalizes names (lowercase, removes common words like "steakhouse"/"restaurant"), finds matches, and writes results to `intersection.txt`.

- **cli.py** - Interactive CLI that runs both scrapers in parallel using ThreadPoolExecutor, captures their output, finds the intersection, and displays results in the terminal.

## Data Flow

**CLI (recommended):** Run `python cli.py` - handles everything automatically.

**Manual:** Redirect scraper output to text files, then run intersection finder:
1. `python scraper.py > all-restaurants.txt`
2. `python scrape-michelin.py > michelin-restaurants.txt`
3. `python find-intersection.py` → generates `intersection.txt`

## Dependencies

Python 3.11+ (see pyproject.toml for packages)
