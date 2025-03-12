import os
import csv
import re
import unicodedata

def clean_title(title):
    """ Membersihkan judul dari encoding error dan memastikan 1 baris """
    title = unicodedata.normalize("NFKC", title)  # Normalisasi Unicode
    title = title.encode("utf-8", "ignore").decode("utf-8")  # Konversi ke UTF-8
    title = re.sub(r'\s+', ' ', title)  # Hilangkan spasi berlebih
    title = title.replace('"', '').strip()  # Hapus tanda kutip
    return title

def preprocess_titles(input_file, output_file):
    """ Membaca file CSV, membersihkan judul, dan menyimpannya ke file baru """
    cleaned_titles = []
    
    # Membaca file CSV
    with open(input_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        next(reader)  # Lewati header
        
        for row in reader:
            if row:
                cleaned_title = clean_title(row[0])
                cleaned_titles.append(cleaned_title)
    
    # Menyimpan hasil ke file baru
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["Judul Koleksi Bersih"])  # Header baru
        for title in cleaned_titles:
            writer.writerow([title])
    
    print(f"Hasil preprocessing telah disimpan di {output_file}")

if __name__ == "__main__":
    input_filename = "hasil-scraping/judul.csv"
    output_filename = "hasil-preprocessing/cleaned.csv"
    preprocess_titles(input_filename, output_filename)
