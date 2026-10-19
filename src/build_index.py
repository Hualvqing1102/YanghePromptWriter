import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HUB_DISABLE_XET'] = "1"
os.environ['HF_HUB_OFFLINE'] = "1"
from pathlib import Path
from data_preparation import prepare_data
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

INDEX_DIR = Path(__file__).resolve().parents[1] / 'index'

_,all_chunks = prepare_data()

embeddings = HuggingFaceEmbeddings(
    model_name = 'BAAI/bge-m3',
    encode_kwargs = {'normalize_embeddings':True},
)

chroma = Chroma(
    persist_directory = str(INDEX_DIR),
    collection_name = 'prompt_chunks',
    embedding_function = embeddings,
)
chroma.reset_collection()
vector_store = Chroma.from_documents(
    documents = all_chunks,
    embedding = embeddings,
    persist_directory = str(INDEX_DIR),
    collection_name = 'prompt_chunks',
)

print(vector_store._collection.count())