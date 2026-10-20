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

#初始化session_state:跨重跑保留的”存档区“
if 'prompt_text' not in st.session_state:
    st.session_state.prompt_text = ''
if 'prompt_sources' not in st.session_state:
    st.session_state.prompt_sources = []
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

#按钮 + 生成 （只有点击那一次会执行）
if st.button('生成',type='primary'):  #type = 'primary' 按钮显示为高亮主色
    with st.spinner('生成中……'):
        #try-expect- 防止API失败时页面显示一大片红色堆栈
        try:
            output, resources = generate_prompt(
                requirement, get_vector_store(), get_docs(), get_model()
            )
            st.session_state.prompt_text = output
            st.session_state.prompt_sources = resources
        except Exception as e:
            st.error(f'生成失败:{e}')

if st.session_state.prompt_text:
    st.divider()    #一条水平分割线，隔开输入区和结果区
    #渲染 Markdown：你的输出里那个 ```markdown 代码块会被渲染成带复制按钮的块
    st.markdown(st.session_state.prompt_text)
    #小字灰色说明，适合放"本次使用的资料"这类辅助信息
    #注意：原来的写法 f"本次使用的资料、".join(列表) 会把分隔符当成前缀重复拼，
    #正确做法是先 join 再拼前缀
    sources_text = "、".join(st.session_state.prompt_sources)
    st.caption(f"本次使用的资料：{sources_text}")