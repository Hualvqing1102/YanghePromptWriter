import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HUB_DISABLE_XET'] = "1"
os.environ['HF_HUB_OFFLINE'] = "1"
from pathlib import Path
from data_preparation import prepare_data,get_parent_documents
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from datetime import datetime

INDEX_DIR = Path(__file__).resolve().parents[1] / 'index'
docs,all_chunks = prepare_data()

embeddings = HuggingFaceEmbeddings(
    model_name = 'BAAI/bge-m3',
    encode_kwargs = {'normalize_embeddings':True},
)

vector_store = Chroma(
    persist_directory = str(INDEX_DIR),
    collection_name = 'prompt_chunks',
    embedding_function = embeddings,
)

questions = [
    '怎么防止提示词注入攻击？',
    '系统提示词泄露有什么风险？',
    '如何写少样本提示？',
    '怎么让模型一步步推理？',
    '帮我写一个代码审查的 Prompt',
]

save_to_eval = []
for question in questions:
    print(f'\n===== 问题: {question} =====')
    save_to_eval.append(f'\n===== 问题: {question} =====')
    chunk_list = []
    answer = vector_store.similarity_search_with_score(question,filter={'is_noise':'no'}, k=5)
    for chunk, score in answer:
        print(f"score: {score:.3f},title:{chunk.metadata['title']},{chunk.metadata.get('H2')}")
        save_to_eval.append(f"score: {score:.3f},title:{chunk.metadata['title']},{chunk.metadata.get('H2')}")
        chunk_list.append(chunk)
    text = get_parent_documents(chunk_list, docs)
    print(f"来源文档：\n")
    save_to_eval.append(f"来源文档：\n")
    for d in text:
        print(d.metadata['title'])
        save_to_eval.append(d.metadata['title'])

ts = datetime.now().strftime('%m%d_%H%M')
save_path = Path(__file__).resolve().parents[1]/'eval'/f"run_{ts}_chunks{len(all_chunks)}.md"
save_path.write_text('\n'.join(save_to_eval),encoding='utf-8')

