import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def fetch_ipo_data_requests():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct paths relative to the script's location
    CSV_PATH = os.path.join(script_dir, "ipo_data.csv")

    url = "https://www.investorgain.com/report/live-ipo-gmp/331/ipo/"

    try:
        # Send HTTP request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with IPO data
        table = soup.find('table', class_='table')
        if not table:
            print("Table not found on the page.")
            return None

        # Extract rows from the table
        rows = table.find_all('tr')
        print(f"Rows found: {len(rows)}")  # Debug: check how many rows were found

        # Extract data from each row
        data = []
        for row in rows[1:]:  # Skip header row
            cols = row.find_all('td')
            if cols:
                data.append({
                    "IPO Name": cols[0].text.strip(),
                    "Status": cols[1].text.strip(),
                    "Price": cols[2].text.strip(),
                    "GMP(₹)": cols[3].text.strip(),
                    "Est Listing": cols[4].text.strip(),
                    " ": cols[5].text.strip(),  # rating (fire)
                    "IPO Size": cols[6].text.strip(),
                    "Lot Size": cols[7].text.strip(),
                    "Open Date": cols[8].text.strip(),
                    "Close Date": cols[9].text.strip(),
                    "BoA Dt": cols[10].text.strip(),
                    "Listing": cols[11].text.strip(),
                    "GMP Updated": cols[12].text.strip(),
                })

        # Save data to CSV if data is available
        if data:
            df = pd.DataFrame(data)
            df.to_csv(CSV_PATH, index=False)
            print(f"Data saved to {CSV_PATH}")
            return df
        else:
            print("No data extracted.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

# Run the scraper
if __name__ == "__main__":
    ipo_data = fetch_ipo_data_requests()
    if ipo_data is not None:
        print(ipo_data.head())
