import streamlit as st
import pandas as pd
from webdav4.client import Client
import os
from datetime import datetime
from datetime import timedelta
from datetime import timezone


########3.1目标规范留言时间
# username 为坚果云账号，password 为刚刚创建的密码
JIANGUO_NAME = st.secrets["JIANGUO_NAME"]
JIANGUO_TOKEN = st.secrets["JIANGUO_TOKEN"]
client = Client(base_url='https://dav.jianguoyun.com/dav/',
                auth=(JIANGUO_NAME, JIANGUO_TOKEN))

# 指定本地保存下载文件的路径
remote_file_path = '/streamlit_app/codonMessage.txt'
local_file_path = 'data/codonMessage.txt'
# 添加内容
st.title("留言板")
st.markdown("有什么建议和改进可以在这里提出哦")
# 侧边栏用于输入新留言
user_input = st.text_input("输入你的名字", "匿名用户")
new_message = st.text_area("输入留言", "")
client.download_file(remote_file_path, to_path=local_file_path)
# 当用户按下提交按钮时，将新留言添加到数据框中
if st.button("提交留言"):
    # 北京时间
    SHA_TZ = timezone(timedelta(hours=8),name='Asia/Shanghai',)
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    beijing_now = utc_now.astimezone(SHA_TZ)
    formatted_beijing_now = beijing_now.strftime('%Y-%m-%d %H:%M')
    # 追加到留言文档中
    with open(local_file_path, 'a', encoding='utf-8') as file:
    # 将用户输入的内容写入文件，同时在两列之间用制表符隔开
        file.write(f"\n{user_input}\t{new_message}\t{formatted_beijing_now}")
    try:
        client.upload_file(from_path=local_file_path, to_path=remote_file_path, overwrite=True)
        st.success("留言提交成功！")
    except Exception as e:
        # 这个出错会把报错内容传上来。
        st.error(f"提交留言时出错：{e}")

# 开始展示下载文件
if st.button("显示留言"):
    try:
        # 下载文件
        client.download_file(remote_file_path, to_path=local_file_path)
        # 使用文件流对象创建一个 DataFrame
        df = pd.read_csv(local_file_path, sep='\t', header=0)
        # 逐行逐列展示 DataFrame
        df
    except Exception as e:
        st.error(f"显示留言时出错：{e}")

