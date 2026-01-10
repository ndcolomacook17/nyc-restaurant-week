#!/usr/bin/env python3
"""CLI tool to run scrapers in parallel and find Michelin restaurants in NYC Restaurant Week."""

import subprocess
import sys
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


def clean_name(name):
    """Normalize restaurant names for matching."""
    name = re.sub(r'\<[^>]+\>', '', name)
    name = name.lower()
    for word in ['steakhouse', 'restaurant', 'bar', 'grill', 'nyc']:
        name = name.replace(word, '')
    name = "".join(char for char in name if char.isalnum() or char.isspace())
    return " ".join(name.split())


def run_scraper(script_name, marker):
    """Run a scraper and return the list of restaurants."""
    print(f"Starting {script_name}...")
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=True,
        text=True
    )

    output = result.stdout
    restaurants = []

    # Parse output after the marker line
    lines = output.split('\n')
    capture = False
    for line in lines:
        if marker in line:
            capture = True
            continue
        if capture and line.strip():
            # Stop at summary line
            if line.startswith('Total unique'):
                break
            restaurants.append(line.strip())

    print(f"Finished {script_name}: found {len(restaurants)} restaurants")
    return restaurants


def find_intersection(list1, list2):
    """Find restaurants appearing in both lists."""
    dict1 = {clean_name(name): name for name in list1}
    dict2 = {clean_name(name): name for name in list2}

    matches = set()

    # Exact matches
    common_keys = set(dict1.keys()) & set(dict2.keys())
    matches.update(dict1[key] for key in common_keys)

    # Substring matches: check if a Michelin name is contained in a Restaurant Week name
    for michelin_clean, michelin_orig in dict2.items():
        for rw_clean, rw_orig in dict1.items():
            if michelin_clean != rw_clean and michelin_clean in rw_clean:
                matches.add(rw_orig)

    return sorted(matches)


def main():
    print("NYC Restaurant Week + Michelin Finder")
    print("=" * 40)

    response = input("\nRun both scrapers? [Y/n] ").strip().lower()
    if response and response != 'y':
        print("Cancelled.")
        return

    print("\nRunning scrapers in parallel...\n")

    scrapers = [
        ("scraper.py", "--- ALL RESTAURANTS ---"),
        ("scrape-michelin.py", "--- MICHELIN RESTAURANTS ---"),
    ]

    results = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(run_scraper, script, marker): script
            for script, marker in scrapers
        }
        for future in as_completed(futures):
            script = futures[future]
            results[script] = future.result()

    rw_restaurants = results["scraper.py"]
    michelin_restaurants = results["scrape-michelin.py"]

    matches = find_intersection(rw_restaurants, michelin_restaurants)

    print("\n" + "=" * 40)
    print("MICHELIN RESTAURANTS IN RESTAURANT WEEK")
    print("=" * 40 + "\n")

    for restaurant in matches:
        print(f"  {restaurant}")

    print(f"\nFound {len(matches)} Michelin restaurants participating in Restaurant Week!")


if __name__ == "__main__":
    main()
