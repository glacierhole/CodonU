import requests
from bs4 import BeautifulSoup

# 替换为您要访问的 KEGG 页面的 URL
kegg_url = 'https://www.genome.jp/kegg-bin/show_pathway?hsa00010'

# 发起 HTTP 请求获取页面内容
response = requests.get(kegg_url)

# 检查请求是否成功
if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 在这里添加您的数据提取逻辑
    # 以下示例提取标题和基因信息
    title = soup.find('title').text
    gene_info = soup.find('div', class_='pathway-disease-gene-table').text

    # 打印结果
    print(f'Title: {title}')
    print(f'Gene Information: {gene_info}')
else:
    print(f'Error: Unable to fetch data. Status Code: {response.status_code}')
