from langchain_community.document_loaders import DirectoryLoader,TextLoader
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter
from collections import Counter
import re

md_path = Path(__file__).resolve().parents[1]/'raw'
md_glob = '**/*.md'
NOISE_HEADER_KEYWORDS = ('references', 'reference links', 'related frameworks', 'further reading', '参考')
MAX_NOISE_CHUNK_CHARS = 3000


def neutralize_code_headings(text):
    pattern = re.compile(r'^#{1,6}\s')
    lines = []
    in_code = False
    for line in text.splitlines():
        if line.lstrip().startswith('```'):
            in_code = not in_code
            lines.append(line)
            continue
        if in_code and pattern.match(line):
            lines.append('     ' + line)
        else:
            lines.append(line)
    return '\n'.join(lines)

def is_noise_chunk(chunk):
    h1 = str(chunk.metadata.get('H1','')).lstrip('*#: ').lower()
    h2 = str(chunk.metadata.get('H2','')).lstrip('*#: ').lower()
    h3 = str(chunk.metadata.get('H3','')).lstrip('*#: ').lower()
    if not h2 and not h3:
        return False
    if len(chunk.page_content) > MAX_NOISE_CHUNK_CHARS:
        return False
    title_hit = any(title.startswith(NOISE_HEADER_KEYWORDS) for title in [h1,h2,h3])
    lines = chunk.page_content.splitlines()
    if not lines:
        return False
    link_like = sum(1 for line in lines if '](' in line or 'http' in line)
    ratio = link_like / len(lines)
    return title_hit or ratio > 0.7

def prepare_data():
    loader = DirectoryLoader(
        path=md_path,
        glob=md_glob,
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[('#', 'H1'), ('##', 'H2'), ('###', 'H3')],
        strip_headers=False
    )
    docs = loader.load()
    all_chunks = []
    for doc in docs:
        p = Path(doc.metadata['source'])

        if '写法' in p.parts:
            doc.metadata['category'] = '写法'
        else:
            doc.metadata['category'] = '安全'

        doc.metadata['title'] = p.stem
        doc.metadata['doc_type'] = 'parent'
        doc.metadata['parent_id'] = str(p.relative_to(md_path))

        prepared_doc = neutralize_code_headings(doc.page_content)
        md_chunks = splitter.split_text(prepared_doc)

        for i, chunk in enumerate(md_chunks):
            chunk.metadata.update(doc.metadata)
            chunk.metadata['chunk_id'] = f"{chunk.metadata['parent_id']}#{i}"
            chunk.metadata['doc_type'] = 'child'
            chunk.metadata['chunk_index'] = i
            chunk.metadata['is_noise'] = 'yes' if is_noise_chunk(chunk) else 'no'
            all_chunks.append(chunk)
    noise = [chunk for chunk in all_chunks if chunk.metadata['is_noise'] == 'yes']
    return docs,all_chunks



def get_parent_documents(hit_chunks,documents):
    most_parent = Counter(c.metadata['parent_id'] for c in hit_chunks).most_common()
    parent_docs = []
    for pid, _ in most_parent:
        for doc in documents:
            if doc.metadata['parent_id'] == pid:
                parent_docs.append(doc)
                break

    return parent_docs
