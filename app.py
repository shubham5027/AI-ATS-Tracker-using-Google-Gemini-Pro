from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
from streamlit_lottie import st_lottie
import requests
import google.generativeai as genai


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.set_page_config(layout="wide")

# st_lottie(load_lottie_url("https://assets9.lottiefiles.com/private_files/lf30_3scEHm.json"), speed=1, height=200, key='initial')

col1, col2 = st.columns(2)

with col1:
    st.header("AI Resume Analysis")
    input_text = st.text_area("Paste the Job Description here:", height=250)

with col2:
    st.header("Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file is not None:
        st.success("PDF Uploaded Successfully!")


submit1 = st.button("Analyze Resume Fit")
submit3 = st.button(" Calculate Match Percentage")


input_prompt1 = """As an ATS technical resource, you have been tasked with reviewing the attached candidate's resume to assess their suitability 
                  for the open position. Your task is to provide a detailed analysis of the candidate's qualifications, skills, and experience, as well as
                 any potential gaps or areas that may need further evaluation."""

input_prompt3 = """In your capacity as a highly skilled ATS (Applicant Tracking System) scanner, equipped with an in-depth 
                  understanding of data science, software development,cloud computing,cyber security and ATS functionality,
                    your mission is to conduct a thorough evaluation of the resume against the provided job description. 
                  Your output should include the percentage match between the resume and the job description. Additionally,
                    identify any keywords that may be missing in the resume, and conclude with your final thoughts on the candidate's suitability for the role."""

if submit1:
    with st.spinner(text='In progress...'):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("Professional Evaluation")
            st.write(response)
        else:
            st.error("Please upload a resume to proceed.")

elif submit3:
    with st.spinner(text='In progress...'):
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("Match Analysis")
            st.write(response)
        else:
            st.error("Please upload a resume to proceed.")

st.sidebar.header("Resume Tips")
st.sidebar.info(
    "1. Tailor your resume to the job description.\n"
    "2. Highlight your achievements with data.\n"
    "3. Use keywords from the job posting.\n"
    "4. Keep the format clean and professional."
)
