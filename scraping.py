import os
import requests
import csv
from bs4 import BeautifulSoup

def scrape_ui_library(base_url, total_titles=100, step=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    titles = []
    for start in range(0, total_titles, step):
        url = f"{base_url}&start={start}&lokasi=lokal"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for item in soup.find_all('div', class_='judul-koleksi'):
                title = item.find('a').text.strip()
                titles.append(title)
                
                if len(titles) >= total_titles:
                    return titles
        else:
            print(f"Gagal mengakses halaman {url}. Kode status: {response.status_code}")
            break

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
    results = scrape_ui_library(base_url, total_titles=100)

    if results:
        save_to_csv(results, "hasil-scraping/judul.csv")
