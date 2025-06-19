import os
import json
import pandas as pd
from bertopic import BERTopic
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import nltk
from datetime import datetime
import mlflow
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora.dictionary import Dictionary

print("=== Mulai proses training BERTopic dengan MLflow ===")

def setup_stopwords():
    try:
        print("1. Mengecek dan mengunduh stopwords NLTK...")
        try:
            from nltk.corpus import stopwords
            stopwords.words('english')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        from nltk.corpus import stopwords
        stopwords_en = set(stopwords.words('english'))
        stopwords_id = set(StopWordRemoverFactory().get_stop_words())
        all_stopwords = stopwords_en.union(stopwords_id)
        print(f"   Jumlah stopword EN: {len(stopwords_en)}, ID: {len(stopwords_id)}")
        return all_stopwords
    except Exception as e:
        print(f"Error pada proses stopword: {e}")
        return set(['dan', 'atau', 'dengan', 'untuk', 'yang', 'di', 'ke', 'dari', 'pada', 'adalah'])

def preprocess_text(text, stopwords_set):
    if pd.isna(text) or text == "":
        return ""
    import re
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in stopwords_set and len(t) > 2]
    return " ".join(tokens)

def validate_data(df):
    if df.empty:
        raise ValueError("DataFrame kosong")
    if 'title' not in df.columns:
        raise ValueError("Kolom 'title' tidak ditemukan")
    null_count = df['title'].isnull().sum()
    if null_count > 0:
        print(f"Ditemukan {null_count} nilai null di kolom title")
    valid_docs = df['title'].dropna().astype(str)
    if len(valid_docs) < 10:
        raise ValueError(f"Dokumen terlalu sedikit untuk training: {len(valid_docs)}")
    return True

def compute_coherence_score(model, documents, topics, top_n_words=10):
    """
    Menghitung coherence score untuk topik yang dihasilkan.
    """
    # Ambil top-n kata dari setiap topik
    topic_words = [ [word for word, _ in model.get_topic(topic_id)[:top_n_words]] for topic_id in range(len(topics)) ]
    # Buat dictionary dan corpus
    texts = [doc.split() for doc in documents]
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    # Hitung coherence
    coherence_model = CoherenceModel(
        topics=topic_words,
        texts=texts,
        dictionary=dictionary,
        coherence='c_v'
    )
    coherence_score = coherence_model.get_coherence()
    return coherence_score

def main():
    os.makedirs("pipeline", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    all_stopwords = setup_stopwords()

    json_path = '/app/data/scrape_data.json'
    if not os.path.exists(json_path):
        json_path = './data/scrape_data.json'

    print(f"2. Membaca file JSON dari: {json_path}")
    if not os.path.exists(json_path):
        print(f"File {json_path} tidak ditemukan.")
        return False

    try:
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
        print(f"Berhasil membaca file JSON. Jumlah data: {len(data)}")
    except Exception as e:
        print(f"ERROR saat membaca file JSON: {e}")
        return False

    try:
        df = pd.DataFrame(data)
        print(f"DataFrame dibuat. Kolom tersedia: {df.columns.tolist()}")
        validate_data(df)
    except Exception as e:
        print(f"ERROR saat membuat/validasi DataFrame: {e}")
        return False

    try:
        print("4. Melakukan preprocessing pada kolom 'title'...")
        df['title_processed'] = df['title'].apply(lambda x: preprocess_text(x, all_stopwords))
        df = df[df['title_processed'].str.len() > 0]
        documents = df['title_processed'].tolist()
        print(f"Preprocessing selesai. Dokumen valid: {len(documents)}")
        print(f"Contoh dokumen: {documents[:2]}")
        if len(documents) < 10:
            raise ValueError(f"Dokumen terlalu sedikit setelah preprocessing: {len(documents)}")
    except Exception as e:
        print(f"ERROR saat preprocessing: {e}")
        return False

    try:
        print("5. Training BERTopic...")

        mlflow.set_tracking_uri("file:/app/mlruns")  # local tracking
        mlflow.set_experiment("bertopic-training")

        with mlflow.start_run() as run:
            topic_model = BERTopic(
                language="multilingual",
                calculate_probabilities=True,
                verbose=True,
                min_topic_size=max(2, len(documents) // 50)
            )
            topics, probs = topic_model.fit_transform(documents)
            num_topics = len(set(topics)) - (1 if -1 in topics else 0)
            print(f"Training selesai. Jumlah topik: {num_topics}")

            topic_info = topic_model.get_topic_info()
            print(f"Topic distribution:\n{topic_info.head()}")

            # Hitung coherence score
            coherence_score = compute_coherence_score(topic_model, documents, topics)
            print(f"Coherence score: {coherence_score:.4f}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_path = f"pipeline/bertopic_model_{timestamp}"
            topic_model.save(model_path)
            print(f"Model disimpan di {model_path}")

            metadata = {
                "timestamp": timestamp,
                "num_documents": len(documents),
                "num_topics": num_topics,
                "model_path": model_path,
                "data_source": json_path,
                "coherence_score": coherence_score
            }

            with open(f"pipeline/training_metadata_{timestamp}.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            with open("pipeline/train_log.txt", "a", encoding="utf-8") as logf:
                logf.write(f"{timestamp}: Trained BERTopic on {len(documents)} documents, "
                          f"{num_topics} topics. Model: {model_path}, Coherence: {coherence_score:.4f}\n")

            # 💡 Log ke MLflow
            mlflow.log_param("timestamp", timestamp)
            mlflow.log_param("num_documents", len(documents))
            mlflow.log_param("num_topics", num_topics)
            mlflow.log_param("model_path", model_path)
            mlflow.log_param("coherence_score", coherence_score)
            mlflow.log_artifact(f"pipeline/training_metadata_{timestamp}.json")
            mlflow.log_artifact("pipeline/train_log.txt")
            mlflow.log_artifacts(model_path, artifact_path="model")

    except Exception as e:
        print(f"ERROR saat training/logging MLflow: {e}")
        return False

    print("=== Proses training BERTopic selesai tanpa error ===")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
