import streamlit as st
import os
import fitz  # PyMuPDF
from io import BytesIO

# 创建目录
menu = {
    "简介": [
        ("我做这个程序的目的", "收集术数学习资料，方便自己随时随地的查看和下载 "),
        ("我的 GitHub", "[点击这里访问我的 GitHub](https://github.com/Shuying-exquisite)"),
    ],
    "目录": [
        ("滴天髓",""),
        ("st.write()：文本输出", "st.write() 是一个万能的输出函数，可以输出文本、表格、图形等。"),
        ("st.button()：按钮", "st.button('按钮') 创建一个按钮组件，用户点击后触发事件。"),
    ]
}

# 侧边栏目录
with st.sidebar:
    st.title("目录")
    
    # 选择章节
    selected_section = st.selectbox("选择章节:", list(menu.keys()))
    
    # 展开章节的小标题
    selected_topic = st.radio("选择小标题:", [item[0] for item in menu[selected_section]])

# 根据选择的小标题在主界面展示内容
if selected_section:
    st.title(selected_section)
    # 获取选中的小标题的内容
    for title, content in menu[selected_section]:
        if title == selected_topic:
            st.subheader(title)
            st.write(content)

            # 如果选择了 "机器学习西瓜书"，则提供 PDF 查看功能
            if title == "滴天髓":
                # 假设 PDF 文件在同一个文件夹中
                pdf_file_path = "滴天髓原文（刘基注）.pdf"  # 请确保文件名与实际文件匹配

                if os.path.exists(pdf_file_path):
                    # 使用 Streamlit 缓存 PDF 文件加载
                    @st.cache_resource
                    def load_pdf(pdf_path):
                        # 使用 PyMuPDF 打开 PDF 文件
                        doc = fitz.open(pdf_path)
                        return doc

                    # 加载 PDF 文件
                    doc = load_pdf(pdf_file_path)

                    # 获取总页数
                    total_pages = doc.page_count

                    # 允许用户输入页码
                    page_num = st.number_input("输入页码查看（1 到 10）", min_value=1, max_value=10, step=1)

                    # 渲染指定页面
                    def render_page(page_num):
                        page = doc.load_page(page_num - 1)  # 页码从 1 开始，但 PyMuPDF 使用 0-based index
                        # 提高渲染质量，增加渲染分辨率
                        zoom_x = 4.0  # 水平缩放
                        zoom_y = 4.0  # 垂直缩放
                        matrix = fitz.Matrix(zoom_x, zoom_y)
                        pix = page.get_pixmap(matrix=matrix)  # 使用更高分辨率渲染页面
                        img_data = pix.tobytes("png")
                        return img_data

                    # 使用容器显示图像
                    with st.container():  # 添加容器来放置图像
                        # 渲染当前页
                        current_page_data = render_page(page_num)
                        st.image(current_page_data, use_column_width=True)  # 图像自适应容器宽度

                else:
                    st.error("找不到 PDF 文件，请确保文件存在并且路径正确。")
