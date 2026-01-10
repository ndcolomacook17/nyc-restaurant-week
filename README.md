# NYC Restaurant Week + Michelin Finder

Find Michelin-starred restaurants participating in NYC Restaurant Week.

## Getting Started

### Prerequisites

- Python 3.13+
- Chrome browser (for Restaurant Week scraper)

### Installation

```bash
# Clone the repository
git clone https://github.com/ndcolomacook17/nyc-restaurant-week.git
cd nyc-restaurant-week

# Install with uv (recommended)
uv sync

# Or with pip
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

### Quick Start (Recommended)

Run the CLI to scrape both sources and find matches:

```bash
uv run python cli.py
```

This will:
1. Scrape all NYC Restaurant Week participants
2. Scrape Michelin-starred NYC restaurants
3. Display the intersection in your terminal

### Manual Usage

Run scrapers individually and save output to files:

```bash
# Scrape Restaurant Week (requires Chrome)
python scraper.py > all-restaurants.txt

# Scrape Michelin Guide
python scrape-michelin.py > michelin-restaurants.txt

# Find intersection
python find-intersection.py
```

Results are saved to `intersection.txt`.

## License

MIT
