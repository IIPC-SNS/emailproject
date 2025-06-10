import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import tempfile

# ---- Configure Gemini API Key ----
GEMINI_API_KEY = "AIzaSyCpB8-Yuw3d-HW6j5foqRIBHcKwA_Lt9ek"  # Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)

# ---- Title and Instructions ----
st.set_page_config(page_title="AI Email Generator", layout="centered")
st.title("📧 AI Email Generator using Gemini")
st.markdown("Enter your message context, choose a format and tone, and generate your email instantly!")

# ---- Sidebar: Format and Tone Options ----
st.sidebar.header("Email Options")
format_choice = st.sidebar.selectbox("Email Format", ["Formal", "Informal", "Professional", "Apologetic", "Promotional"])
tone_choice = st.sidebar.selectbox("Email Tone", ["Friendly", "Confident", "Polite", "Urgent", "Neutral"])

# ---- Input Text ----
input_text = st.text_area("✍️ Enter the context or content for the email:", height=200)

# ---- Session State ----
if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""

# ---- Generate Email Function ----
def generate_email(context, format_type, tone_type):
    prompt = f"""You are an email writing assistant.
    Write an email based on the following context:
    
    Context: {context}
    
    Format: {format_type}
    Tone: {tone_type}
    
    Provide only the email body."""
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

# ---- Generate Button ----
if st.button("Generate Email"):
    if input_text.strip():
        email = generate_email(input_text, format_choice, tone_choice)
        st.session_state.generated_email = email
    else:
        st.warning("Please enter some input text.")

# ---- Display Generated Email ----
if st.session_state.generated_email:
    st.subheader("📨 Generated Email")
    st.text_area("Email Output", st.session_state.generated_email, height=300)

    # ---- Download PDF Function ----
    def download_as_pdf(email_text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in email_text.split("\n"):
            pdf.multi_cell(0, 10, line)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf.output(tmp_file.name)
            return tmp_file.name

    # ---- PDF Download Button ----
    if st.download_button("📥 Download Email as PDF", data=open(download_as_pdf(st.session_state.generated_email), "rb").read(),
                          file_name="generated_email.pdf", mime="application/pdf"):
        st.success("Download ready!")

    # ---- Regenerate Button ----
    if st.button("🔁 Regenerate with New Format & Tone"):
        st.session_state.generated_email = generate_email(input_text, format_choice, tone_choice)

