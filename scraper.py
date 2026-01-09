from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "https://www.nyctourism.com/restaurant-week/"
TOTAL_PAGES = 49

RESTAURANT_SELECTOR = (
    "h3.CardHeading_headline__qu1q3"
)

NEXT_SELECTOR = "ul.PromotionCardGrid_pagination__cd1k4 li.next a"
ACTIVE_PAGE_SELECTOR = "li.PromotionCardGrid_active__ihUB4"

def main():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    wait = WebDriverWait(driver, 15)

    driver.get(URL)

    all_restaurants = set()

    for page in range(1, TOTAL_PAGES + 1):
        print(f"\nScraping page {page}...")

        # wait for restaurants
        wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, RESTAURANT_SELECTOR)
            )
        )

        restaurants = driver.find_elements(By.CSS_SELECTOR, RESTAURANT_SELECTOR)
        page_names = [r.text.strip() for r in restaurants if r.text.strip()]
        print(f"Found {len(page_names)} restaurants")

        all_restaurants.update(page_names)

        # stop if last page
        if page == TOTAL_PAGES:
            break

        # capture first restaurant BEFORE click
        first_restaurant_before = restaurants[0].text

        next_link = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, NEXT_SELECTOR)
            )
        )

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

        # JS click to avoid header interception
        driver.execute_script("arguments[0].click();", next_link)

        # wait until restaurant list updates
        wait.until(
            lambda d: d.find_element(
                By.CSS_SELECTOR, RESTAURANT_SELECTOR
            ).text != first_restaurant_before
        )


    driver.quit()

    print("\n--- ALL RESTAURANTS ---")
    for r in sorted(all_restaurants):
        print(r)

    print(f"\nTotal unique restaurants: {len(all_restaurants)}")

if __name__ == "__main__":
    main()
