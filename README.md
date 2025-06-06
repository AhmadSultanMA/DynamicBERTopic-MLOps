﻿# DynamicBERTopic-MLOps

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
│   ├───cleaned                 # Preprocessing results after data cleaning 
│   └───scrape                  # Scraping results in CSV format 
├───model                       # Model-related artifacts 
├───pipeline                    # Pipeline for end-to-end automation 
├───src
|   ├───services 
|   │   ├───scraping_service    # Service to handle scraping processes 
|   |   └───result_service      # Service to return preprocessed results 
|   ├───EDA.py                  # Script for Exploratory Data Analysis (EDA) 
|   ├───preprocessing.py        # Script for data cleaning and processing 
│   └───scraping.py             # Script for data scraping 
├───docker-compose.yml          # Compose file for running multiple services 
├───requirements.txt            # Python dependencies 
└───README.md

markdown
Salin
Edit

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
    
6. **Run Services Locally**
   
    ```bash
    uvicorn src.services.scraping_service.scraping_service:app --reload --port 8000
    uvicorn src.services.result_service.result_service:app --reload --port 8001
    ```

7. **Run Docker Compose**
   
    ```bash
    docker-compose up --build
    ```

6. **Run Docker Compose**
   
    ```bash
    docker-compose up --build
    ```  
## 📌 Feature

✅ Scraping UI library collections

✅ Cleaning data from unnecessary characters

✅ Storing data in CSV format

✅ Exploratory Data Analysis (EDA) to identify patterns and data distribution
 
✅ Build API using FastAPI for both scraping and result retrieval

✅ Test API locally using Postman

✅ Containerize the APIs using Docker & Docker Compose

✅ Model training and evaluation with coherence score

## 📊 Monitoring Implementation with Grafana & Prometheus

### 🔧 Services Monitored
- scraping_service (port 8000)
- result_service (port 8001)

### 🧰 Tools
- Prometheus
- Grafana
- Prometheus FastAPI Instrumentator

### 📈 Grafana Dashboards
Metrics shown:
- Total HTTP requests
- Response time per endpoint
- Error rate
- Container uptime

### 🔗 Access URLs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Metrics: http://localhost:8000/metrics, http://localhost:8001/metrics
