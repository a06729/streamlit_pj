import base64
from io import BytesIO
import re
import uuid
import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OpenAi_key = os.environ.get('openai_apikey')

client = OpenAI(api_key=OpenAi_key)

# 이미지 생성 함수
def createImage():
    image_prompt = st.session_state.get("image_prompt", None)
    if image_prompt:
        response = client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
        image_url = response.data[0].url
        im = Image.open(requests.get(image_url, stream=True).raw)
        st.session_state["generated_image"] = im

# 초기 상태 설정
if "generated_image" not in st.session_state:
    st.session_state["generated_image"] = None

# 사이드바 설정
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("point", "freedraw", "line", "rect", "circle", "transform")
)
stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == 'point':
    point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
realtime_update = st.sidebar.checkbox("Update in realtime", True)

# 배경 이미지 설정
background_image = None

if "generated_image" in st.session_state and st.session_state["generated_image"] is not None:
    background_image = st.session_state["generated_image"]
elif bg_image:
    background_image = Image.open(bg_image)

# 캔버스 설정
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=background_image,
    update_streamlit=realtime_update,
    width=700,
    height=300,
    drawing_mode=drawing_mode,
    point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
    key="canvas",
)

# 이미지 프롬프트 입력 및 버튼 설정
image_prompt = st.text_input("프롬프트", key="image_prompt")
run_button = st.button("실행", on_click=createImage)

# 생성된 이미지 표시
# if st.session_state["generated_image"] is not None:
#     st.image(st.session_state["generated_image"], width=700)

# 다운로드 링크 생성
st.session_state["button_id"] = re.sub("\d+", "", str(uuid.uuid4()).replace("-", ""))
button_id = st.session_state["button_id"]
file_path = f"./temp/{button_id}.png"

custom_css = f""" 
    <style>
        #{button_id} {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: rgb(255, 255, 255);
            color: rgb(38, 39, 48);
            padding: .25rem .75rem;
            position: relative;
            text-decoration: none;
            border-radius: 4px;
            border-width: 1px;
            border-style: solid;
            border-color: rgb(230, 234, 241);
            border-image: initial;
        }} 
        #{button_id}:hover {{
            border-color: rgb(246, 51, 102);
            color: rgb(246, 51, 102);
        }}
        #{button_id}:active {{
            box-shadow: none;
            background-color: rgb(246, 51, 102);
            color: white;
            }}
    </style> """

data = canvas_result

if data is not None and data.image_data is not None and background_image is not None :
    image = background_image.convert("RGBA")
    
    drawn_image = Image.fromarray(canvas_result.image_data.astype(np.uint8)).convert("RGBA")
    drawn_image = drawn_image.resize(image.size, Image.Resampling.LANCZOS)
    
    final_image = Image.alpha_composite(image, drawn_image)
    final_image.save(file_path, "PNG")

    buffered = BytesIO()
    final_image.save(buffered, format="PNG")
    img_data = buffered.getvalue()
    try:
        b64 = base64.b64encode(img_data.encode()).decode()
    except AttributeError:
        b64 = base64.b64encode(img_data).decode()

    dl_link = (
        custom_css
        + f'<a download="{file_path}" id="{button_id}" href="data:file/txt;base64,{b64}">Export PNG</a><br></br>'
    )
    st.markdown(dl_link, unsafe_allow_html=True)

# 이미지 및 데이터프레임 표시
if canvas_result.image_data is not None:
    if background_image is not None and canvas_result.image_data is not None:
        image = background_image.convert("RGBA")
        
        drawn_image = Image.fromarray(canvas_result.image_data.astype(np.uint8)).convert("RGBA")
        drawn_image = drawn_image.resize(image.size, Image.Resampling.LANCZOS)
        
        final_image = Image.alpha_composite(image, drawn_image)
        st.image(final_image)
    else:
        st.image(canvas_result.image_data)

if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"])
    for col in objects.select_dtypes(include=['object']).columns:
        objects[col] = objects[col].astype("str")
    st.dataframe(objects)
