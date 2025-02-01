import streamlit as st
import os
import fitz  # PyMuPDF
from io import BytesIO

def get_book_titles(folder_path):
    file_names = os.listdir(folder_path)
    book_titles = tuple(file_name.split(".")[0] for file_name in file_names if file_name.endswith(".pdf"))
    return book_titles
folder_path = "./"
book_titles = get_book_titles(folder_path)

def display_pdf_page(title):
    # 动态生成 PDF 文件路径，假设每本书的 PDF 文件名是书名 + ".pdf"
    pdf_file_path = f"{title}.pdf"

    if os.path.exists(pdf_file_path):
        # 使用 Streamlit 缓存文件路径等简单数据
        @st.cache_data
        def get_pdf_metadata(pdf_path):
            # 使用 PyMuPDF 打开 PDF 文件并获取元数据
            doc = fitz.open(pdf_path)
            return doc.page_count  # 返回总页数

        # 获取 PDF 元数据（例如页数）
        total_pages = get_pdf_metadata(pdf_file_path)

        # 允许用户输入页码
        page_num = st.number_input(f"输入页码查看（1 到 {total_pages}）", min_value=1, max_value=total_pages, step=1)

        # 使用容器显示图像
        with st.container():  # 添加容器来放置图像
            # 渲染当前页
            current_page_data = render_page(pdf_file_path, page_num)
            st.image(current_page_data, use_column_width=True)  # 图像自适应容器宽度

def render_page(pdf_path, page_num):
    doc = fitz.open(pdf_path)  # 每次需要打开 PDF 文件
    page = doc.load_page(page_num - 1)  # 页码从 1 开始，但 PyMuPDF 使用 0-based index
    zoom_x = 4.0  # 水平缩放
    zoom_y = 4.0  # 垂直缩放
    matrix = fitz.Matrix(zoom_x, zoom_y)
    pix = page.get_pixmap(matrix=matrix)  # 使用更高分辨率渲染页面
    img_data = pix.tobytes("png")
    return img_data

menu = {
    "简介": [
        ("我做这个程序的目的", "收集术数学习资料，方便自己随时随地的查看和下载；从目录开始每一个小标题是每一本经典古集。 "),
        ("我的 GitHub", "[点击这里访问我的 GitHub](https://github.com/Shuying-exquisite)"),
    ],
    "目录": []
}

# 将元组中的书名填入 "目录" 部分的小标题
for title in book_titles:
    menu["目录"].append((title, ""))

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

display_pdf_page(title)
