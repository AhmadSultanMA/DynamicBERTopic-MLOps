# DynamicBERTopic-MLOps

## 📒 Index
- [About](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-about)
- [File Structure](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-file-structure)
- [How to Use](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-how-to-use)
- [Feature](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-feature)

## 📌 About

**DynamicBERTopic-MLOps** is a project that integrates **BERTopic** with **MLOps** to perform dynamic topic modeling. This project aims to implement **BERTopic** in a pipeline that can be deployed, monitored, and automatically updated.

## 📂 File Structure

📦 **Repository**

```
├───📜 scraping.py # Main script for data scraping
├───📜 preprocessing.py # Script for cleaning and processing data
├───📁 hasil-scraping # Scraping results in CSV format
└───📁 hasil-preprocessing # Preprocessing results after data cleaning

```

## 🔧 How to Use
1. **Clone Repository**

    ```bash
    git clone https://github.com/AhmadSultanMA/DynamicBERTopic-MLOps.git
    cd DynamicBERTopic-MLOps
    ```

2. **Install Required Depedencies**

    ```bash
    pip install requests beautifulsoup4
    ```
    
3. **Run scraping.py**
   
    ```bash
    python scraping.py
    ```

4. **Run preprocessing.py**
   
    ```bash
    python preprocessing.py
    ```

## 📌 Feature

✅ Scraping UI library collections

✅ Cleaning data from unnecessary characters

✅ Storing data in CSV format
