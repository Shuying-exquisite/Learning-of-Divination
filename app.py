import streamlit as st
import os
import fitz  # PyMuPDF
from io import BytesIO

# 创建目录
menu = {
    "简介": [
        ("我做这个程序的目的", "收集术数学习资料，方便自己随时随地的查看和下载；从目录开始每一个小标题是每一本经典古集。 "),
        ("我的 GitHub", "[点击这里访问我的 GitHub](https://github.com/Shuying-exquisite)"),
    ],
    "目录": [
        ("滴天髓", ""),
        ("三命通会", ""),
        ("四库存目 子平汇刊 5 穷通宝鉴评注", ""),
    ]
}

# 侧边栏目录
with st.sidebar:
    st.title("目录")
    
    # 选择章节
    selected_section = st.selectbox("选择章节:", list(menu.keys()))
    
    # 展开章节的小标题
    selected_topic = st.selectbox("选择小标题:", [item[0] for item in menu[selected_section]])

# 根据选择的小标题在主界面展示内容
if selected_section:
    st.title(selected_section)
    # 获取选中的小标题的内容
    for title, content in menu[selected_section]:
        if title == selected_topic:
            st.subheader(title)
            st.write(content)

            # 如果选择了 "滴天髓"，则提供 PDF 查看功能
            if title == "滴天髓":
                # 假设 PDF 文件在同一个文件夹中
                pdf_file_path = "滴天髓原文（刘基注）.pdf"  # 请确保文件名与实际文件匹配

                if os.path.exists(pdf_file_path):
                    # 使用 Streamlit 缓存文件路径等简单数据
                    @st.cache_data
                    def get_pdf_metadata(pdf_path):
                        # 使用 PyMuPDF 打开 PDF 文件并获取元数据
                        doc = fitz.open(pdf_path)
                        return doc.page_count  # 仅返回页数等简单数据

                    # 获取 PDF 元数据（例如页数）
                    total_pages = get_pdf_metadata(pdf_file_path)

                    # 允许用户输入页码
                    page_num = st.number_input("输入页码查看（1 到 52）", min_value=1, max_value=52, step=1)
 
                else:
                    st.error("找不到 PDF 文件，请确保文件存在并且路径正确。")

