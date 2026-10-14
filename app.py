import os
from datetime import date

import streamlit as st
import google.generativeai as genai

# ---------- Gemini setup ----------
API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

st.set_page_config(page_title="LegalEase", page_icon="⚖️")
st.title("⚖️ LegalEase - AI Legal Document Generator")
st.caption("Disclaimer: AI generated draft only. Lawyer review is mandatory!")

if not API_KEY:
    st.error("API key not found. Render > Environment la GOOGLE_API_KEY add pannunga.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-3.8-flash")

# ---------- Inputs ----------
DOC_TYPES = [
    "Rental Agreement",
    "NDA - Non Disclosure",
    "Employment Offer Letter",
    "Affidavit",
    "Service Agreement",
]

col1, col2 = st.columns(2)
with col1:
    doc_type = st.selectbox("Document Type", DOC_TYPES)
with col2:
    doc_date = st.date_input("Date", date.today())

st.divider()
st.subheader("Party Details")
p1_name = st.text_input("Party 1 / Owner / Company Name")
p1_address = st.text_input("Party 1 Address")
p2_name = st.text_input("Party 2 / Tenant / Employee Name")
p2_address = st.text_input("Party 2 Address")

extra = st.text_area(
    "Extra details (rent amount, duration, salary, job role, etc.)",
    height=120,
)

# ---------- Generate ----------
if st.button("Generate Document", type="primary"):
    if not p1_name or not p2_name:
        st.warning("Party 1 and Party 2 names kudunga.")
    else:
        prompt = f"""
You are a legal drafting assistant. Draft a professional {doc_type}.

Date: {doc_date}
Party 1: {p1_name}, Address: {p1_address}
Party 2: {p2_name}, Address: {p2_address}
Additional details: {extra if extra else "None"}

Rules:
- Use clear numbered clauses with headings.
- Include signature blocks for both parties at the end.
- Use simple, formal language.
- Do not invent facts that were not provided; leave blanks like ____ instead.
"""
        with st.spinner("Document generate aagudhu..."):
            try:
                response = model.generate_content(prompt)
                st.session_state["result"] = response.text
            except Exception as e:
                st.error(f"Error: {e}")

# ---------- Output ----------
if "result" in st.session_state:
    st.divider()
    st.subheader("Generated Document")
    st.markdown(st.session_state["result"])
    st.download_button(
        "Download as .txt",
        data=st.session_state["result"],
        file_name=f"{doc_type.replace(' ', '_')}.txt",
        mime="text/plain",
    )
