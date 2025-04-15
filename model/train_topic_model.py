from bertopic import BERTopic
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora import Dictionary
import os
import joblib

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

def save_model(topic_model, output_dir="D:/kulyeah/git/DynamicBERTopic-MLOps/pipeline/saved_model"):
    os.makedirs(output_dir, exist_ok=True)
    topic_model.save(os.path.join(output_dir, "bertopic_model"))

def save_visualizations(topic_model, output_dir="D:/kulyeah/git/DynamicBERTopic-MLOps/pipeline/visualizations"):
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

    print("📥 Loading data...")
    texts = load_data(csv_path)

    print("🧠 Training BERTopic model...")
    topic_model, topics = train_model(texts)

    print("📈 Evaluating coherence score...")
    coherence = evaluate_model(topic_model, texts)
    print(f"Coherence Score: {coherence:.4f}")

    print("💾 Saving the model...")
    save_model(topic_model)

    print("📊 Generating visualizations...")
    save_visualizations(topic_model)

    print("✅ All done!")