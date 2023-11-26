import streamlit as st
import pandas as pd
import os
import re
# --- 版本介绍 --- #
# 版本3.2 加page设定
# --- 部署的位置 --- #
# https://cyjcodon.streamlit.app/
# --- 更改的编辑部分 --- #
# 确定宿主
suzhu = "Cyberlindnera jadinii"
suzhuweb = "https://www.ncbi.nlm.nih.gov/datasets/genome/?taxon=4903"
suzhucodon = "codonset-cyj.txt"
suzhudataset = "GCA_001661405.1"
# 确定文件上传的位置
weizhi = "/streamlit_app/CodonU/cyj"
# --- UI设置 --- #
st.set_page_config(page_title=f"{suzhu}的稀有密码子打分",
                   page_icon="🐣",
                   layout="wide")
# --- 程序的主体部分 --- #
def main():
    # 基本信息介绍
    st.title(f"这是一个{suzhu}宿主的密码子偏好性预测程序")
    st.write("作者：饶一率")
    st.write("时间：2023-09-16")
    st.write("""## 物种信息""")
    st.write(f"{suzhu}基因组编码基因来源：[NCBI]({suzhuweb})")
    st.write(f"选择{suzhudataset}来进行统计得到{suzhu}密码子打分表")

main()
# --- 侧边栏的输入提示 --- #
with st.sidebar:
    st.image('picture/ulogo.png', use_column_width=True)
    ## 方式1
    st.write("""## 序列上传方式1""")
    seq_input = st.text_input("请输入DNA序列")
    ## 方式2
    st.write("""## 序列上传方式2""")
    # 创建一个文件夹用于保存上传的文件
    if not os.path.exists("data"):
        os.makedirs("data")
    st.write("请上传fasta类型的文件,fastq和txt也可以")
    uploaded_file = st.file_uploader("选择文件", type=["fasta","fastq","txt"])
    # 收尾介绍
    st.write("""## 模式生物的分析""")
    st.write("[外链侵权删](http://www.detaibio.com/tools/rare-codon-analyzer.html)")
    st.write("[欢迎留言提建议](https://codonmessage.streamlit.app)")
# --- 实现文件后台 --- #
from webdav4.client import Client
JIANGUO_NAME = st.secrets["JIANGUO_NAME"]
JIANGUO_TOKEN = st.secrets["JIANGUO_TOKEN"]
client = Client(base_url='https://dav.jianguoyun.com/dav/',
                auth=(JIANGUO_NAME, JIANGUO_TOKEN))
def save_file(uploaded_file):
    file_name = uploaded_file.name
    st.write(f"已上传文件名: {file_name}")
    file_path = os.path.join("data", file_name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    # 云盘后台保存
    remote_file_path = os.path.join(weizhi, file_name)
    local_file_path = file_path
    client.upload_file(from_path=local_file_path, to_path=remote_file_path, overwrite=True)
    return file_path
def start_analysis2(file_path,uploaded_file):
    st.write("""### 开始处理以下序列数据""")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    records = []
    with open(file_path) as f:
        for line in f:
            if line.startswith(">"):
                id = line[1:].strip()
            else:
                seq = line.strip()
                records.append({"id":id, "seq":seq})
    df = pd.DataFrame(records)
    df
    return df
def data_slicing2(seq_df):
    st.write("""### 将数据切割""")
    codons = [seq_df['seq'][0][i:i+3] for i in range(0, len(seq_df['seq'][0]), 3)]
    codons
    return codons
def start_analysis1(seq_input):
    st.write("""### 开始处理以下序列数据""")
    seq_input_upper = seq_input.upper()
    seq_input_upper
    return seq_input_upper
def data_slicing1(seq_input_upper):
    st.write("""### 将数据切割""")
    # 在这里执行下一步操作，例如将序列分成三联密码子
    codons = []
    for i in range(0, len(seq_input_upper), 3):
        codon = seq_input_upper[i:i+3]
        codons.append(codon)
    codons
    return codons
def codonset_show():
    st.write(f"""### 显示{suzhu}密码子打分表""")
    codonset = pd.read_csv(f'data/{suzhucodon}', sep='\t', header=None)
    codonset.columns = ['codon', 'abbc', 'num', 'percent', 'percent100', 'score']
    codonset
    return codonset
def cal_score(codons,codonset):
    st.write("""### 数据打分""")
    scores = []
    not_found = []
    # 遍历密码子计算分数
    num = 0
    for c in codons:
        c = c.upper()
        if c in codonset['codon'].values:
            num += 1
            score = codonset.loc[codonset['codon'] == c, 'score'].values[0]
            scores.append({'num': num, 'codon': c, 'score': score})
        else:
            not_found.append(c)
    #scores
    df_scores = pd.DataFrame(scores)
    df_scores
    return df_scores
def bar_chart(df_scores):
    st.write("""### 打分条形图""")
    df_scores['score'] = df_scores['score'].astype(float)
    st.bar_chart(df_scores, x='num', y='score')
def stacking_diagram(df_scores):
    st.write("""### 打分堆积图""")
    df_scores['score'] = df_scores['score'].astype(float)
    st.bar_chart(df_scores, x='codon', y='score')
def statistics_histogram(df_scores):
    st.write("""### 分数统计直方图""")
    df_scores['score'] = df_scores['score'].astype(float)
    counts = {'0-10': 0, '11-20': 0, '21-30': 0, '31-40': 0, '41-50': 0, '51-60': 0, '61-70': 0, '71-80': 0, '81-90': 0, '91-100': 0}
    for score in df_scores['score'].values:
        if 0 <= score <= 10:
            counts['0-10'] += 1
        elif 11 <= score <= 20:
            counts['11-20'] += 1
        elif 21 <= score <= 30:
            counts['21-30'] += 1
        elif 31 <= score <= 40:
            counts['31-40'] += 1
        elif 41 <= score <= 50:
            counts['41-50'] += 1
        elif 51 <= score <= 60:
            counts['51-60'] += 1
        elif 61 <= score <= 70:
            counts['61-70'] += 1
        elif 71 <= score <= 80:
            counts['71-80'] += 1
        elif 81 <= score <= 90:
            counts['81-90'] += 1
        elif 91 <= score <= 100:
            counts['91-100'] += 1
    st.bar_chart(counts)

# --- 上传文件进行分析 --- #
if uploaded_file is not None: 
    file_path = save_file(uploaded_file)
    seq_df= start_analysis2(file_path,uploaded_file)
    codons=data_slicing2(seq_df)
    codonset = codonset_show()
    df_scores =cal_score(codons,codonset)
    bar_chart(df_scores)
    stacking_diagram(df_scores)
    statistics_histogram(df_scores)
    
# --- 上传序列进行分析 --- #
if seq_input:
    seq_input_upper = start_analysis1(seq_input)
    codons = data_slicing1(seq_input_upper)
    codonset = codonset_show()
    df_scores =cal_score(codons,codonset)
    bar_chart(df_scores)
    stacking_diagram(df_scores)
    statistics_histogram(df_scores)
else:
    st.sidebar.warning("请输入DNA序列")

