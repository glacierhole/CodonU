import requests
import streamlit as st
from PIL import Image
from io import BytesIO

# 设置页面标题
st.title("图片展示应用")

# 定义API地址
api_url = 'https://api.gumengya.com/Api/FjImg?format=image'

# 通过API获取图片数据
response = requests.get(api_url)

# 检查API响应状态码
if response.status_code == 200:
    # 从响应中获取图片数据
    image_data = response.content

    # 使用PIL库打开图片
    image = Image.open(BytesIO(image_data))

    # 显示图片
    st.image(image, caption='API返回的图片', use_column_width=True)
else:
    # 显示错误消息
    st.error(f"获取图片失败，状态码: {response.status_code}")
