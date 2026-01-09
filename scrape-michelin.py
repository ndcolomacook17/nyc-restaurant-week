import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://guide.michelin.com/us/en/new-york-state/new-york/restaurants/all-starred"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_page(page_num):
    if page_num == 1:
        url = f"{BASE_URL}?sort=distance"
    else:
        url = f"{BASE_URL}/page/{page_num}?sort=distance"

    print(f"Scraping page {page_num}: {url}")

    resp = requests.get(url, headers=HEADERS)
    
    # If we hit a 404, we've reached the end of the list
    if resp.status_code == 404:
        print("No more pages found.")
        return None
    
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    restaurants = []

    # Using the selector from your original script
    links = soup.select("a.link[aria-label^='Open ']")
    for link in links:
        label = link.get("aria-label", "")
        name = label.replace("Open ", "").strip()
        if name:
            restaurants.append(name)

    print(f"Found {len(restaurants)} restaurants")
    return restaurants

def main():
    all_restaurants = set()
    page = 1

    while True:
        try:
            page_restaurants = scrape_page(page)
            
            # Stop if the page doesn't exist (None) or is empty
            if page_restaurants is None or len(page_restaurants) == 0:
                break
                
            all_restaurants.update(page_restaurants)
            page += 1
            time.sleep(1.5)  # Slightly longer polite delay
            
        except requests.exceptions.HTTPError as e:
            print(f"Stopped scraping: {e}")
            break

    print("\n--- MICHELIN RESTAURANTS ---")
    for r in sorted(all_restaurants):
        print(r)

    print(f"\nTotal unique restaurants: {len(all_restaurants)}")

if __name__ == "__main__":
    main()