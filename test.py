import streamlit as st
import requests
from PIL import Image
import io

def _max_width_(prcnt_width: int = 75):
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
    # 获取图像数据
    image_data = requests.get('https://api.gumengya.com/Api/FjImg?format=image').content

    # 尝试用 PIL 打开图像
    try:
        pil_image = Image.open(io.BytesIO(image_data))
        
        # 在容器中显示图像
        st.image(pil_image, caption='风景图', use_column_width=True)
    except Exception as e:
        # 打印异常信息
        st.error(f"Error opening image: {e}")
