import streamlit as st
from PyPDF2 import PdfReader
import os

# 获取当前工作目录（应用程序所在的目录）
current_dir = os.path.dirname(os.path.abspath(__file__))

# 假设 PDF 文件与应用程序代码在同一文件夹下
pdf_folder = current_dir

# 列出文件夹中的所有PDF文件
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

# 让用户选择要阅读的 PDF 文件
selected_pdf = st.selectbox('选择要阅读的PDF书籍', pdf_files)

# 显示 PDF 文件内容
pdf_path = os.path.join(pdf_folder, selected_pdf)

# 读取并显示 PDF 文件的第一页内容
reader = PdfReader(pdf_path)
page = reader.pages[0]
st.text(page.extract_text())

# 提供下载链接
with open(pdf_path, 'rb') as pdf:
    st.download_button(
        label="下载 PDF",
        data=pdf,
        file_name=selected_pdf,
        mime="application/pdf"
    )
