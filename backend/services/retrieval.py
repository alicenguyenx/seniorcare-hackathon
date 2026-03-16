import os

from dotenv import load_dotenv
from opensearchpy import OpenSearch

load_dotenv()

OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", "9200"))
OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX", "gov-docs")


def get_client() -> OpenSearch:
    return OpenSearch(
        hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
        http_compress=True,
        use_ssl=False,
        verify_certs=False,
    )


def get_context(user_query: str, top_k: int = 3) -> str:
    client = get_client()

    search_body = {
        "size": top_k,
        "query": {
            "multi_match": {
                "query": user_query,
                "fields": ["title^2", "content"],
            }
        }
    }

    response = client.search(index=OPENSEARCH_INDEX, body=search_body)
    hits = response.get("hits", {}).get("hits", [])

    if not hits:
        return "No relevant documents found."

    context_parts = []
    for hit in hits:
        source = hit.get("_source", {})
        title = source.get("title", "Untitled")
        content = source.get("content", "")
        snippet = content[:1200].strip()
        context_parts.append(f"Source: {title}\n{snippet}")

    return "\n\n---\n\n".join(context_parts)
