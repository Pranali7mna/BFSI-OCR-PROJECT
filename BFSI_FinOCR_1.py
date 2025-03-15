import pytesseract
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import base64
import pandas as pd
import streamlit as st

# 📌 Set Background with a Beautiful Image
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        h1, h2, h3, h4, p, label {{
            color: #000000;
            text-align: center;
            font-family: 'Arial', sans-serif;
        }}
        .sidebar .sidebar-content {{
            background: linear-gradient(135deg, rgba(0, 150, 255, 0.7), rgba(0, 100, 200, 0.7));
            padding: 20px;
            border-radius: 15px;
        }}
        .stButton>button {{
            background: linear-gradient(135deg, #005c97, #363795);
            color: white;
            border-radius: 12px;
            padding: 12px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            transition: 0.3s ease-in-out;
        }}
        .stButton>button:hover {{
            background: linear-gradient(135deg, #363795, #005c97);
            transform: scale(1.05);
        }}
        .stTextArea, .stSelectbox, .stNumberInput {{
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 8px;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("C:/Users/hp/PycharmProjects/BFSI OCR Project/BFSI Code/bg.jpg")

# 📌 Set Sidebar Background
def set_sidebar_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_sidebar_background("C:/Users/hp/PycharmProjects/BFSI OCR Project/BFSI Code/sidebarimg.jpg")

# 📌 Sidebar Navigation
st.sidebar.markdown("<h1 style='color:#000000; font-weight: bold;'>FinOCR</h1>", unsafe_allow_html=True)
module = st.sidebar.radio("", [
    "📄 Image OCR Extraction",
    "🌎 Multilingual OCR",
    "📊 Data Insights & Visualization",
    "💰 AI Loan Recommendation",
    "📹 Real-Time Video OCR"
])

# 📌 OCR Extraction Function
def extract_text(image):
    return pytesseract.image_to_string(image)

# ✅ Image OCR Extraction
if module == "📄 Image OCR Extraction":
    st.markdown('<h3 style="color: white;">📄 Upload an Image for OCR</h3>', unsafe_allow_html=True)
    uploaded_image = st.file_uploader("Upload Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        extracted_text = extract_text(image)
        st.text_area("📜 Extracted Text", extracted_text, height=200)

# ✅ Multilingual OCR
elif module == "🌎 Multilingual OCR":
    st.markdown("<h3 style='color: white;'>🌎 Extract Text in Any Language!</h3>", unsafe_allow_html=True)
    lang_options = {"Marathi": "mar", "Hindi": "hin", "Telugu": "tel", "Tamil": "tam", "Arabic": "ara"}
    selected_lang = st.selectbox("🌍 Select Language", list(lang_options.keys()))
    uploaded_image = st.file_uploader("📂 Upload Document", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        extracted_text = pytesseract.image_to_string(image, lang=lang_options[selected_lang])
        st.text_area(f"📜 Extracted Text ({selected_lang})", extracted_text, height=200)

# ✅ Data Insights Visualization
elif module == "📊 Data Insights & Visualization":
    st.markdown("<h3 style='color: white;'>📄 OCR-based Document Classification & Visualization</h3>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("📂 Upload up to 5 Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded_files:
        extracted_texts = [extract_text(Image.open(img)) for img in uploaded_files]
        text_lengths = [len(text) for text in extracted_texts]
        labels = [f"Image {i + 1}" for i in range(len(uploaded_files))]
        fig, ax = plt.subplots()
        ax.pie(text_lengths, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

# ✅ AI Loan Recommendation
elif module == "💰 AI Loan Recommendation":
    st.markdown("<h3 style='color: white;'>🎓 Find the Best Education Loan</h3>", unsafe_allow_html=True)
    cgpa = st.number_input("📊 Enter CGPA (0-10)", min_value=0.0, max_value=10.0)
    cibil_score = st.number_input("🏦 Enter CIBIL Score (300-900)", min_value=300, max_value=900)
    exam_score = st.number_input("📜 Enter Exam Score (GATE/JEE/NEET)", min_value=0, max_value=500)
    if st.button("🔎 Find Loan Options"):
        loan_options = pd.DataFrame([
            {"Bank": "SBI Scholar Loan", "Interest Rate": "7.5%-9.0%", "Max Loan": "₹40L", "Repayment": "15 Years"},
            {"Bank": "HDFC Credila", "Interest Rate": "9.5%-12.5%", "Max Loan": "₹50L", "Repayment": "10 Years"}
        ])
        st.dataframe(loan_options)

# ✅ Real-Time Video OCR
elif module == "📹 Real-Time Video OCR":
    st.markdown("<h3 style='color: white;'>🎥 Capture text from live video streams</h3>", unsafe_allow_html=True)
    st.warning("⚠️ Webcam required.")
    if st.button("🎥 Start Video OCR"):
        cap = cv2.VideoCapture(0)
        stframe = st.empty()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(processed_frame, config="--psm 6")
            stframe.image(frame, channels="BGR", caption="Live Video Stream")
            st.text_area("📜 Live Extracted Text", text, height=200)
        cap.release()
        cv2.destroyAllWindows()
