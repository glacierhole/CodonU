# --- Required Libraries and Modules --- #
import replicate
import streamlit as st
import requests
import zipfile
import io
from streamlit_image_select import image_select

# --- 版本介绍 --- #
# 文字的艺术工作室3.0 要实现与坚果云数据库进行通讯，保存好看图片，加数据后台
# --- 部署的位置 --- #
# https://tool-rao.streamlit.app/
# --- UI 配置 --- #
st.set_page_config(page_title="文字的艺术工作室",
                   page_icon="🐣",
                   layout="wide")
st.markdown("# :rainbow[文字的艺术工作室]")

# --- Initialize session state for generated images --- #
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None

# --- 隐藏起来的API --- #
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
REPLICATE_MODEL_ENDPOINTSTABILITY = st.secrets["REPLICATE_MODEL_ENDPOINTSTABILITY"]

# --- Elements --- #
with st.form("my_form"):
    st.info("**从这里开始你的作品吧**", icon="👋🏾")
    with st.expander(":rainbow[**改进你的图片作品**]"):
        # 高级设置(为好奇的头脑!)
        width = st.number_input("图像宽度", value=1024)
        height = st.number_input("图像高度", value=1024)
        num_outputs = st.slider(
            "生成的图片数量", value=1, min_value=1, max_value=4)
        scheduler = st.selectbox('调度程序', ('DDIM', 'DPMSolverMultistep', 'HeunDiscrete',
                                                'KarrasDPM', 'K_EULER_ANCESTRAL', 'K_EULER', 'PNDM'))
        num_inference_steps = st.slider(
                "去噪步骤数（增加去噪步骤的数量通常可以更有效地净化图像，但也可能导致过度平滑或丢失细节）", value=50, min_value=1, max_value=500)
        guidance_scale = st.slider(
                "无分类器引导的尺度（较大的比例或尺度可能意味着更强烈地依赖于与分类器无关的引导）", value=7.5, min_value=1.0, max_value=50.0, step=0.1)
        prompt_strength = st.slider(
                "使用img2img/inpaint(1.0)时的提示词对信息的修正程度", value=0.8, max_value=1.0, step=0.1)
        refine = st.selectbox(
                "选择要使用的精炼样式（通过选择一种样式，用户或算法可能决定专注于特定的风格或特征，而不考虑其他两种样式）", ("expert_ensemble_refiner", "None"))
        high_noise_frac = st.slider(
                "`expert_ensemble_refiner`用的噪声比例（0 表示没有噪声，1 表示全部使用噪声。）", value=0.8, max_value=1.0, step=0.1)
    prompt = st.text_area(
            ":orange[**输入提示: Rabbit ✍️**]",
            value="A super cute elf-style white fairy tale China Rabbit,smiling,big eyes,smiling,lively and cheerful smile,wearing an ice-blue wedding dress,with light shining on the wedding dress,fluffy hem and light,which is super dreamy and realistic rendering,shiny ice-blue fluffy,bright big eyes,smiling,fluffy tail,complete role concept,rainbow light,art station popularity,matte painting,fairy tales,ureal")
    negative_prompt = st.text_area(":orange[**你不想要在图片里出现的东东 🙅🏽‍♂️**]",
                                       value="the absolute worst quality, distorted features",
                                       help="This is a negative prompt, basically type what you don't want to see in the generated image")

        # The Big Red "Submit" Button!
    submitted = st.form_submit_button(
            "Submit", type="primary", use_container_width=True)

# --- 图像和图库的占位符 --- #
generated_images_placeholder = st.empty()
gallery_placeholder = st.empty()    

# --- Image Generation --- #
if submitted:
    with st.status('👩🏾‍🍳 正在把优美的字符变成图片艺术...', expanded=True) as status:
        st.write("⚙️ 正在使用replicate上的stability-ai模型...")
        st.write("🙆‍♀️ 正在跟我一起扭动脖子休息一下..")
        try:
            # Only call the API if the "Submit" button was pressed
            if submitted:
                # Calling the replicate API to get the image
                with generated_images_placeholder.container():
                    all_images = []  # List to store all generated images
                    output = replicate.run(
                        REPLICATE_MODEL_ENDPOINTSTABILITY,
                        input={
                            "prompt": prompt,
                            "width": width,
                            "height": height,
                            "num_outputs": num_outputs,
                            "scheduler": scheduler,
                            "num_inference_steps": num_inference_steps,
                            "guidance_scale": guidance_scale,
                            "prompt_stregth": prompt_strength,
                            "refine": refine,
                            "high_noise_frac": high_noise_frac
                        }
                    )
                    if output:
                        st.toast('Your image has been generated!', icon='😍')
                        # Save generated image to session state
                        st.session_state.generated_image = output

                        # Displaying the image
                        for image in st.session_state.generated_image:
                            with st.container():
                                st.image(image, caption="新鲜出炉的图片😍",
                                         use_column_width=True)
                                # Add image to the list
                                all_images.append(image)

                                response = requests.get(image)
                    # 将所有生成的图像保存到会话状态
                    st.session_state.all_images = all_images

                    # Create a BytesIO object
                    zip_io = io.BytesIO()

                    # 每个图像的下载选项
                    with zipfile.ZipFile(zip_io, 'w') as zipf:
                        for i, image in enumerate(st.session_state.all_images):
                            response = requests.get(image)
                            if response.status_code == 200:
                                image_data = response.content
                                # Write each image to the zip file with a name
                                zipf.writestr(
                                    f"output_file_{i+1}.png", image_data)
                            else:
                                st.error(
                                    f"Failed to fetch image {i+1} from {image}. Error code: {response.status_code}", icon="🚨")
                    # Create a download button for the zip file
                    st.download_button(
                        ":red[**下载所有图片**]", data=zip_io.getvalue(), file_name="picture_files.zip", mime="application/zip", use_container_width=True)
            status.update(label="✅ Images generated!",
                          state="complete", expanded=False)
        except Exception as e:
            st.error(f'Encountered an error: {e}', icon="🚨")

# If not submitted, chill here 🍹
else:
    pass

