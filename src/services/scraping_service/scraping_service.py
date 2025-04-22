from fastapi import FastAPI
import os
import requests
import time
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

BASE_URL = os.getenv("BASE_URL")
SCRAPED_FILE = "data/scrape_data.json"

@app.get("/scrape")
def scrape_ui_library(target_total: int = 1000, step: int = 10):
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    current_no = 1
    start = 0

    while len(results) < target_total:
        url = f"{BASE_URL}&start={start}&lokasi=lokal"
        try:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Gagal mengambil halaman {url}: {str(e)}")
            start += step
            time.sleep(1)
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='daftikol2')

        if not items:
            break  # Tidak ada lagi data, keluar dari loop

        for item in items:
            try:
                author_div = item.find_all('div')[0]
                authors = [a.strip() for a in author_div.text.split(",") if a.strip()]

                title_tag = item.find('div', class_='judul-koleksi').find('a')
                title = title_tag.text.strip()
                detail_url = f"https://lib.ui.ac.id/{title_tag['href']}"

                pub_year_div = item.find_all('div')[3].text.strip()
                publisher, year = "", ""
                if ":" in pub_year_div:
                    try:
                        publisher, year = pub_year_div.rsplit(",", 1)
                        publisher = publisher.strip()
                        year = int(year.strip())
                    except:
                        publisher = pub_year_div
                        year = None

                detail_response = requests.get(detail_url, headers=headers, timeout=20)
                detail_response.raise_for_status()
                detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                abstrak_div = detail_soup.find("div", id="abstrak")

                if abstrak_div:
                    abstract_text = abstrak_div.get_text(separator=" ", strip=True)
                else:
                    continue

                result = {
                    "no": current_no,
                    "title": title,
                    "abstract": abstract_text,
                    "authors": authors,
                    "journal_conference_name": "library_ui",
                    "publisher": publisher,
                    "year": year,
                    "doi": detail_url,
                    "group_name": "Diversity"
                }

                results.append(result)
                current_no += 1

                # Auto-save setiap 50 data
                if len(results) % 50 == 0:
                    save_to_json(results, SCRAPED_FILE)
                    print(f"Auto-saved {len(results)} data to {SCRAPED_FILE}")

                if len(results) >= target_total:
                    break

            except Exception as e:
                print(f"Error parsing item: {e}")
                continue

        start += step
        time.sleep(0.5)

    # Final save
    save_to_json(results, SCRAPED_FILE)
    return {"message": f"{len(results)} data berhasil disimpan di {SCRAPED_FILE}"}




def save_to_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
