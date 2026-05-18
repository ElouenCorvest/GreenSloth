from langchain_ollama import ChatOllama

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

from tqdm import tqdm
from pathlib import Path

model = ChatOllama(
    model="qwen3.5",
    validate_model_on_init=True,
    temperature=0.8,
    num_predict=256,
    # other params ...
)

embeddings = OllamaEmbeddings(model="qwen3-embedding")

vector_file = "nike_vectors.json"
if Path(vector_file).exists():
    vector_store = InMemoryVectorStore(embeddings).load(vector_file, embeddings)
else:
    file_path = "nke-10k-2023.pdf"
    loader = PyPDFLoader(file_path)

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)

    vector_store = InMemoryVectorStore(embeddings)

    for split in tqdm(all_splits):
        vector_store.add_documents([split])
        
    vector_store.dump(vector_file)
    
results = vector_store.similarity_search(
    "How much did Nike earn?"
)

print(results[0])