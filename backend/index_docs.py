import os
from pathlib import Path

from dotenv import load_dotenv
from opensearchpy import OpenSearch

load_dotenv()

INDEX_NAME = os.getenv("OPENSEARCH_INDEX", "gov-docs")
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", "9200"))

DATA_DIR = Path(__file__).resolve().parent / "data"


def get_client() -> OpenSearch:
    return OpenSearch(
        hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
        http_compress=True,
        use_ssl=False,
        verify_certs=False,
    )


def create_index(client: OpenSearch) -> None:
    if client.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists.")
        return

    mapping = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
            }
        },
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "source": {"type": "keyword"},
                "content": {"type": "text"},
            }
        },
    }

    client.indices.create(index=INDEX_NAME, body=mapping)
    print(f"Created index '{INDEX_NAME}'.")


def index_documents(client: OpenSearch) -> None:
    txt_files = sorted(DATA_DIR.glob("*.txt"))

    if not txt_files:
        print(f"No .txt files found in {DATA_DIR}")
        return

    for file_path in txt_files:
        content = file_path.read_text(encoding="utf-8").strip()

        if not content:
            print(f"Skipping empty file: {file_path.name}")
            continue

        doc = {
            "title": file_path.stem.replace("_", " ").title(),
            "source": file_path.name,
            "content": content,
        }

        response = client.index(
            index=INDEX_NAME,
            body=doc,
            refresh=True,
        )

        print(f"Indexed {file_path.name} -> {response['_id']}")


def main() -> None:
    client = get_client()
    create_index(client)
    index_documents(client)
    print("Done indexing documents.")


if __name__ == "__main__":
    main()