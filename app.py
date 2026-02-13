import streamlit as st
import os
from openai import OpenAI
from pypdf import PdfReader

# Load API key safely from environment variable
client = OpenAI(api_key=os.getenv("DB_USERNAME = "myuser"
DB_TOKEN = "abcdef"

[some_section]
some_key = 1234"))

st.set_page_config(page_title="Tamil AI Literary Assistant")

st.title("📘 தமிழ் AI கல்வி உதவியாளர்")
st.write("தமிழ் கவிதையை பதிவேற்றுங்கள் (PDF / TXT) மற்றும் வரி வாரியாக விளக்கம் பெறுங்கள்.")

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("கவிதையை பதிவேற்றவும்", type=["pdf", "txt"])

def extract_text(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    else:
        return file.read().decode("utf-8")

if uploaded_file is not None:

    poem_text = extract_text(uploaded_file)

    # ---------- PREPROCESSING ----------
    lines = poem_text.split("\n")
    lines = [line.strip() for line in lines if line.strip() != ""]

    st.subheader("📜 அசல் கவிதை")
    st.write(poem_text)

    if st.button("விளக்கம் பெற"):

        analysis_results = []

        # ---------- LINE BY LINE PROCESSING ----------
        for line in lines:

            prompt = f"""
நீங்கள் ஒரு தமிழ் இலக்கிய ஆசிரியர்.

கொடுக்கப்பட்டுள்ள கீழே உள்ள தமிழ் வரியை:

1. எளிய நடுத்தர தமிழில் மாற்றவும்.
2. அதன் பொருளை தெளிவாக விளக்கவும்.
3. கடினமான சொற்களின் அர்த்தத்தை தனியாக குறிப்பிடவும்.

வெளியீடு வடிவம்:

எளிய தமிழ்:
பொருள் விளக்கம்:
சொற்களின் அர்த்தம்:

தமிழ் வரி:
{line}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            analysis_results.append({
                "original": line,
                "analysis": result
            })

        # ---------- FULL POEM ANALYSIS ----------
        summary_prompt = f"""
நீங்கள் ஒரு தமிழ் இலக்கிய ஆசிரியர்.

கொடுக்கப்பட்டுள்ள முழு கவிதைக்காக:

1. முழு சுருக்கம் எழுதவும்.
2. கவிதையின் கரு / முக்கிய கருத்து எழுதவும்.
3. மூன்று முக்கிய கேள்வி - பதில்கள் உருவாக்கவும்.

கவிதை:
{poem_text}
"""

        summary_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": summary_prompt}]
        )

        full_analysis = summary_response.choices[0].message.content

        # ---------- DISPLAY RESULTS ----------
        st.subheader("📖 வரி வாரியான விளக்கம்")

        for item in analysis_results:
            st.markdown(f"### 🔹 அசல் வரி:\n{item['original']}")
            st.write(item["analysis"])
            st.markdown("---")

        st.subheader("📚 முழு கவிதை பகுப்பு")
        st.write(full_analysis)

