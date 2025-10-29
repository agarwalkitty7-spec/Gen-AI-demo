from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# retriever.py

def retrieve_relevant_chunks(question, chunks):
    question_lower = question.lower()
    relevant = []
    for chunk in chunks:
        if any(word in chunk.lower() for word in question_lower.split()):
            relevant.append(chunk)
    return relevant[:3]  # limit to top 3 relevant chunks
