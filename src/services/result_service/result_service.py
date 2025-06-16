import os
import json
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)

# Dapatkan direktori absolut tempat result_service.py berada
base_dir = os.path.dirname(os.path.abspath(__file__))

possible_paths = [
    os.path.join("/app", "scraping_data", "scrape_data.json"),
    os.path.join("/app", "data", "scrape_data.json"), 
    os.path.join(base_dir, "..", "scraping_service", "data", "scrape_data.json"), 
]

# Cari path yang valid
file_path = None
for path in possible_paths:
    if os.path.exists(path):
        file_path = path
        break

# Jika tidak ada yang ditemukan, gunakan path default
if file_path is None:
    file_path = possible_paths[0]  # gunakan path pertama sebagai default

@app.get("/get-results")
async def get_results():
    print(f"Mencari file di: {file_path}")  # Debugging
    print(f"Path absolut: {os.path.abspath(file_path)}")  # Debugging path absolut

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {
                "status": "success",
                "data": data,
                "total_records": len(data) if isinstance(data, list) else 1
            }
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    else:
        return {
            "error": f"File tidak ditemukan di {os.path.abspath(file_path)}. Pastikan scraping sudah dilakukan.",
            "status": "file_not_found"
        }

@app.get("/")
async def root():
    return {"message": "Result Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Tambahan endpoint untuk mendapatkan info file
@app.get("/file-info")
async def file_info():
    abs_path = os.path.abspath(file_path)
    return {
        "file_path": file_path,
        "absolute_path": abs_path,
        "file_exists": os.path.exists(file_path),
        "current_directory": os.getcwd(),
        "service_directory": base_dir
    }