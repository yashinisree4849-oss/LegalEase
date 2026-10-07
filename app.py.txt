import streamlit as st
import google.generativeai as genai
from datetime import date

genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="LegalEase", page_icon="⚖️")
st.title("⚖️ LegalEase - AI Legal Document Generator")
st.caption("Disclaimer: AI generated draft only. Lawyer review is mandatory!")

col1, col2 = st.columns(2)
with col1:
doc_type = st.selectbox("Document Type", ["Rental Agreement", "NDA - Non Disclosure", "Employment Offer Letter", "Affidavit", "Service Agreement"])
with col2:
doc_date = st.date_input("Date", date.today())

st.divider()
st.subheader("Party Details")
p1_name = st.text_input("Party 1 / Owner / Company Name")
p1_address = st.text_input("Party 1 Address")
p2_name = st.text_input("Party 2 / Tenant / Employee Name")
p2_address = st.text_input("Party 2 Address")

extra = st.text_area("Important Clauses / Salary / Rent Amount / Duration (Tamil/English la type pannalam)", height=120)

if st.button("📄 Generate Legal Document"):
if p1_name and p2_name and extra:
with st.spinner("Drafting document..."):
prompt = f"""
You are LegalEase AI. Draft a simple, India-legal compliant {doc_type}
dated {doc_date} between {p1_name} ({p1_address}) and {p2_name} ({p2_address}).
Extra details: {extra}.
Structure: Title, Parties, Recitals, Terms & Conditions, Termination, Signature Section.
Language: Professional English. Add disclaimer at end: This is AI generated draft, consult advocate.
"""
response = model.generate_content(prompt)
st.success("Document Generated!")
st.write(response.text)
st.download_button("Download as .txt", response.text, file_name=f"{doc_type}.txt")
else:
st.warning("Party names & details fill pannu da!")

st.sidebar.markdown("**For:** NASSCOM FSP - Generative AI with Google Cloud Data")