import chromadb
from collections import Counter
from rag_project.ingestion.vector_store import PERSIST_DIRECTORY 


COLLECTION_NAME = "docs"


def main():

    client = chromadb.PersistentClient(
        path=str(PERSIST_DIRECTORY)
    )

    collections = client.list_collections()

    if not collections:
        print("No collections found")
        return

    print("\nCollections:")
    for c in collections:
        print(" -", c.name)

    collection = client.get_collection(COLLECTION_NAME)

    total = collection.count()

    print("\ncollection:", COLLECTION_NAME)
    print("chunks:", total)

    # 读取 metadata
    data = collection.get(include=["metadatas"])

    sources = Counter()

    for m in data["metadatas"]:
        source = m.get("source", "unknown")

        # 只保留文件名
        source = source.split("/")[-1]

        sources[source] += 1

    print("\nsources:")

    for src, count in sources.most_common():
        print(f" - {src}: {count}")


if __name__ == "__main__":
    main()