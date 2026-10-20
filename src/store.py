import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HUB_DISABLE_XET'] = "1"
os.environ['HF_HUB_OFFLINE'] = "1"

from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = ROOT / 'index'
COLLECTION = 'prompt_chunks'
EMBED_MODEL = 'BAAI/bge-m3'
LLM_MODEL = 'deepseek-flash'
load_dotenv(ROOT / '.env')

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        encode_kwargs={'normalize_embeddings':True}
    )
def get_vector_store():
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=str(INDEX_DIR),
        collection_name=COLLECTION,
        embedding_function=embeddings,
    )
def get_llm():
    api_key = os.getenv('DEEPSEEK_API_KEY')
    return ChatOpenAI(
        model=LLM_MODEL,
        api_key=api_key,
        base_url='https://api.deepseek.com',
        temperature=0.3,
    )
def rebuild_vector_store(documents):
    '清空集合并用新的块列表重建向量库，返回新的库对象。'
    embeddings = get_embeddings()
    store = Chroma(
        persist_directory=str(INDEX_DIR),
        collection_name=COLLECTION,
        embedding_function=embeddings,
    )
    store.reset_collection()
    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(INDEX_DIR),
        collection_name=COLLECTION,
    )