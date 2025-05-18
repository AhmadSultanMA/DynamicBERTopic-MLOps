from bertopic import BERTopic
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora import Dictionary
import os
import mlflow
from datetime import datetime

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df['Judul Koleksi'].astype(str).tolist()

def train_model(texts):
    topic_model = BERTopic(verbose=True)
    topics, _ = topic_model.fit_transform(texts)
    return topic_model, topics

def evaluate_model(topic_model, texts):
    vectorizer_model = CountVectorizer().fit(texts)
    words = [text.split() for text in texts]
    dictionary = Dictionary(words)
    bow_corpus = [dictionary.doc2bow(word) for word in words]
    topic_words = topic_model.get_topics()
    topics = [[word for word, _ in topic_words[i]] for i in range(len(topic_words)) if i in topic_words]

    coherence_model = CoherenceModel(
        topics=topics,
        texts=words,
        dictionary=dictionary,
        coherence='c_v'
    )
    coherence_score = coherence_model.get_coherence()
    return coherence_score

def save_visualizations(topic_model, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    fig_topics = topic_model.visualize_topics()
    fig_topics.write_html(os.path.join(output_dir, "topics.html"))

    fig_hierarchy = topic_model.visualize_hierarchy()
    fig_hierarchy.write_html(os.path.join(output_dir, "hierarchy.html"))

    fig_barchart = topic_model.visualize_barchart()
    fig_barchart.write_html(os.path.join(output_dir, "barchart.html"))

    print(f"📊 Visualizations saved to {output_dir}")

if __name__ == "__main__":
    csv_path = "D:/kulyeah/git/DynamicBERTopic-MLOps/data/cleaned/cleaned.csv"
    model_output_dir = "D:/kulyeah/git/DynamicBERTopic-MLOps/pipeline/saved_model"
    viz_output_dir = "D:/kulyeah/git/DynamicBERTopic-MLOps/pipeline/visualizations"

    # MLflow setup
    mlflow.set_tracking_uri("file:///D:/kulyeah/git/DynamicBERTopic-MLOps/model/mlruns")
    mlflow.set_experiment("BERTopic Experiment")

    with mlflow.start_run():
        print("📥 Loading data...")
        texts = load_data(csv_path)

        print("🧠 Training BERTopic model...")
        topic_model, topics = train_model(texts)

        print("📈 Evaluating coherence score...")
        coherence = evaluate_model(topic_model, texts)
        print(f"Coherence Score: {coherence:.4f}")
        mlflow.log_metric("coherence_score", coherence)

        print("💾 Saving the model to MLflow...")
        # Gunakan timestamp biar unik
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_save_folder = os.path.join(model_output_dir, f"bertopic_model_{timestamp}")
        os.makedirs(model_save_folder, exist_ok=True)

        model_save_path = os.path.join(model_save_folder, "model.pkl")
        topic_model.save(model_save_path)

        mlflow.log_artifacts(model_save_folder, artifact_path="model")

        print("📊 Generating visualizations...")
        save_visualizations(topic_model, viz_output_dir)
        mlflow.log_artifacts(viz_output_dir, artifact_path="visualizations")

        mlflow.log_param("num_documents", len(texts))

        print("✅ All done with MLflow tracking!")