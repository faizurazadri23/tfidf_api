# 🧠 TF-IDF API (Flask)

API ini digunakan untuk melakukan **pencarian teks berbasis TF-IDF (Term Frequency – Inverse Document Frequency)**.  
Didesain untuk diintegrasikan dengan frontend seperti **Laravel**, yang bertugas menampilkan UI upload dokumen dan hasil pencarian.

---

## 🚀 Fitur Utama

- 📂 Upload dokumen berformat `.pdf` atau `.txt`.
- 🧾 Ekstraksi teks otomatis dari file PDF atau file teks biasa.
- 🔢 Pembentukan model **TF-IDF Vectorizer** secara dinamis.
- 🔍 Endpoint untuk melakukan pencarian berdasarkan query.
- 🧮 Hasil dikembalikan dalam bentuk **ranking similarity (cosine similarity)** antar dokumen.

---

## 🧰 Teknologi yang Digunakan

| Komponen | Deskripsi |
|-----------|------------|
| **Python 3.8+** | Bahasa pemrograman utama |
| **Flask** | Web framework untuk REST API |
| **scikit-learn** | Library untuk vektorisasi TF-IDF dan perhitungan cosine similarity |
| **PyMuPDF (fitz)** | Ekstraksi teks dari file PDF |
| **JSON API** | Format komunikasi antar aplikasi |

---

## 📁 Struktur Folder

```
tfidf_api/
│
├── app.py               # File utama Flask API
├── requirements.txt     # Dependensi Python
├── uploads/             # Folder untuk menyimpan file yang diupload
└── README.md            # Dokumentasi API
```

---

## ⚙️ Instalasi

### 1️⃣ Clone Repository
```bash
git clone https://github.com/faizurazadri23/tfidf_api.git
cd tfidf-api
```

### 2️⃣ Buat Virtual Environment (opsional tapi direkomendasikan)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependensi
```bash
pip install -r requirements.txt
```

### 4️⃣ Jalankan API
```bash
python app.py
```

API akan berjalan di:
```
http://127.0.0.1:5000
```

---

## 🔗 Endpoint API

### 📤 **1. Upload Dokumen**
Upload dokumen `.pdf` atau `.txt` untuk diproses menjadi bagian dari model TF-IDF.

- **URL**: `/upload`  
- **Method**: `POST`  
- **Form Data**:
  - `file`: file dokumen (`.pdf` / `.txt`)
- **Response (JSON)**:
```json
{
  "message": "dokumen1.pdf berhasil diproses",
  "total_docs": 3
}
```

#### 🧩 Contoh Curl
```bash
curl -X POST -F "file=@/path/to/file.pdf" http://127.0.0.1:5000/upload
```

---

### 🔍 **2. Search Dokumen**
Melakukan pencarian berdasarkan query teks yang diberikan.  
API akan menghitung kesamaan (*cosine similarity*) antara query dan seluruh dokumen yang telah diupload.

- **URL**: `/search`  
- **Method**: `POST`  
- **Body (JSON)**:
```json
{
  "query": "Timnas Indonesia menang"
}
```

- **Response (JSON)**:
```json
[
  {
    "document": "Dokumen 1",
    "score": 0.712
  },
  {
    "document": "Dokumen 3",
    "score": 0.102
  }
]
```

#### 🧩 Contoh Curl
```bash
curl -X POST http://127.0.0.1:5000/search      -H "Content-Type: application/json"      -d '{"query": "Timnas Indonesia"}'
```

---

## 🧮 Cara Kerja

1. Saat file diupload ke endpoint `/upload`, sistem akan:
   - Menyimpan file di folder `/uploads`
   - Mengekstrak teks (menggunakan `fitz` jika PDF)
   - Menambahkan teks ke daftar dokumen
   - Melatih ulang model **TF-IDF Vectorizer**

2. Saat query dikirim ke endpoint `/search`, sistem akan:
   - Mengubah query menjadi vektor TF-IDF
   - Menghitung **cosine similarity** antara query dan seluruh dokumen
   - Mengembalikan daftar ranking dokumen paling relevan

---

## 📦 Contoh Integrasi Laravel

Laravel frontend dapat menggunakan controller seperti berikut:

```php
$response = Http::attach('file', file_get_contents($filePath), $fileName)
    ->post('http://127.0.0.1:5000/upload');

$response = Http::post('http://127.0.0.1:5000/search', [
    'query' => $request->input('query')
]);
```

---

## ⚠️ Catatan Penting

- Model TF-IDF akan **dilatih ulang setiap kali file baru diupload**.
- Untuk skala besar, disarankan menyimpan model (`vectorizer` dan `tfidf_matrix`) ke file `.pkl` menggunakan `joblib`.
- API ini belum menggunakan database — semua data disimpan sementara di memori.

---

## 🔒 Keamanan (Opsional)

Untuk lingkungan produksi, disarankan:
- Menambahkan autentikasi token API.
- Membatasi ukuran file upload.
- Menggunakan reverse proxy (Nginx) untuk routing Laravel → Flask.

---

## 🧠 Rencana Pengembangan

- [ ] Dukungan upload multi-file sekaligus  
- [ ] Penyimpanan model TF-IDF dengan `joblib`  
- [ ] API endpoint `/train` dan `/reset`  
- [ ] Ekstraksi teks dengan OCR untuk file gambar  

---

## 🧑‍💻 Pembuat

**TF-IDF Hybrid Search API**  
Dibuat oleh: *Faizura Zadri & ChatGPT (GPT-5)*  
Lisensi: MIT License  
Tahun: 2025
