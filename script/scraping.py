import os
import requests
import csv
import time
from bs4 import BeautifulSoup

def scrape_ui_library(base_url, total_titles=100, step=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    titles = []
    for start in range(0, total_titles, step):
        url = f"{base_url}&start={start}&lokasi=lokal"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error mengambil halaman {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        
        for item in soup.find_all('div', class_='judul-koleksi'):
            title_tag = item.find('a')
            if title_tag:
                title = title_tag.text.strip()
                titles.append(title)
                
                if len(titles) >= total_titles:
                    return titles

        time.sleep(1)  # Delay untuk menghindari blocking

    return titles

def save_to_csv(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Judul Koleksi"]) 
        for row in data:
            writer.writerow([row])
    
    print(f"Hasil scraping telah disimpan di {filename}")

if __name__ == "__main__":
    base_url = "https://lib.ui.ac.id/daftikol2?id=102"
    results = scrape_ui_library(base_url, total_titles=1000)

    if results:
        save_to_csv(results, "data/scrape/judul.csv")
