import numpy as np

def search(query, model, index, chunks, top_k=5):
    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, top_k)

    results = []
    
    for i, idx in enumerate(indices[0]):
        score = distances[0][i]

        # Filter bad results (distance threshold)
        if score < 1.5:   # tune this value
            results.append(chunks[idx])

    return results