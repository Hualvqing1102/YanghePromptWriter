from data_preparation import prepare_data,get_parent_documents
from store import get_vector_store,ROOT
from datetime import datetime

docs,all_chunks = prepare_data()
vector_store = get_vector_store()

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
save_path = ROOT/'eval'/f"run_{ts}_chunks{len(all_chunks)}.md"
save_path.write_text('\n'.join(save_to_eval),encoding='utf-8')

