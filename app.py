import streamlit as st
import requests
import os

# --- CONFIG ---
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
HF_TOKEN = st.secrets["HF_TOKEN"]

headers = {"Authorization": f"Bearer {HF_TOKEN}"}


def explain_tamil_poem(poem_text):
    prompt = f"""
நீங்கள் ஒரு தமிழ் இலக்கிய பேராசிரியர்.

கீழே உள்ள தமிழ் கவிதைக்கு:

1. நவீன தமிழில் சாராம்சம்
2. ஒவ்வொரு வரிக்கும் தனித்தனி விளக்கம்
3. முக்கிய கருத்து
4. இலக்கிய அம்சங்கள்

அமைப்பாக விளக்கவும்.

கவிதை:
{poem_text}
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.3
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.json()}"

    return response.json()[0]["generated_text"]


# --- STREAMLIT UI ---

st.title("📜 Tamil Poem Explainer")
st.write("Enter any Tamil poem and get structured explanation.")

poem_input = st.text_area("Enter Tamil Poem Here:")

if st.button("Explain"):
    if poem_input.strip() == "":
        st.warning("Please enter a poem.")
    else:
        with st.spinner("Analyzing poem..."):
            result = explain_tamil_poem(poem_input)
            st.write(result)


