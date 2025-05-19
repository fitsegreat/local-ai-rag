# Local AI RAG

This repository contains code and resources related to [Local AI Retrival Augemented Generation (RAG)](Local-RAG.md).

## Prerequsite
- Make sure [devbox](https://www.jetify.com/devbox) and [nix](https://nixos.org/) installed
- [Ollama](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [**qwen3:1.7b**](https://ollama.com/library/qwen3:1.7b) AI model for generation and [**nomic-embed-text**](https://ollama.com/library/nomic-embed-text) model for text embedding
- [Qdrant](https://qdrant.tech/documentation/guides/installation/) vector database
- [Docker](https://docs.docker.com/engine/install/)/[Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) to run the Qdrant database

## Instructions
1. Start the development environment
```sh
devbox shell
```
2. Make sure ollama is installed and the necessary model is available
```sh
ollama list

NAME                        ID              SIZE      MODIFIED
nomic-embed-text:latest     0a109f422b47    274 MB    6 hours ago
qwen3:1.7b                  458ce03a2187    1.4 GB    31 hours ago
```
3. Run Qdrant database
```sh
docker pull qdrant/qdrant
docker run -d -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;You can access the Qdrant UI at [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

4. Run the `upload_data.py` to upload the news articles in `data/` directory to Qdrant database. **NOTE - Run only once**
```sh
uv run upload_data.py
```
5. Run the `main.py` to start interacting with the application
```sh
uv run main.py
```
6. Enter a sample prompt
```
What's the relationship between Safaricom and EEU?
```