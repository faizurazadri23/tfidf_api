from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

documents = []
vectorizer = TfidfVectorizer()
tfidf_matrix = None

def extract_text(file_path):
    """Ekstrak teks dari PDF atau file teks"""
    if file_path.endswith(".pdf"):
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

@app.route("/upload", methods=["POST"])
def upload_file():
    global documents, tfidf_matrix

    if "file" not in request.files:
        return jsonify({"error": "Tidak ada file terupload"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nama file kosong"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Ekstrak teks dan simpan
    text = extract_text(file_path)
    documents.append(text)

    # Latih ulang TF-IDF setiap upload
    tfidf_matrix = vectorizer.fit_transform(documents)

    return jsonify({"message": f"{file.filename} berhasil diproses", "total_docs": len(documents)})

@app.route("/search", methods=["POST"])
def search():
    global tfidf_matrix
    if tfidf_matrix is None or len(documents) == 0:
        return jsonify({"error": "Belum ada dokumen diupload"}), 400

    data = request.get_json()
    query = data.get("query", "")
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()

    results = [
        {"document": f"Dokumen {i+1}", "score": float(similarity[i])}
        for i in similarity.argsort()[::-1]
    ]
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
