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

st.button('Fetch Landscape wallpaper')


def getImageLink():
    return 'https://api.gumengya.com/Api/FjImg?format=image'

def getImage(url):
    return requests.get(url).content

def getDogeBytesIO():
    container = io.BytesIO()
    container.write(getImage(getImageLink()))
    return container

loading_bar = st.progress(0.0, '加载中')
time.sleep(0.1)
loading_bar.progress(0.1, '加载中')
image = getDogeBytesIO()
loading_bar.progress(1.0, '加载完成')
time.sleep(0.1)
loading_bar.image(image)