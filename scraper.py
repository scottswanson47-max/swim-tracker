import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Setup the robot's "eyes" (Headless Chrome)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

def scrape():
    url = "https://amymasonsafety.com/class-%26-lessons-schedule"
    driver.get(url)
    time.sleep(5) # Wait for page to load

    master_slots = ["4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM"]
    
    # This finds the available buttons on the page
    elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'PM')]")
    available_times = [el.text for el in elements]

    # If it's not available, it's booked
    booked = [slot for slot in master_slots if slot not in available_times]
    
    with open('swim_data.json', 'w') as f:
        json.dump({"booked": booked, "last_updated": time.ctime()}, f)

    driver.quit()

if __name__ == "__main__":
    scrape()
