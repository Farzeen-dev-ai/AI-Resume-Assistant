import streamlit as st
import google.generativeai as genai
import PyPDF2

# Configure the Streamlit page
st.set_page_config(page_title="ATS Resume Analyzer", page_icon="📄", layout="centered")
st.title("📄 ATS Resume Analyzer")
st.write(# Create a 2-column layout for the most important takeaways
col1, col2 = st.columns([1, 2])

with col1:
    # This displays a large, stylized metric. 
    # (You can program the AI to output just a number later to make this dynamic)
    st.metric(label="ATS Match Score", value="38%") 

with col2:
    # This creates a highlighted callout box for the profile summary
    st.warning("Significant mismatch: Prioritize C++ and OOP concepts.")

# This places the dense list of missing keywords into a toggleable dropdown
with st.expander("View Missing Keywords Breakdown"):
    st.write(response.text)) # Replace 'response.text' with your actual AI output variable

# Securely capture the API key so it isn't hardcoded
api_key = st.secrets["GEMINI_API_KEY"]
job_description = st.text_area("Job Description", height=200, placeholder="Paste the job description here...")
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

def extract_pdf_text(file):
    """Reads the uploaded PDF and extracts all text."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text

def analyze_resume(api_key, resume_text, job_desc):
    """Sends the resume and job description to Gemini for ATS evaluation."""
    genai.configure(api_key=api_key)
    # gemini-1.5-pro is recommended for complex reasoning and formatting tasks
    model = genai.GenerativeModel('gemini-3.6-flash')

    prompt = f"""
    Act as a highly experienced Applicant Tracking System (ATS) and expert Technical HR Manager. 
    Review the following resume against the provided job description.

    Job Description:
    {job_desc}

    Resume Text:
    {resume_text}

    Provide a detailed evaluation with the exact following structure:
    1. **ATS Match Score:** A percentage score indicating how well the resume matches the job description.
    2. **Missing Keywords:** A list of important skills or keywords from the job description missing in the resume.
    3. **Profile Summary:** A brief summary of the candidate's fit for the role.
    4. **Suggestions for Improvement:** Actionable, specific advice to improve the resume for this job.
    """

    response = model.generate_content(prompt)
    return response.text

if st.button("Analyze Resume"):
    # Basic validation before making API calls
    if not api_key:
        st.warning("Please enter your Gemini API Key.")
    elif not job_description.strip():
        st.warning("Please provide the job description.")
    elif uploaded_file is None:
        st.warning("Please upload a PDF resume.")
    else:
        with st.spinner("Analyzing resume against job description..."):
            try:
                resume_text = extract_pdf_text(uploaded_file)
                if not resume_text.strip():
                    st.error("Could not extract text from the uploaded PDF. Please ensure it is a text-based PDF, not an image.")
                else:
                    result = analyze_resume(api_key, resume_text, job_description)
                    st.subheader("Evaluation Results")
                    st.markdown(result)
            except Exception as e:
                st.error(f"An API or processing error occurred: {e}")
