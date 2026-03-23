import sys
import logging

print("Loading libraries...", flush=True)

try:
    from qdrant_client import QdrantClient
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

print("Initialize Qdrant...", flush=True)
qdrant = QdrantClient(host="localhost", port=6333)
try:
    collections = qdrant.get_collections()
    print(f"Collections found: {[c.name for c in collections.collections]}", flush=True)
except Exception as e:
    print(f"Failed to connect to Qdrant: {e}")
    sys.exit(1)

print("Initialize Model (this may take a minute to download weights)...", flush=True)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

query = "My name is Paul Iusztin. Could you draft a LinkedIn post discussing RAG systems?"
query_vector = model.encode(query).tolist()

for collection_name in ["embedded_articles", "embedded_posts", "embedded_repositories"]:
    print(f"\n--- Searching {collection_name} ---", flush=True)
    try:
        hits = qdrant.search(collection_name=collection_name, query_vector=query_vector, limit=2)
        if not hits:
            print("No hits found.")
        for i, hit in enumerate(hits):
            content = hit.payload.get("content", "") if hit.payload else ""
            print(f"[{i+1}] Score: {hit.score:.4f} | Content Snippet: {content[:300]}...\n")
    except Exception as e:
        print(f"Collection {collection_name} not properly initialized or empty: {e}")

print("Test Finished!", flush=True)
