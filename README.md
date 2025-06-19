# DynamicBERTopic-MLOps

## 📒 Indeks
- [Tentang Proyek](#tentang-proyek)
- [Struktur File](#struktur-file)
- [Cara Penggunaan](#cara-penggunaan)
- [Fitur](#fitur)
- [Implementasi Monitoring](#implementasi-monitoring)

---

## 📌 Tentang Proyek

**DynamicBERTopic-MLOps** adalah proyek yang mengintegrasikan **BERTopic** dengan **MLOps** untuk melakukan pemodelan topik secara dinamis. Proyek ini bertujuan untuk mengimplementasikan BERTopic dalam sebuah *pipeline* yang dapat di-*deploy*, dimonitor, dan diperbarui secara otomatis.

---

## 📂 Struktur File

```

├── data
│   ├── cleaned                              # Hasil preprocessing setelah pembersihan data
│   └── scrape\_data.json                     # Hasil scraping dalam format JSON
├── monitoring                               # File konfigurasi Prometheus (prometheus.yml)
├── pipeline                                 # Pipeline untuk otomasi end-to-end
├── src
│   └── services
│       ├── scraping\_service                 # Service untuk menangani proses scraping
│       ├── result\_service                   # Service untuk menampilkan hasil data
│       └── preprocess\_training\_service      # Service untuk preprocessing dan training model
├── docker-compose.yml                       # Compose file untuk menjalankan semua service
└── README.md

````

---

## 🔧 Cara Penggunaan

### 1. Clone Repositori

```bash
git clone https://github.com/AhmadSultanMA/DynamicBERTopic-MLOps.git
cd DynamicBERTopic-MLOps
````

### 2. Jalankan Aplikasi dengan Docker Compose

Pastikan Anda sudah menginstal **Docker** dan **Docker Compose**. Jalankan perintah berikut untuk membangun dan menjalankan semua layanan:

```bash
docker-compose up --build
```

Setelah selesai, semua layanan akan aktif dan siap digunakan.

---

## ✨ Fitur

* ✅ Scraping koleksi library UI
* ✅ Membersihkan data dari karakter yang tidak diperlukan
* ✅ Menyimpan data dalam format JSON
* ✅ Membangun API dengan **FastAPI** untuk scraping, preprocessing, training, dan pengambilan hasil
* ✅ Pengujian API secara lokal menggunakan **Postman** atau sejenisnya
* ✅ Mengemas API dalam kontainer menggunakan **Docker & Docker Compose**
* ✅ Pelatihan dan evaluasi model
* ✅ Integrasi **MLOps** untuk monitoring dengan Prometheus dan Grafana

---

## 📊 Implementasi Monitoring

### 🔧 Layanan yang Dimonitor

* `scraping_service` (port `8000`)
* `preprocess_training_service` (port `8001`)
* `result_service` (port `8002`)

### 🧰 Tools

* Prometheus
* Grafana
* Prometheus FastAPI Instrumentator

### 📈 Dashboard Grafana

**Metrik yang ditampilkan:**

* Total permintaan HTTP
* Waktu respons per endpoint
* Tingkat kesalahan (*error rate*)
* Waktu aktif kontainer (*container uptime*)

### 🔗 URL Akses

* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000)
* Metrics:

  * [http://localhost:8000/metrics](http://localhost:8000/metrics)
  * [http://localhost:8001/metrics](http://localhost:8001/metrics)
  * [http://localhost:8002/metrics](http://localhost:8002/metrics)


