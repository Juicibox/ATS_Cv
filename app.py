from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, pdf_content, job_description):
    model = genai.GenerativeModel('gemini-1.5-flash')
    contents = [
        {"text": input_prompt},  # El prompt es texto
        {"mime_type": "image/jpeg", "data": pdf_content[0]['inline_data']},  # Ajuste para el contenido PDF
        {"text": job_description}  # Descripción del trabajo como texto
    ]
    response = model.generate_content(contents)
    #response = model.generate_content([input_prompt, pdf_content[0], job_description])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to images
        images = pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path=r'C:\Program Files\poppler\Library\bin')

        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "inline_data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("File not uploaded")

## Streamlit App+

st.set_page_config(page_title="ATS CV", page_icon="🔮")
st.header("ATS CV")

input_text = st.text_area("Descripción del trabajo", key="input_text")
uploaded_file = st.file_uploader("Cargue el CV en PDF", type=["pdf"])

if uploaded_file is not None:
    st.write("CV cargado")

# Submit buttons
submit1 = st.button("Cuéntame sobre el CV")
submit2 = st.button("Qué habilidades puede sumar al equipo")
submit3 = st.button("Porcentaje de match con el trabajo")

input_prompt1 = """
    You are an experienced Technical Human Resources Manager, 
    your task is to review the provided resume againts the job description. 
    Please share your professional evaluation on wheter the candidate's profile aligns with the job requirements.
    Hilights the strengths and weaknesses of the applicant in relation to the specific job requirements.
    Please answer all in spanish.
"""

input_prompt2 = """
    You are an Technical Human Resources Manager,
    your role is to scrutinize the resume and provide in tight of the job description provided.
    Shere your insights on the candidate's suitability for the job. from an HR prespective.
    Adittionally, offer advice on enhancing the candidate's skills and identifying areas for job.
    Please answer all in spanish.
"""
input_prompt3 = """
    you are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of the job requirements.
    Your task is to evaluate the resume against the provided job description. Give me the percentage of match between the resume and the job description.
    firt the output should come as percentage and then keywords.
    Please answer all in spanish.
"""


# Handling button clicks
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Respuesta")
        st.write(response)
    else:
        st.write("Por favor cargue el CV")

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("Respuesta")
        st.write(response)
    else:
        st.write("Por favor cargue el CV")

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Respuesta")
        st.write(response)
    else:
        st.write("Por favor cargue el CV")