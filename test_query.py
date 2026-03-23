from llm_engineering import settings
from llm_engineering.domain.cleaned_documents import (
    CleanedArticleDocument,
    CleanedPostDocument,
    CleanedRepositoryDocument,
)
import os

try:
    articles, _ = CleanedArticleDocument.bulk_find(limit=100)
except Exception as e:
    articles = [e]

try:
    posts, _ = CleanedPostDocument.bulk_find(limit=100)
except Exception as e:
    posts = [e]

try:
    repos, _ = CleanedRepositoryDocument.bulk_find(limit=100)
except Exception as e:
    repos = [e]

print("Articles:", len(articles) if articles else 0)
print("Posts:", len(posts) if posts else 0)
print("Repos:", len(repos) if repos else 0)
