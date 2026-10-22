from data_preparation import prepare_data
from generate import generate_prompt
from store import get_vector_store as _build_vector_store
from store import get_llm as _build_llm

import streamlit as st

#Streamlit 每次交互都会把整个脚本重跑一遍，所以重资源必须缓存：
#@st.cache_data 缓存"数据"（返回副本），@st.cache_resource 缓存"对象"（返回同一个实例）
@st.cache_data
def get_docs():
    docs,_ = prepare_data()
    return docs

@st.cache_resource
def get_vector_store():
    return _build_vector_store()

@st.cache_resource
def get_model():
    return _build_llm()

def extract_fence_body(text):
    start = text.find('````')
    end = text.rfind('````')
    if start == -1 or end <= start:
        return text
    body = text[start + 4: end]
    first_line, sep, rest = body.partition('\n')
    head = first_line.strip()
    if sep and head and len(head) <= 15 and head.isascii():
        body = rest
    return body

def build_effective_requirement(requirement,history,version):
    if version is None:
        return requirement
    item = next((h for h in history if h['version'] == version), None)
    if item is None:
        return requirement
    return f"{requirement}\n\n【上一版 Prompt（v{version}）】\n{item['prompt']}"

def append_history(requirement,output,sources):
    # 1. 从"已有历史列表"里取最大版本号，+1 得到本次版本号
    version = max([h['version'] for h in st.session_state.history], default=0) + 1
    # 2. 把本次结果打包成一条记录（一个字典）
    item = {
        'version': version,
        'requirement': requirement,
        'prompt': extract_fence_body(output),
        'sources': list(sources),
        'has_prompt': '````' in output,
    }
    # 3. 追加到历史列表里
    st.session_state.history.append(item)
    # 4. 返回版本号，供页面显示
    return version

#初始化session_state:跨重跑保留的”存档区“
if 'prompt_text' not in st.session_state:
    st.session_state.prompt_text = ''
if 'prompt_sources' not in st.session_state:
    st.session_state.prompt_sources = []
if 'history' not in st.session_state:
    st.session_state.history = []
if 'viewing_version' not in st.session_state:
    st.session_state.viewing_version = None
# session_state是什么？
# 它是一个跨重跑保留的字典，普通变量每次重跑都会被情况，但session_state里的东西会留下来。
# 用法和字典完全一样：
# 操作1：判断键是否存在
# if key not in dic
# 操作2：写
# dic.key = value == ( dic['key']=value)
# 操作3：读
# dic.key
#
# 如果不初始化的话，第一次运行时会话里什么都没有，直接读会报KeyError。这段if-not-只在第一次执行
#
# 默认值用''和[]，而不是None：
# 因为空字符串能安全的做 if判断 和 st.markdown 渲染；
# [] 能被join处理

#页面头
st.title("YanghePromptWriter")
st.markdown("基于 RAG 的提示词撰写助手：输入需求，系统从知识库检索资料并生成可直接使用的 Prompt。")

#输入区
requirement = st.text_area(
    "输入你的需求",
    height = 100,   #输入框高度（像素），比默认更宽松
    placeholder = '例如：帮我写一个能自动审查代码的 Prompt',    #灰色提示文字——用户没输入时显示的示例
)

labels = ['不基于任何版本（新建）']
values = [None]

for item in st.session_state.history:
    req = item['requirement'].replace('\n',' ').strip()
    if not req:
        summary = '无新要求'
    elif len(req) > 20:
        summary = req[:20] + '…'
    else:
        summary = req
    labels.append(f"v{item['version']} : {summary}")
    values.append(item['version'])

selected_label = st.selectbox(
    '版本选择',
    options=labels,
    index = 0,
    disabled = len(labels) == 1,
)
version_to_use = values[labels.index(selected_label)]

#按钮文字随状态变化
btn_view_label = (
    '返回最新结果' if st.session_state.viewing_version is not None
    else (f'查看 v{version_to_use} 原文' if version_to_use is not None else '查看原文')
)

#按钮 + 生成 （只有点击那一次会执行）
with st.container(horizontal=True,gap='small'):
    clicked_generate = st.button('生成', type='primary', disabled=not requirement.strip())
    clicked_view = st.button(
        label=btn_view_label,
        disabled=(version_to_use is None) and (st.session_state.viewing_version is None)
    )
if clicked_generate:
    with st.spinner('生成中……'):
        #try-expect- 防止API失败时页面显示一大片红色堆栈
        try:
            effective = build_effective_requirement(
                requirement,st.session_state.history,version_to_use
            )
            output, resources = generate_prompt(
                effective,
                get_vector_store(),
                get_docs(),
                get_model(),
                retrieval_qurery=requirement,
            )
            version = append_history(
                requirement,
                output,
                resources,
            )
            st.session_state.version = version
            st.session_state.prompt_text = output
            st.session_state.prompt_sources = resources
            st.session_state.viewing_version = None
        except Exception as e:
            st.error(f'生成失败:{e}')
if clicked_view:
    if st.session_state.viewing_version is None:
        st.session_state.viewing_version = version_to_use
    else:
        st.session_state.viewing_version = None

if st.session_state.prompt_text:
    st.divider()    #一条水平分割线，隔开输入区和结果区
    viewing = st.session_state.viewing_version

    if viewing is None:
        #正常 显示最新结果
        # 渲染 Markdown：你的输出里那个 ```markdown 代码块会被渲染成带复制按钮的块
        st.markdown(st.session_state.prompt_text)
        # 小字灰色说明，适合放"本次使用的资料"这类辅助信息
        # 注意：原来的写法 f"本次使用的资料、".join(列表) 会把分隔符当成前缀重复拼，
        # 正确做法是先 join 再拼前缀
        sources_text = "、".join(st.session_state.prompt_sources)
        st.caption(f"本次使用的资料：{sources_text}")
        st.caption(f"已保存为 v{st.session_state.get('version')}")
    else:
        #查看 用选中的那一版的原文覆盖上面全部内容
        item = next((h for h in st.session_state.history if h['version'] == viewing), None)
        if item is None:
            st.warning(f'找不到 v{viewing}')
        elif not item.get('has_prompt',True):
            st.info(f'v{viewing} 没有 Prompt 产出（拒绝/说明类回复）')
        else:
            req_summary = item['requirement'][:30] or '无新要求'
            st.caption(f"正在查看 v{viewing} · {req_summary}")
            st.code(item['prompt'], language='markdown')

st.divider()
if st.button('清空历史',disabled=not st.session_state.history):
    st.session_state.history = []
    st.session_state.viewing_version = None
    st.session_state.version = None
    st.session_state.prompt_text = ''
    st.session_state.prompt_sources = []