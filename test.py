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
    pil_image = Image.open(io.BytesIO(image_data))

    loading_bar.progress(1.0, '快看')

    # 在容器中显示图像
    container.image(pil_image)
