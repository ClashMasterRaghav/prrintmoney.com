import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def convert_ipo_link(original_link):
    """
    Converts the IPO link to the desired format.
    """
    if original_link:
        # Remove the base URL to manipulate only the path
        base_url = "https://www.investorgain.com"
        path = original_link.replace(base_url, "")
        
        # Replace 'gmp' with 'ipo' and remove the '-gmp' part
        parts = path.split('/')
        if len(parts) > 3 and parts[1] == "gmp":
            parts[1] = "ipo"
            parts[2] = parts[2].replace("-gmp", "")
        
        # Reconstruct the path and prepend the base URL
        edited_link = base_url + "/".join(parts)
        return edited_link
    return None

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
        base_url = "https://www.investorgain.com"  # Base URL to prepend

        for row in rows[1:]:  # Skip header row
            cols = row.find_all('td')
            if cols:
                # Find the IPO link in the first column (assumed to be in an <a> tag)
                ipo_link = cols[0].find('a')['href'] if cols[0].find('a') else None
                
                # Prepend the base URL to the link
                if ipo_link and not ipo_link.startswith('http'):
                    ipo_link = base_url + ipo_link

                # Convert the IPO link to the desired format
                edited_ipo_link = convert_ipo_link(ipo_link)

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
                    "IPO Link": ipo_link,  # Original link
                    "Edited IPO Link": edited_ipo_link,  # Edited link
                })

        # Save data to CSV if data is available
        if data:
            df = pd.DataFrame(data)
            df.to_csv(ipo_data.csv, index=False)
            print(f"Data saved to {ipo_data.csv}")
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
