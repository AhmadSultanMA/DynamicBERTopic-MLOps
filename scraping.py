import os
import requests
import csv
import re
from bs4 import BeautifulSoup

def clean_text(text):
    """
    Membersihkan teks agar setiap judul berada dalam satu baris dengan format yang rapi.
    - Menghapus tanda kutip ganda ("), newline (\n), dan karakter tidak perlu lainnya.
    - Menghilangkan spasi berlebih dan whitespace yang tidak diinginkan.
    """
    text = text.strip()  # Hapus spasi di awal dan akhir
    text = re.sub(r'\s+', ' ', text)  # Ganti semua spasi berlebih dengan satu spasi
    text = text.replace('"', '')  # Hapus tanda kutip
    text = text.replace("\n", " ")  # Pastikan judul tetap dalam satu baris
    return text

def scrape_ui_library(base_url, total_titles=100, step=10):
    """
    Scraping judul dari halaman web dan memastikan hasilnya bersih sebelum disimpan.
    """
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
                title = item.find('a').get_text(separator=" ").strip()  # Ambil teks dengan separator spasi
                cleaned_title = clean_text(title)  # Bersihkan teks
                titles.append(cleaned_title)
                
                if len(titles) >= total_titles:
                    return titles
        else:
            print(f"Gagal mengakses halaman {url}. Kode status: {response.status_code}")
            break

    return titles

def save_to_csv(data, filename):
    """
    Menyimpan data hasil scraping ke CSV dengan format rapi.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Judul Koleksi"])  # Header
        for row in data:
            writer.writerow([row])
    
    print(f"Hasil scraping telah disimpan di {filename}")

if __name__ == "_main_":
    base_url = "https://lib.ui.ac.id/daftikol2?id=102"
    results = scrape_ui_library(base_url, total_titles=100)

    if results:
        save_to_csv(results, "hasil-scraping/judul_cleaned.csv")