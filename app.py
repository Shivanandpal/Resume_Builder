import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# --- API CONFIGURATION (HARDCODED) ---
# ⚠️ WARNING: Never upload this file to GitHub with your key inside!
GOOGLE_API_KEY = "AIzaSyCj8xyFZY1MEMIHAIAJjZ3_DhaD3pOS26o"

# Configure the API immediately


# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Career Architect", layout="wide")

# --- GEMINI MODEL HELPER ---

genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_response(prompt):
    if GOOGLE_API_KEY == "PASTE_YOUR_GOOGLE_API_KEY_HERE":
        return "Error: You forgot to replace the API key placeholder in the code!"

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


# --- PDF GENERATOR FUNCTION ---
def create_pdf(text, filename="document.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    # Simple cleanup for unicode characters (emojis/bullets) that FPDF might break on
    # replacing them with standard equivalents
    text = text.encode('latin-1', 'replace').decode('latin-1')
    
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    
    return pdf.output(dest='S').encode('latin-1')

# --- MAIN UI ---
st.title("🚀 AI Resume & Portfolio Builder")
st.subheader("Transform your raw data into professional career assets.")
st.caption("Powered by Google Gemini Pro")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["📝 Input Data", "📄 Resume & Cover Letter", "🌐 Portfolio Code"])

# GLOBAL VARS TO STORE DATA
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# --- TAB 1: INPUTS ---
with tab1:
    st.header("Step 1: Tell us about yourself")
    st.info("Fill in the details below and click 'Save Data'.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", placeholder="Jane Doe")
        email = st.text_input("Email", placeholder="jane@example.com")
        phone = st.text_input("Phone", placeholder="+1 234 567 890")
        linkedin = st.text_input("LinkedIn URL")
        
    with col2:
        education = st.text_area("Education", placeholder="e.g., B.Tech in CS from XYZ University, GPA 9.0, 2021-2025")
        skills = st.text_area("Skills (comma separated)", placeholder="Python, ML, Streamlit, SQL, Leadership")
        experience = st.text_area("Experience / Internships", placeholder="e.g., Data Science Intern at ABC Corp. Worked on... (Add dates and key metrics)")
        projects = st.text_area("Projects", placeholder="e.g., Built a chatbot using NLP. Tech stack: Python, NLTK...")

    st.markdown("---")
    st.subheader("Target Job (Optional but Recommended)")
    job_desc = st.text_area("Paste the Job Description (JD) here to tailor your resume:", height=150)
    
    if st.button("Save Data"):
        if not name or not email:
            st.warning("Please at least provide Name and Email.")
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
                "job_desc": job_desc
            }
            st.success("Data saved successfully! Go to the next tabs to generate content.")

# --- TAB 2: DOCUMENTS ---
with tab2:
    st.header("Step 2: Generate Documents")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("ATS-Friendly Resume")
        if st.button("Generate Resume"):
            if not st.session_state.user_data:
                st.warning("Please fill in your data in Step 1 first.")
            else:
                data = st.session_state.user_data
                prompt = f"""
                Act as an expert Resume Writer and Career Coach. 
                Create a professional, ATS-friendly resume for the following candidate.
                
                PERSONAL DETAILS:
                Name: {data['name']}
                Email: {data['email']}
                Phone: {data['phone']}
                LinkedIn: {data['linkedin']}
                
                EDUCATION: {data['education']}
                SKILLS: {data['skills']}
                EXPERIENCE: {data['experience']}
                PROJECTS: {data['projects']}
                
                TARGET JOB DESCRIPTION:
                {data['job_desc']}
                
                INSTRUCTIONS:
                1. Structure the resume professionally (Summary, Skills, Experience, Projects, Education).
                2. Use strong action verbs.
                3. Tailor the keywords to match the Target Job Description provided.
                4. Highlight quantitative results in the experience section.
                5. Output plain text suitable for copying or PDF conversion. Do not use Markdown bolding (**) just standard text formatting.
                """
                
                with st.spinner("AI is crafting your resume..."):
                    resume_content = get_gemini_response(prompt)
                    st.text_area("Generated Resume", resume_content, height=600)
                    
                    # PDF Download
                    if "Error" not in resume_content:
                        pdf_bytes = create_pdf(resume_content)
                        st.download_button(
                            label="Download Resume as PDF",
                            data=pdf_bytes,
                            file_name="Generated_Resume.pdf",
                            mime="application/pdf"
                        )

    with col_b:
        st.subheader("Tailored Cover Letter")
        if st.button("Generate Cover Letter"):
            if not st.session_state.user_data:
                st.warning("Please fill in your data in Step 1 first.")
            else:
                data = st.session_state.user_data
                prompt = f"""
                Write a compelling cover letter for {data['name']} applying for the role described below.
                
                CANDIDATE SKILLS: {data['skills']}
                CANDIDATE EXPERIENCE: {data['experience']}
                TARGET JOB DESCRIPTION: {data['job_desc']}
                
                INSTRUCTIONS:
                1. Keep it professional yet engaging.
                2. Explain why the candidate is a perfect fit based on the provided JD.
                3. Keep it under 300 words.
                """
                
                with st.spinner("Writing cover letter..."):
                    cover_letter = get_gemini_response(prompt)
                    st.text_area("Generated Cover Letter", cover_letter, height=600)
                    
                    if "Error" not in cover_letter:
                        st.download_button(
                            label="Download Cover Letter",
                            data=cover_letter,
                            file_name="Cover_Letter.txt"
                        )

# --- TAB 3: PORTFOLIO ---
with tab3:
    st.header("Step 3: Personal Portfolio Website")
    st.write("Generate code for a personal portfolio website based on your profile.")
    
    if st.button("Generate Portfolio Code"):
         if not st.session_state.user_data:
                st.warning("Please fill in your data in Step 1 first.")
         else:
            data = st.session_state.user_data
            prompt = f"""
            Create a single-file HTML/CSS/JS code for a responsive, modern personal portfolio website for {data['name']}.
            
            Use the following data:
            - About: {data['education']}
            - Skills: {data['skills']}
            - Projects: {data['projects']}
            - Contact: {data['email']}, {data['linkedin']}
            
            DESIGN STYLE:
            - Minimalist, dark mode capable.
            - Use a nice sans-serif font.
            - Include a 'Download Resume' button placeholder.
            
            OUTPUT:
            Provide ONLY the raw HTML code inside a code block. Do not add explanations.
            """
            
            with st.spinner("Coding your website..."):
                portfolio_code = get_gemini_response(prompt)
                
                # Clean up the code block markdown if present
                clean_code = portfolio_code.replace("```html", "").replace("```", "")
                
                st.code(clean_code, language="html")
                
                # Preview (Sandboxed)
                st.subheader("Preview")
                st.components.v1.html(clean_code, height=600, scrolling=True)
                
                st.download_button(
                    label="Download HTML File",
                    data=clean_code,
                    file_name="index.html",
                    mime="text/html"
                )