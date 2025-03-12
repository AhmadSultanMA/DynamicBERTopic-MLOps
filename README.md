# DynamicBERTopic-MLOps

## 📒 Index
- [About](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-about)
- [File Structure](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-file-structure)
- [How to Use](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-how-to-use)
- [Feature](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-feature)

## 📌 About

**DynamicBERTopic-MLOps** adalah proyek yang mengintegrasikan **BERTopic** dengan **MLOps** untuk melakukan **topic modeling** secara dinamis. Proyek ini bertujuan untuk menerapkan **BERTopic** dalam pipeline yang dapat di-deploy, di-monitor, dan diperbarui secara otomatis.

## 📂 File Structure

📦 **Repository**

```
├───preprocessing.py
├───scraping.py  
├───hasil-preprocessing
└───hasil-scraping

```

## 🔧 How to Use
1. **Clone Repository**

    ```bash
    git clone https://github.com/AhmadSultanMA/DynamicBERTopic-MLOps.git
    cd DynamicBERTopic-MLOps
    ```

2. **Instal Dependensi yang Diperlukan**

    ```bash
    pip install requests beautifulsoup4
    ```
    
3. **Jalankan scraping.py**
   
    ```bash
    python scraping.py
    ```

4. **Jalankan preprocessing.py**
   
    ```bash
    python preprocessing.py
    ```

## 📌 Feature

✅ Scraping koleksi perpustakaan UI

✅ Pembersihan data dari karakter tidak perlu

✅ Penyimpanan data dalam format CSV
