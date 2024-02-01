import streamlit as st
import requests
from bs4 import BeautifulSoup

# Streamlit 页面布局设置
st.set_page_config(page_title="KEGG 数据展示", page_icon=":microscope:")

# KEGG 页面 URL
kegg_url = 'https://www.genome.jp/kegg-bin/show_pathway?hsa00010'

# 发起 HTTP 请求获取页面内容
response = requests.get(kegg_url)

# 检查请求是否成功
if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取标题和基因信息
    title = soup.find('title').text
    gene_info = soup.find('div', class_='pathway-disease-gene-table').text

    # Streamlit 中显示标题和基因信息
    st.title(title)
    st.text("Gene Information:")
    st.text(gene_info)
else:
    st.error(f'Error: Unable to fetch data. Status Code: {response.status_code}')
