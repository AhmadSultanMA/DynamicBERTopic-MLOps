from fastapi import FastAPI
import os
import requests
import csv
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

BASE_URL = os.getenv("BASE_URL")
SCRAPED_FILE = os.getenv("SCRAPED_FILE")

@app.get("/scrape")
def scrape():
    return scrape_ui_library(BASE_URL)

def scrape_ui_library(base_url, total_titles=100, step=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []

    for start in range(0, total_titles, step):
        url = f"{base_url}&start={start}&lokasi=lokal"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": f"Gagal mengambil halaman {url}: {str(e)}"}

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='judul-koleksi')

        for item in items:
            title_tag = item.find('a')
            if not title_tag:
                continue

            title = title_tag.text.strip()
            detail_url = f"https://lib.ui.ac.id{title_tag['href']}"

            # Get detail content
            try:
                detail_resp = requests.get(detail_url, headers=headers, timeout=10)
                detail_resp.raise_for_status()
            except requests.exceptions.RequestException:
                continue

            detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')

            result = {
                "title": title,
                "abstract": get_detail_field(detail_soup, "Abstrak"),
                "authors": get_authors(detail_soup),
                "journal_conference_name": "library_ui",
                "publisher": get_detail_field(detail_soup, "Fakultas"),
                "year": get_detail_field(detail_soup, "Tahun"),
                "doi": detail_url,
                "group_name": "Diversity"
            }

            results.append(result)
            if len(results) >= total_titles:
                break

        time.sleep(1)

    save_to_csv(results, SCRAPED_FILE)
    return {"message": f"{len(results)} data berhasil disimpan di {SCRAPED_FILE}"}

def get_detail_field(soup, field_name):
    try:
        td = soup.find('td', string=field_name)
        return td.find_next_sibling('td').text.strip() if td else ""
    except:
        return ""

def get_authors(soup):
    try:
        td = soup.find('td', string="Nama")
        raw_authors = td.find_next_sibling('td').text.strip() if td else ""
        return [author.strip() for author in raw_authors.split(";") if author.strip()]
    except:
        return []

def save_to_csv(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["title", "abstract", "authors", "journal_conference_name", "publisher", "year", "doi", "group_name"])
        for row in data:
            writer.writerow([
                row["title"],
                row["abstract"],
                "; ".join(row["authors"]),
                row["journal_conference_name"],
                row["publisher"],
                row["year"],
                row["doi"],
                row["group_name"]
            ])
