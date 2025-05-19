import os
import ollama
from uuid import uuid4
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Constants
COLLECTION_NAME = "blog_posts"

# connect to local Qdrant database and create a collection if not exists
def connect_to_qdrant():
    # Initialize Qdrant client
    qdrant_client = QdrantClient(host="localhost", port=6333)
    # Create a collection if it doesn't already exist
    if not qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1024,
                distance=Distance.COSINE
            ),
        )
        print(f"Collection '{COLLECTION_NAME}' created.")
    return qdrant_client

# upsert a vector embedding to the collection received from the user
def upsert_vector(qdrant_client, vector, payload):
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            {
                "id": str(uuid4()),
                "vector": vector,
                "payload": payload
            }
        ]
    )

# Connect to Ollama API
ollama_client = ollama.Client(host="172.18.224.1")
# Get the vector embedding with nomic-embed-text
def get_vector_embedding(text):
    response = ollama_client.embeddings(
        model="mxbai-embed-large",
        prompt=text,
    )
    # This should return a vector of size 1024
    return response.embedding

# Loop through txt files in data/ directory,
# Get the content of each file,
# Get the vector embedding and upsert it to the Qdrant collection
def process_files():
    for filename in os.listdir("data/"):
        if filename.endswith(".txt"):
            with open(os.path.join("data/", filename), "r") as file:
                content = file.read()
                # Update the first line with "Event date"
                news_date = content.splitlines()[0]
                vector = get_vector_embedding(content)
                upsert_vector(
                    qdrant_client,
                    vector=vector,
                    payload={"filename": filename, "content": content, "news_date": news_date}
                )
                print(f"Upserted vector for {filename} to Qdrant collection '{COLLECTION_NAME}'")

# Initialize Qdrant client
qdrant_client = connect_to_qdrant()

def main():
    process_files()

if __name__ == "__main__":
    main()
