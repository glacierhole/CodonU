import streamlit as st
import requests
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

    # 调试语句，输出图像数据的长度
    st.write(f"Image data length: {len(image_data)}")

    # 在容器中显示图像
    st.image(image_data, caption='风景图', use_column_width=True)
