import os
import pandas as pd
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)

# Dapatkan direktori absolut tempat result_service.py berada
base_dir = os.path.dirname(os.path.abspath(__file__))

# Gabungkan dengan path ke judul.csv
file_path = os.path.join(base_dir, "..", "data", "scrape", "judul.csv")

@app.get("/get-results")
async def get_results():
    print(f"Mencari file di: {file_path}")  # Debugging

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df.to_dict()
    else:
        return {"error": f"File tidak ditemukan di {file_path}. Pastikan scraping sudah dilakukan."}
