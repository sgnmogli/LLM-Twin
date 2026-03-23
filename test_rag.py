import sys

print("Starting script...", flush=True)

try:
    from llm_engineering.infrastructure.opik_utils import configure_opik

    print("Imported configure_opik", flush=True)
except Exception as e:
    print(f"Error importing configure_opik: {e}", flush=True)

try:
    from llm_engineering.application.rag.retriever import ContextRetriever

    print("Imported ContextRetriever", flush=True)
except Exception as e:
    print(f"Error importing ContextRetriever: {e}", flush=True)


print("Calling configure_opik()...", flush=True)
try:
    configure_opik()
    print("Done configure_opik()", flush=True)
except Exception as e:
    print(f"opik error: {e}", flush=True)

print("Initializing ContextRetriever...", flush=True)
try:
    retriever = ContextRetriever(mock=False)
    print("Done initializing ContextRetriever.", flush=True)

    print("Searching...", flush=True)
    query = "My name is Paul Iusztin. Could you draft a LinkedIn post discussing RAG systems?"
    documents = retriever.search(query, k=3)
    print("Search done!", flush=True)

    for rank, document in enumerate(documents):
        print(f"{rank + 1}: {document}", flush=True)
except Exception as e:
    print(f"RAG error: {e}", flush=True)
