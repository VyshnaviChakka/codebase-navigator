from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model (free)
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks, batch_size=64):
    all_embeddings = []

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        batch_embeddings = model.encode(batch)
        all_embeddings.extend(batch_embeddings)

        print(f"Processed {i + len(batch)} / {len(chunks)}")

    return np.array(all_embeddings)

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))
    return index