import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scrape():
    url = "https://amymasonsafety.com/class-%26-lessons-schedule"
    driver.get(url)
    
    master_slots = ["4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM"]
    available_times = []

    try:
        # 1. Wait for the iframe (the booking window) to exist
        wait = WebDriverWait(driver, 20)
        # GoDaddy/OLA usually uses an iframe. We wait for it and switch inside.
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for frame in iframes:
            driver.switch_to.frame(frame)
            # 2. Look for any text containing "PM" inside this frame
            elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'PM')]")
            if elements:
                available_times = [el.text for el in elements]
                break
            driver.switch_to.default_content() # Switch back out if not found

    except Exception as e:
        print(f"Error encountered: {e}")
    
    # 3. Logic check: If we found NOTHING, don't overwrite with 'All Booked' 
    # to avoid false alarms.
    if not available_times:
        booked = ["Error: Could not find calendar"]
    else:
        booked = [slot for slot in master_slots if slot not in available_times]
    
    with open('swim_data.json', 'w') as f:
        json.dump({"booked": booked, "last_updated": time.ctime()}, f)

    driver.quit()

if __name__ == "__main__":
    scrape()
