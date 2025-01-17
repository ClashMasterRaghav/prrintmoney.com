from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

def fetch_ipo_data_selenium():

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct paths relative to the script's location
    DRIVER_PATH = os.path.join(script_dir, "chromedriver-linux64/chromedriver")
    CHROME_BINARY_PATH = os.path.join(script_dir, "chrome-headless-shell-linux64/chrome-headless-shell")

    url = "https://www.investorgain.com/report/live-ipo-gmp/331/ipo/"

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.binary_location = CHROME_BINARY_PATH
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox
    chrome_options.add_argument("--disable-dev-shm-usage")  # Optional: reduce memory issues
    chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering
    chrome_options.add_argument("--headless")  # Enable headless mode (no UI)
    chrome_options.add_argument("--disable-software-rasterizer")  # Optional: Disable software rendering

    # Set up Selenium WebDriver
    service = Service(DRIVER_PATH)
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)

        # Wait for the table to load (increase wait time)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )

        # Scroll the page to load any dynamically loaded content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for content to load after scrolling
        
        # Check if the table exists in the page source
        page_source = driver.page_source
        if "table" not in page_source:
            print("Table not found in page source. Something might be wrong.")
            return None

        # Extract IPO data
        data = []
        table = driver.find_element(By.CLASS_NAME, "table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        print(f"Rows found: {len(rows)}")  # Debug: check how many rows were found
        
        for row in rows[1:]:  # Skip header
            cols = row.find_elements(By.TAG_NAME, "td")
            if cols:
                data.append({
                    "IPO Name": cols[0].text.strip(),
                    "Status": cols[1].text.strip(),
                    "Price": cols[2].text.strip(),
                    "GMP(₹)": cols[3].text.strip(),
                    "Est Listing": cols[4].text.strip(),
                    " ": cols[5].text.strip(), # rating (fire)
                    "IPO Size": cols[6].text.strip(),
                    "Lot Size": cols[7].text.strip(),
                    "Open Date": cols[8].text.strip(),
                    "Close Date": cols[9].text.strip(),
                    "BoA Dt": cols[10].text.strip(),
                    "Listing": cols[11].text.strip(),
                    "GMP Updated": cols[12].text.strip(),
                })

        # Save data
        if data:
            df = pd.DataFrame(data)
            CSV_PATH = os.path.join(script_dir, "ipo_data.csv")
            # Save the DataFrame to the constructed path
            df.to_csv(CSV_PATH, index=False)
            print(f"Data saved to {CSV_PATH}")
            return df
        else:
            print("No data extracted.")
            return None
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

# Run the scraper
if __name__ == "__main__":
    ipo_data = fetch_ipo_data_selenium()
    if ipo_data is not None:
        print(ipo_data.head())
