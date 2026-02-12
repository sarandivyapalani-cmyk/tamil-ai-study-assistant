import streamlit as st
from PIL import Image
import base64
import os
from openai import OpenAI

st.set_page_config(page_title="Tamil Study Assistant AI")

st.title("📘 Tamil Study Assistant AI")
st.subheader("Upload Tamil Image or Paste Tamil Text")

# API Key from Streamlit Secrets
client = OpenAI(api_key=st.secrets["1234"])

uploaded_image = st.file_uploader("Upload Tamil Image", type=["jpg", "jpeg", "png"])
user_text = st.text_area("Or Paste Tamil Text Here")

process_button = st.button("Process")

def encode_image(image):
    return base64.b64encode(image.read()).decode("utf-8")

if process_button:

    with st.spinner("Processing... Please wait."):

        if uploaded_image is not None:
            # Convert image to base64
            image_base64 = encode_image(uploaded_image)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract the Tamil text from this image and then simplify it with explanation, summary, 2-mark and 5-mark answers."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=2000,
            )

            result = response.choices[0].message.content
            st.write(result)

        elif user_text.strip() != "":
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
Convert the following Tamil text into:

1. Simple modern Tamil
2. Line-by-line explanation
3. Important word meanings
4. Overall summary
5. 2-mark answer
6. 5-mark answer

Tamil Text:
{user_text}
"""
                    }
                ],
                max_tokens=2000,
            )

            result = response.choices[0].message.content
            st.write(result)

        else:
            st.warning("Please upload an image or paste Tamil text.")
