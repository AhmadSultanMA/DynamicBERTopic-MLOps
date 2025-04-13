import os
import csv
import re
import unicodedata
import pandas as pd

def clean_title(title):
    """ Membersihkan judul dari karakter tidak perlu tanpa menghapus koma. """
    title = unicodedata.normalize("NFKC", title)  # Normalisasi Unicode
    title = title.encode("utf-8", "ignore").decode("utf-8")  # Konversi ke UTF-8
    title = re.sub(r'\s+', ' ', title)  # Hilangkan spasi berlebih
    title = title.replace('"', '').replace("'", "").strip()  # Hapus tanda kutip
    return title

def clean_csv(input_file, output_file):
    """ Membersihkan file CSV dan menyimpannya dengan kutipan otomatis agar kompatibel dengan Pandas. """
    if not os.path.exists(input_file):
        print(f"File {input_file} tidak ditemukan.")
        return

    cleaned_data = []

    # Baca file CSV
    with open(input_file, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        header = next(reader)  # Ambil header
        
        for row in reader:
            if row:  # Pastikan baris tidak kosong
                cleaned_row = [clean_title(cell) for cell in row]  # Bersihkan setiap kolom dalam baris
                cleaned_data.append(cleaned_row)

    # Simpan data yang sudah dibersihkan
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # Kutip semua nilai agar aman
        writer.writerow(header)
        writer.writerows(cleaned_data)

    print(f"Data bersih telah disimpan di {output_file}")

def load_cleaned_csv(file_path):
    """ Memuat file CSV yang sudah dibersihkan ke dalam Pandas DataFrame """
    df = pd.read_csv(file_path)
    return df

# Eksekusi script
if __name__ == "__main__":
    input_file = "data/scrape/judul.csv"
    output_file = "data/cleaned/cleaned.csv"
    
    clean_csv(input_file, output_file)

    # Load CSV ke Pandas untuk pengecekan
    df = load_cleaned_csv(output_file)
    print(df.head())  # Tampilkan 5 baris pertama
