import os
import json
import pandas as pd
from bertopic import BERTopic
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import nltk
from datetime import datetime

print("=== Mulai proses training BERTopic ===")

def setup_stopwords():
    """Setup stopwords dengan error handling yang lebih baik"""
    try:
        print("1. Mengecek dan mengunduh stopwords NLTK...")
        
        # Check if stopwords already downloaded
        try:
            from nltk.corpus import stopwords
            stopwords.words('english')  # Test if available
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        from nltk.corpus import stopwords
        stopwords_en = set(stopwords.words('english'))
        
        # Indonesian stopwords
        stopwords_id = set(StopWordRemoverFactory().get_stop_words())
        all_stopwords = stopwords_en.union(stopwords_id)
        
        print(f"   Jumlah stopword EN: {len(stopwords_en)}, ID: {len(stopwords_id)}")
        return all_stopwords
        
    except Exception as e:
        print(f"Error pada proses stopword: {e}")
        return set(['dan', 'atau', 'dengan', 'untuk', 'yang', 'di', 'ke', 'dari', 'pada', 'adalah'])

def preprocess_text(text, stopwords_set):
    """Preprocessing text dengan cleaning yang lebih baik"""
    if pd.isna(text) or text == "":
        return ""
    
    # Convert to string dan lowercase
    text = str(text).lower()
    
    # Remove special characters (keep alphanumeric and spaces)
    import re
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Tokenize dan remove stopwords
    tokens = text.split()
    tokens = [t for t in tokens if t not in stopwords_set and len(t) > 2]
    
    return " ".join(tokens)

def validate_data(df):
    """Validasi data sebelum training"""
    if df.empty:
        raise ValueError("DataFrame kosong")
    
    if 'title' not in df.columns:
        raise ValueError("Kolom 'title' tidak ditemukan")
    
    # Check for null values
    null_count = df['title'].isnull().sum()
    if null_count > 0:
        print(f"Ditemukan {null_count} nilai null di kolom title")
    
    # Check document length after preprocessing
    valid_docs = df['title'].dropna().astype(str)
    if len(valid_docs) < 10:
        raise ValueError(f"Dokumen terlalu sedikit untuk training: {len(valid_docs)}")
    
    return True

def main():
    # Setup directories first
    os.makedirs("pipeline", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Setup stopwords
    all_stopwords = setup_stopwords()
    
    # Path ke file JSON - sesuaikan dengan docker volume
    json_path = '/app/data/scrape_data.json'  # Path di dalam container
    
    # Fallback untuk local development
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
        
        # Validasi data
        validate_data(df)
        
    except Exception as e:
        print(f"ERROR saat membuat/validasi DataFrame: {e}")
        return False

    try:
        print("4. Melakukan preprocessing pada kolom 'title'...")
        
        # Preprocessing dengan function yang sudah diperbaiki
        df['title_processed'] = df['title'].apply(lambda x: preprocess_text(x, all_stopwords))
        
        # Filter dokumen kosong setelah preprocessing
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
        
        # Konfigurasi BERTopic yang lebih optimal
        topic_model = BERTopic(
            language="multilingual",
            calculate_probabilities=True,
            verbose=True,
            min_topic_size=max(2, len(documents) // 50)  # Dynamic min_topic_size
        )
        
        topics, probs = topic_model.fit_transform(documents)
        
        num_topics = len(set(topics)) - (1 if -1 in topics else 0)  # Exclude outlier topic
        print(f"Training selesai. Jumlah topik: {num_topics}")
        
        # Log topic information
        topic_info = topic_model.get_topic_info()
        print(f"Topic distribution:\n{topic_info.head()}")
        
    except Exception as e:
        print(f"ERROR saat training BERTopic: {e}")
        return False

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = f"pipeline/bertopic_model_{timestamp}"
        
        # Save model
        topic_model.save(model_path)
        print(f"Model disimpan di {model_path}")

        # Save training metadata
        metadata = {
            "timestamp": timestamp,
            "num_documents": len(documents),
            "num_topics": num_topics,
            "model_path": model_path,
            "data_source": json_path
        }
        
        with open(f"pipeline/training_metadata_{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Update train log
        with open("pipeline/train_log.txt", "a", encoding="utf-8") as logf:
            logf.write(f"{timestamp}: Trained BERTopic on {len(documents)} documents, "
                      f"{num_topics} topics. Model: {model_path}\n")
        
        print("Training metadata dan log berhasil disimpan")
        
    except Exception as e:
        print(f"ERROR saat menyimpan model/log: {e}")
        return False
    try:
        from pathlib import Path

        vis_path = Path("pipeline/visualizations")
        vis_path.mkdir(parents=True, exist_ok=True)

        print("6. Membuat visualisasi topik...")

        # Visualisasi interaktif topik
        topic_model.visualize_topics().write_html(vis_path / "topics.html")
        print(f"✔ topics.html disimpan di {vis_path}")

        # Visualisasi distribusi topik
        topic_model.visualize_barchart(top_n_topics=10).write_html(vis_path / "bar_chart.html")
        print(f"✔ bar_chart.html disimpan di {vis_path}")

        # Visualisasi hierarki topik
        topic_model.visualize_hierarchy().write_html(vis_path / "hierarchy.html")
        print(f"✔ hierarchy.html disimpan di {vis_path}")

        # Visualisasi heatmap antar topik
        topic_model.visualize_heatmap().write_html(vis_path / "heatmap.html")
        print(f"✔ heatmap.html disimpan di {vis_path}")

    except Exception as e:
        print(f"ERROR saat membuat visualisasi: {e}")

    print("=== Proses training BERTopic selesai tanpa error ===")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)