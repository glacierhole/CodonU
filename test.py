import streamlit as st
import requests
import io
from PIL import Image
import time

def _max_width_(prcnt_width:int = 75):
    max_width_str = f"max-width: {prcnt_width}rem;"
    st.markdown(f""" 
                <style> 
                .block-container{{{max_width_str}}}
                </style>    
                """, 
                unsafe_allow_html=True,
    )
_max_width_(80)

# 使用 st.button 的返回值检测按钮是否被点击
if st.button('点击找到R送你的一张风景图'):
    # 创建一个空的输出容器
    container = st.empty()

    def getImageLink():
        return 'https://api.gumengya.com/Api/FjImg?format=image'

    def getImage(url):
        return requests.get(url).content

    def getDogeBytesIO():
        container = io.BytesIO()
        container.write(getImage(getImageLink()))
        return container

    loading_bar = st.progress(0.0, '加载风景中')
    time.sleep(0.1)
    loading_bar.progress(0.1, '加载风景ing')
    
    # 获取图像数据
    image_data = getDogeBytesIO()
    
    # 调试语句，输出图像数据的长度
    st.write(f"Image data length: {len(image_data)}")

    try:
        # 尝试打开图像
        pil_image = Image.open(io.BytesIO(image_data))
        st.write("Image opened successfully.")
    except Exception as e:
        # 打印异常信息
        st.error(f"Error opening image: {e}")

    loading_bar.progress(1.0, '快看')

    # 在容器中显示图像
    container.image(pil_image)
