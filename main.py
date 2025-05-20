import ollama
from qdrant_client import QdrantClient

# Constants
COLLECTION_NAME = "blog_posts"

# Connect to Ollama API
ollama_client = ollama.Client(host="localhost")
# Get the vector embedding with nomic-embed-text
def get_vector_embedding(text):
    response = ollama_client.embeddings(
        model="mxbai-embed-large",
        prompt=text,
    )
    # This should return a vector of size 1024
    return response.embedding

# Initialize Qdrant client
qdrant_client = QdrantClient(host="localhost", port=6333)

# Ask & loop through the user for prompts
def ask_user_for_prompts():
    while True:
        user_input = input("Enter a prompt (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        # Check if the user input is empty
        if not user_input.strip():
            print("Please enter a valid prompt.")
            continue
        # Get the vector embedding for the user input
        vector = get_vector_embedding(user_input)
        # Search for similar vectors in the Qdrant collection
        results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            score_threshold=0.5,
            limit=5,
        ).points
        
        # Print the results
        # for i, item in enumerate(results):
        #     print(f"Score: {item.score}")
        #     print(f"Filename: {item.payload['filename']}")
        #     print(f"Date: {item.payload['news_date']}")
        #     print(f"Content: {item.payload['content'][:100]}...")

        # Merge the Qdrant data content list into a single string
        merged_content = "\n".join([item.payload["content"] for item in results])

        output = respond_to_user(merged_content, user_input)
        # Print the results
        print(f"Assistant: {output['message']['content']}")

# Respond to the user by augmenting it with Ollama
def respond_to_user(data, prompt):
    augmented_prompt = f"""Use this data: {data}. Respond to the user with the following prompt: {prompt}"""
    # Get the response from Ollama
    response = ollama_client.chat(
        model="qwen3:1.7b",
        messages=[
            {"role": "user", "content": augmented_prompt},
            {"role": "system", "content": "You are helpful Safaricom Ethiopia information desk employee. Respond in a conscise and informative manner."},
        ],
        stream=False,
    )
    return response

def main():
    ask_user_for_prompts()

if __name__ == "__main__":
    main()
