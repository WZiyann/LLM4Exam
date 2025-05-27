from sentence_transformers import SentenceTransformer
import faiss, pickle

questions = ["什么是牛顿第一定律？", "质能方程是什么？", "概率的加法规则是什么？"]
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode(questions)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

with open("id2question.pkl", "wb") as f:
    pickle.dump({i: q for i, q in enumerate(questions)}, f)

faiss.write_index(index, "vector.index")
