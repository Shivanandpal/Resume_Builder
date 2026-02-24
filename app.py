import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os

# ==============================
# API CONFIGURATION
# ==============================

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Google API key not found. Please set GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=API_KEY)

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(page_title="AI Resume Builder", layout="wide")

# ==============================
# GEMINI HELPER FUNCTION
# ==============================

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        if not response.text:
            return "No response generated."

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"

# ==============================
# PDF GENERATOR
# ==============================

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    text = text.encode('latin-1', 'replace').decode('latin-1')

    for line in text.split('\n'):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest='S').encode('latin-1')

# ==============================
# UI STARTS
# ==============================

st.title("🚀 AI Resume & Portfolio Builder")
st.subheader("Transform your raw data into professional career assets.")
st.caption("Powered by Google Gemini 1.5 Flash")

tab1, tab2, tab3 = st.tabs(["📝 Input Data", "📄 Resume & Cover Letter", "🌐 Portfolio Code"])

if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# ==============================
# TAB 1 - INPUT
# ==============================

with tab1:
    st.header("Step 1: Tell us about yourself")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        linkedin = st.text_input("LinkedIn URL")

    with col2:
        education = st.text_area("Education")
        skills = st.text_area("Skills (comma separated)")
        experience = st.text_area("Experience / Internships")
        projects = st.text_area("Projects")

    st.markdown("---")
    job_desc = st.text_area("Target Job Description (Optional)", height=150)

    if st.button("Save Data"):
        if not name or not email:
            st.warning("Name and Email are required.")
        else:
            st.session_state.user_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "linkedin": linkedin,
                "education": education,
                "skills": skills,
                "experience": experience,
                "projects": projects,
                "job_desc": job_desc[:1500]  # limit size for speed
            }
            st.success("Data saved successfully!")

# ==============================
# TAB 2 - DOCUMENTS
# ==============================

with tab2:
    st.header("Step 2: Generate Documents")

    if st.button("Generate Resume"):
        if not st.session_state.user_data:
            st.warning("Please fill your details first.")
        else:
            data = st.session_state.user_data

            prompt = f"""
Create a professional ATS-friendly resume.

Name: {data['name']}
Email: {data['email']}
Phone: {data['phone']}
LinkedIn: {data['linkedin']}

Education: {data['education']}
Skills: {data['skills']}
Experience: {data['experience']}
Projects: {data['projects']}
Target Job: {data['job_desc']}

Use strong action verbs.
Highlight measurable achievements.
Return clean plain text format.
"""

            with st.spinner("Generating resume... (5–15 seconds)"):
                resume_content = get_gemini_response(prompt)

            if resume_content.startswith("Error"):
                st.error(resume_content)
            else:
                st.text_area("Generated Resume", resume_content, height=500)

                pdf_bytes = create_pdf(resume_content)
                st.download_button(
                    "Download Resume as PDF",
                    pdf_bytes,
                    file_name="Generated_Resume.pdf",
                    mime="application/pdf"
                )

# ==============================
# TAB 3 - PORTFOLIO
# ==============================

with tab3:
    st.header("Step 3: Generate Portfolio Website")

    if st.button("Generate Portfolio Code"):
        if not st.session_state.user_data:
            st.warning("Please fill your details first.")
        else:
            data = st.session_state.user_data

            prompt = f"""
Create a modern responsive single-file HTML portfolio website.

Name: {data['name']}
About: {data['education']}
Skills: {data['skills']}
Projects: {data['projects']}
Contact: {data['email']}, {data['linkedin']}

Return only raw HTML code.
"""

            with st.spinner("Generating website... (5–15 seconds)"):
                portfolio_code = get_gemini_response(prompt)

            if portfolio_code.startswith("Error"):
                st.error(portfolio_code)
            else:
                clean_code = portfolio_code.replace("```html", "").replace("```", "")
                st.code(clean_code, language="html")

                st.components.v1.html(clean_code, height=600, scrolling=True)

                st.download_button(
                    "Download HTML File",
                    clean_code,
                    file_name="index.html",
                    mime="text/html"
                )