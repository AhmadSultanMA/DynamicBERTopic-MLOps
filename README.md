# DynamicBERTopic-MLOps

## 📒 Index
- [About](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-about)
- [File Structure](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-file-structure)
- [How to Use](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-how-to-use)
- [Feature](https://github.com/AhmadSultanMA/DynamicBERTopic-MLops?tab=readme-ov-file#-feature)

## 📌 About

**DynamicBERTopic-MLOps** is a project that integrates **BERTopic** with **MLOps** to perform dynamic topic modeling. This project aims to implement **BERTopic** in a pipeline that can be deployed, monitored, and automatically updated.

## 📂 File Structure

```
├───data
│   ├───cleaned # Preprocessing results after data cleaning
│   └───scrape # Scraping results in CSV format
├───pipeline
└───script
    ├───📜 scraping.py      # Script for data scraping
    ├───📜 preprocessing.py # Script for data cleaning and processing
    ├───📜 EDA.py           # Script for Exploratory Data Analysis (EDA)

```

## 🔧 How to Use
1. **Clone Repository**

    ```bash
    git clone https://github.com/AhmadSultanMA/DynamicBERTopic-MLOps.git
    cd DynamicBERTopic-MLOps
    ```

2. **Install Required Depedencies**

    ```bash
    pip install requests beautifulsoup4 pandas matplotlib wordcloud scikit-learn transformers torch
    ```
    
3. **Run scraping.py**
   
    ```bash
    python script/scraping.py
    ```

4. **Run preprocessing.py**
   
    ```bash
    python script/preprocessing.py
    ```

5. **Run EDA.py**
   
    ```bash
    python script/EDA.py
    ```

## 📌 Feature

✅ Scraping UI library collections

✅ Cleaning data from unnecessary characters

✅ Storing data in CSV format

✅ Exploratory Data Analysis (EDA) to identify patterns and data distribution
