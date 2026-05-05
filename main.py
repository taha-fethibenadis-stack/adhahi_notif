import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- SETTINGS ---
WILAYA_NAME = "تلمسان"
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = 60 

def send_alert(message):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

# --- BROWSER CONFIG ---
chrome_options = Options()
chrome_options.add_argument("--headless=new") # Modern headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")

def run_monitor():
    # webdriver-manager helps resolve the path for the binary
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print(f"Monitoring Tlemcen on adhahi.dz...")
    try:
        while True:
            try:
                driver.get("https://adhahi.dz/register")
                time.sleep(5)
                
                content = driver.page_source
                if WILAYA_NAME in content and "غير متوفر حاليًا" not in content:
                    send_alert(f"🚨 TLEMCEN IS OPEN! Go to https://adhahi.dz/register NOW!")
                    break 
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] Still unavailable...")
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(CHECK_INTERVAL)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_monitor()
