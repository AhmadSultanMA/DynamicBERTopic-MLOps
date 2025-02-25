import os
import requests
import csv
from bs4 import BeautifulSoup

def scrape_ui_library(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Menyesuaikan parsing dengan struktur HTML situs
        titles = []
        for item in soup.find_all('div', class_='judul-koleksi'):
            title = item.find('a').text.strip()
            titles.append(title)
        
        return titles
    else:
        print(f"Gagal mengakses halaman. Kode status: {response.status_code}")
        return None

def save_to_csv(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow([row])
    
    print(f"Hasil scraping telah disimpan di {filename}")

if __name__ == "__main__":
    url = "https://lib.ui.ac.id/daftikol2?id=102"
    results = scrape_ui_library(url)
    
    if results:
        save_to_csv(results, "hasil-scraping/judul.csv")
