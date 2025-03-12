import os
import csv
import re
import unicodedata

def clean_title(title):
    """ Membersihkan judul dari encoding error dan memastikan tidak ada tanda kutip. """
    title = unicodedata.normalize("NFKC", title)  # Normalisasi Unicode
    title = title.encode("utf-8", "ignore").decode("utf-8")  # Konversi ke UTF-8
    title = re.sub(r'\s+', ' ', title)  # Hilangkan spasi berlebih
    title = title.replace('"', '').replace("'", "").strip()  # Hapus semua tanda kutip
    return title

def clean_csv(input_file, output_file):
    """ Membersihkan file CSV dari judul yang masih memiliki tanda kutip atau karakter tidak perlu. """
    if not os.path.exists(input_file):
        print(f"File {input_file} tidak ditemukan.")
        return

    cleaned_data = []

    with open(input_file, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        header = next(reader)  # Ambil header
        
        for row in reader:
            if row:  # Pastikan baris tidak kosong
                cleaned_row = [clean_title(cell) for cell in row]  # Bersihkan setiap kolom dalam baris
                cleaned_data.append(cleaned_row)

    # Simpan data yang sudah dibersihkan
    with open(output_file, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar='\\')  # Hindari kutipan
        writer.writerow(header)  # Tulis kembali header
        writer.writerows(cleaned_data)

    print(f"Data bersih telah disimpan di {output_file}")

# Contoh penggunaan
input_file = "hasil-scraping/judul.csv"
output_file = "hasil-preprocessing/cleaned.csv"
clean_csv(input_file, output_file)
