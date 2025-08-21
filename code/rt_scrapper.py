import csv
import os
import re
import time
from datetime import datetime
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


movie_urls = {
    "sinners_2025": "https://www.rottentomatoes.com/m/sinners_2025/reviews",
    "the_life_of_chuck": "https://www.rottentomatoes.com/m/the_life_of_chuck/reviews",
    "superman_2025": "https://www.rottentomatoes.com/m/superman_2025/reviews",
    "jurassic_world_rebirth": "https://www.rottentomatoes.com/m/jurassic_world_rebirth/reviews",
    "weapons": "https://www.rottentomatoes.com/m/weapons/reviews",
    "avatar_the_way_of_water": "https://www.rottentomatoes.com/m/avatar_the_way_of_water/reviews"
}

def setup_driver():
    """Setup Chrome driver with better error handling"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        try:
            driver = webdriver.Chrome(options=chrome_options)
            print(" ChromeDriver found automatically")
            return driver
        except Exception as e1:
            print(f" Auto ChromeDriver failed: {e1}")
            
            try:
                service = Service(r"C:\Users\GIMBIYA BENJAMIN\Desktop\chromedriver\chromedriver.exe")
                driver = webdriver.Chrome(service=service, options=chrome_options)
                print(" ChromeDriver found at specified path")
                return driver
            except Exception as e2:
                print(f" Explicit path failed: {e2}")
                raise Exception(f"ChromeDriver setup failed. Auto: {e1}, Explicit: {e2}")
                
    except Exception as e:
        print(f" Driver setup completely failed: {e}")
        print("\n TROUBLESHOOTING:")
        print("1. Install ChromeDriver: https://chromedriver.chromium.org/")
        print("2. Or install via: pip install webdriver-manager")
        print("3. Make sure Chrome browser is installed")
        raise

def safe_text(el):
    """Safely extract text from element"""
    try:
        return el.text.strip() if el and el.text else ""
    except:
        return ""

def click_if_present(driver, by, selector, timeout=3):
    """Click element if present with better error handling"""
    try:
        btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", btn)
        print(f" Clicked: {selector}")
        return True
    except Exception as e:
        print(f" Could not click {selector}: {e}")
        return False

def accept_cookies_if_needed(driver):
    """Handle cookie consent with more options"""
    print(" Checking for cookie consent...")
    possible = [
        (By.ID, "onetrust-accept-btn-handler"),
        (By.ID, "truste-consent-button"),
        (By.CSS_SELECTOR, "button[aria-label='Agree']"),
        (By.CSS_SELECTOR, "button[mode='primary']"),
        (By.CSS_SELECTOR, "button[title='Accept All']"),
        (By.CSS_SELECTOR, "[data-qa='accept-all-button']"),
        (By.XPATH, "//button[contains(text(), 'Accept')]"),
        (By.XPATH, "//button[contains(text(), 'Agree')]"),
    ]
    
    for by, sel in possible:
        if click_if_present(driver, by, sel, timeout=2):
            time.sleep(1)
            return True
    
    print("ℹ No cookie consent found or needed")
    return False

def load_all_reviews(driver):
    """Load all reviews with better detection"""
    print(" Loading all reviews...")
    loaded_count = 0
    max_attempts = 20  
    
    while loaded_count < max_attempts:
        selectors = [
            "button[data-qa='load-more-btn']",
            "button[data-qa='review-load-more']",
            "rt-button[data-qa='load-more-btn']",
            ".js-show-more-btn",
            "button:has-text('Load More')",  
            "//button[contains(text(), 'Load More')]",
            "//button[contains(text(), 'Show More')]",
        ]
        
        clicked = False
        for sel in selectors:
            try:
                if sel.startswith("//"):
                    btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, sel))
                    )
                else:
                    btn = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                    )
                
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", btn)
                clicked = True
                loaded_count += 1
                print(f" Loaded more reviews (attempt {loaded_count})")
                time.sleep(3)  
                break
                
            except Exception:
                continue
        
        if not clicked:
            print(f"ℹ No more 'Load More' buttons found after {loaded_count} attempts")
            break
    
    return loaded_count

def parse_review_card(card):
    """Parse review card with comprehensive selectors"""
    def safe_extract(selectors):
        for sel in selectors:
            try:
                if sel.startswith("//"):
                    el = card.find_element(By.XPATH, sel)
                else:
                    el = card.find_element(By.CSS_SELECTOR, sel)
                text = el.text.strip() if el.text else ""
                if text: 
                    return text
            except:
                continue
        return ""

    data = {
        "critic": safe_extract([
            ".display-name", 
            ".critic-name a", 
            "[data-qa='review-critic-link']",
            ".author-name",
            "rt-text[slot='critic-name']",
            "//a[contains(@class, 'critic')]//text()",
        ]),
        "outlet": safe_extract([
            ".publication", 
            ".critic-publication", 
            "[data-qa='review-critic-publication']",
            ".publication-name",
            "rt-text[slot='publication']",
        ]),
        "date": safe_extract([
            ".review-date", 
            "time", 
            "[data-qa='review-date']",
            ".date",
            "rt-text[slot='review-date']",
        ]),
        "score": safe_extract([
            ".review-score", 
            ".score", 
            "[data-qa='review-score']",
            ".rating",
        ]),
        "quote": safe_extract([
            ".review-text", 
            ".the_review", 
            "[data-qa='review-text']",
            ".review-quote",
            "rt-text[slot='review-text']",
        ]),
    }

    html = card.get_attribute("outerHTML") or ""
    class_names = card.get_attribute("class") or ""
    
    if any(x in html.lower() for x in ["fresh", "certified-fresh"]) or "fresh" in class_names.lower():
        data["freshness"] = "fresh"
    elif "rotten" in html.lower() or "rotten" in class_names.lower():
        data["freshness"] = "rotten"
    else:
        data["freshness"] = ""

    return data

def write_csv(path, rows):
    """Write CSV with error handling"""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        fieldnames = ["movie_key", "movie_url", "critic", "outlet", "date", "score", "freshness", "quote"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
        print(f" Successfully wrote {path}")
        return True
    except Exception as e:
        print(f" Failed to write {path}: {e}")
        return False

def debug_page_content(driver, movie_key):
    """Debug what's actually on the page"""
    print(f"\n🔍 DEBUGGING PAGE CONTENT for {movie_key}")
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")
    
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        print(f"Body text length: {len(body.text)}")
        if len(body.text) < 100:
            print(f"Body text: {body.text}")
    except:
        print(" No body found")
    
    selectors_to_check = [
        "review-speech-balloon",
        "[data-qa='review-item']",
        ".review-card",
        ".review_table_row",
        ".critic-review",
        ".review-container",
    ]
    
    for sel in selectors_to_check:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, sel)
            print(f"Found {len(elements)} elements with selector: {sel}")
            if elements and len(elements) > 0:
                print(f"  First element text preview: {elements[0].text[:100]}...")
        except Exception as e:
            print(f"Error checking {sel}: {e}")

def main():
    """Main function with comprehensive error handling"""
    all_rows = []
    driver = None
    
    try:
        driver = setup_driver()
        wait = WebDriverWait(driver, 15)
        
        test_movies = movie_urls  
        
        for key, url in test_movies.items():
            print(f"\n Processing: {key}")
            print(f" URL: {url}")
            
            try:
                driver.get(url)
                print(" Page loaded")
                
                time.sleep(3)
                
                accept_cookies_if_needed(driver)
                
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
                    print(" Body element found")
                except TimeoutException:
                    print(" Page load timeout")
                    continue
                
                debug_page_content(driver, key)
                
                load_attempts = load_all_reviews(driver)
                
                review_selectors = [
                    "review-speech-balloon",
                    "[data-qa='review-item']",
                    ".review-card",
                    ".review_table_row",
                    ".critic-review",
                    ".review-container",
                ]
                
                cards = []
                for sel in review_selectors:
                    try:
                        found_cards = driver.find_elements(By.CSS_SELECTOR, sel)
                        if found_cards:
                            cards = found_cards
                            print(f" Found {len(cards)} review cards using selector: {sel}")
                            break
                    except Exception as e:
                        print(f" Selector {sel} failed: {e}")
                
                if not cards:
                    print(" No review cards found with any selector")

                    with open(f"debug_{key}.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    print(f" Saved page source to debug_{key}.html")
                    continue
            
                rows = []
                for i, card in enumerate(cards):
                    try:
                        data = parse_review_card(card)
                        if any(data.values()): 
                            data["movie_key"] = key
                            data["movie_url"] = url
                            rows.append(data)
                            print(f" Parsed review {i+1}: {data.get('critic', 'Unknown critic')}")
                    except Exception as e:
                        print(f" Failed to parse review card {i+1}: {e}")
                
                if rows:
                    out_name = f"{key}_reviews.csv"
                    if write_csv(out_name, rows):
                        print(f" Saved {len(rows)} reviews to {out_name}")
                    
                    all_rows.extend(rows)
                else:
                    print(" No valid review data extracted")
    
                print(f" Waiting 5 seconds before next movie...")
                time.sleep(5)
                
            except Exception as e:
                print(f" Error processing {key}: {e}")
                traceback.print_exc()
                continue
        
        if all_rows:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            combined = f"all_reviews_{timestamp}.csv"
            if write_csv(combined, all_rows):
                print(f"\n SUCCESS! Saved combined CSV with {len(all_rows)} reviews: {combined}")
                print(f" Target: 1100 reviews | Collected: {len(all_rows)} reviews")
                if len(all_rows) >= 1100:
                    print(" TARGET ACHIEVED! ")
                else:
                    print(f" Need {1100 - len(all_rows)} more reviews to reach target")
        else:
            print("\n No reviews collected from any movie")
            
    except Exception as e:
        print(f" CRITICAL ERROR: {e}")
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()
            print("🔚 Browser closed")

if __name__ == "__main__":
    main()