import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import BertTokenizer, BertModel
import torch

# ======== 1. ANALISIS STATISTIK DASAR ========
def basic_text_analysis(df, text_column):
    """ Menampilkan analisis dasar dari dataset teks """
    print("📊 ANALISIS STATISTIK DASAR 📊")
    print(df[text_column].describe())
    print("\n🔹 Panjang Rata-rata Judul:", df[text_column].apply(len).mean())
    print("🔹 Jumlah Kata Rata-rata:", df[text_column].apply(lambda x: len(x.split())).mean())

# ======== 2. VISUALISASI DISTRIBUSI KATA ========
def plot_word_distribution(df, text_column):
    """ Membuat visualisasi distribusi kata menggunakan WordCloud """
    text = " ".join(df[text_column].dropna())  # Gabungkan semua teks
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("WordCloud - Distribusi Kata dalam Judul")
    plt.show()

# ======== 3. REPRESENTASI TEKS DENGAN TF-IDF ========
def tfidf_representation(df, text_column, max_features=100):
    """ Menggunakan TF-IDF untuk representasi teks """
    vectorizer = TfidfVectorizer(max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(df[text_column].dropna())

    print("🔹 TF-IDF Shape:", tfidf_matrix.shape)
    print("🔹 Contoh Kata TF-IDF:", vectorizer.get_feature_names_out()[:10])  # Tampilkan 10 kata pertama

    return tfidf_matrix, vectorizer

# ======== 3. REPRESENTASI TEKS DENGAN BERT EMBEDDINGS ========
def bert_representation(df, text_column, model_name="bert-base-uncased"):
    """ Menggunakan BERT untuk representasi teks """
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)

    def get_embedding(text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=50)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()  # Ambil rata-rata embedding

    embeddings = df[text_column].dropna().apply(get_embedding)
    
    print("🔹 BERT Embedding Shape:", embeddings.iloc[0].shape)  # Cek shape dari embedding pertama
    return embeddings

# ======== 4. PIPELINE UTAMA ========
def main_pipeline(csv_file, text_column="Judul Koleksi"):
    """ Pipeline utama untuk melakukan EDA pada teks """
    if not os.path.exists(csv_file):
        print(f"File {csv_file} tidak ditemukan.")
        return

    df = pd.read_csv(csv_file)

    # Langkah 1: Analisis Statistik
    basic_text_analysis(df, text_column)

    # Langkah 2: Visualisasi Distribusi Kata
    plot_word_distribution(df, text_column)

    # Langkah 3: Representasi Teks dengan TF-IDF
    tfidf_matrix, vectorizer = tfidf_representation(df, text_column)

    # Langkah 3: Representasi Teks dengan BERT
    bert_embeddings = bert_representation(df, text_column)

    # Simpan pipeline preprocessing sebagai script terpisah
    save_pipeline(vectorizer, "pipeline/tfidf_vectorizer.pkl")

# ======== 4. MENYIMPAN PIPELINE PREPROCESSING ========
import pickle

def save_pipeline(model, filepath):
    """ Menyimpan model preprocessing ke dalam file """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as file:
        pickle.dump(model, file)
    print(f"✅ Pipeline preprocessing disimpan di {filepath}")

# ======== EKSEKUSI PIPELINE ========
if __name__ == "__main__":
    csv_file = "data/cleaned/cleaned.csv"
    main_pipeline(csv_file)