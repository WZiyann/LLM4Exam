from sentence_transformers import SentenceTransformer
import faiss
import pickle

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
index = faiss.read_index("vector.index")
with open("id2question.pkl", "rb") as f:
    id2question = pickle.load(f)

def search_similar_questions(query, top_k=5):
    vec = model.encode([query])
    D, I = index.search(vec, top_k)
    return [id2question[i] for i in I[0]]
