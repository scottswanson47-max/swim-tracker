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
# Adding a "User Agent" makes the robot look more like a real person browsing
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scrape():
    url = "https://amymasonsafety.com/class-%26-lessons-schedule"
    driver.get(url)
    
    master_slots = ["4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM"]
    available_times = []

    try:
        # 1. Give the page a moment to settle
        time.sleep(8) 
        
        # 2. GoDaddy uses many nested iframes. This command finds ALL of them 
        # and checks each one for our time slots.
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for index, frame in enumerate(iframes):
            driver.switch_to.default_content()
            driver.switch_to.frame(frame)
            
            # Look for elements that look like time buttons
            elements = driver.find_elements(By.XPATH, "//button[contains(., 'PM')] | //span[contains(., 'PM')]")
            
            if elements:
                available_times = [el.text.strip() for el in elements if "PM" in el.text]
                # Clean up the text (e.g., "4:30 PM" might come in as "4:30\nPM")
                available_times = [t.replace('\n', ' ') for t in available_times]
                break 

    except Exception as e:
        print(f"Error: {e}")
    
    # 3. Decision Logic
    if not available_times:
        # If we still see nothing, let's list what we DID see to help debug
        booked = ["Scanning... No slots found"]
    else:
        # Find slots in our master list that are NOT in the available list
        booked = [slot for slot in master_slots if slot not in available_times]
    
    with open('swim_data.json', 'w') as f:
        json.dump({"booked": booked, "last_updated": time.ctime()}, f)

    driver.quit()

if __name__ == "__main__":
    scrape()
