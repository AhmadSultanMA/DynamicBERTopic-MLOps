from fastapi import FastAPI
import os
import requests
import csv
import time
from bs4 import BeautifulSoup

app = FastAPI()

BASE_URL = "https://lib.ui.ac.id/daftikol2?id=102"
SCRAPED_FILE = "data/scrape/judul.csv"

def scrape_ui_library(base_url, total_titles=100, step=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    titles = []
    
    for start in range(0, total_titles, step):
        url = f"{base_url}&start={start}&lokasi=lokal"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": f"Gagal mengambil halaman {url}: {str(e)}"}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.find_all('div', class_='judul-koleksi'):
            title_tag = item.find('a')
            if title_tag:
                titles.append(title_tag.text.strip())
                if len(titles) >= total_titles:
                    break
        time.sleep(1)

    save_to_csv(titles, SCRAPED_FILE)
    return {"message": f"Hasil scraping disimpan di {SCRAPED_FILE}"}

def save_to_csv(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Judul Koleksi"])
        for row in data:
            writer.writerow([row])

@app.get("/scrape")
def scrape():
    return scrape_ui_library(BASE_URL)
