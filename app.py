# import streamlit as st
# import pypdf
# import io

# # --- App Title ---
# st.title("🧠 Intelligent Study Notes Agent")

# # --- PDF Uploader ---
# st.header("1. Upload your PDF")
# uploaded_file = st.file_uploader("Choose a PDF file to summarize and create a quiz from.", type="pdf")

# if uploaded_file is not None:
#     st.success(f"Successfully uploaded: {uploaded_file.name}")

#     # To read file as bytes
#     bytes_data = uploaded_file.getvalue()
#     bytes_io = io.BytesIO(bytes_data)

#     # Extract text from PDF
#     try:
#         pdf_reader = pypdf.PdfReader(bytes_io)
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text() or ""

#         # Store extracted text in session state
#         st.session_state.extracted_text = text

#         if text:
#             st.info("PDF content extracted successfully. Click the button below to summarize.")
#         else:
#             st.warning("Could not extract any text from the PDF. The file might be image-based or corrupted.")
#             st.stop()

#     except Exception as e:
#         st.error(f"An error occurred while reading the PDF: {e}")
#         st.stop()


#     # --- Summarizer ---
#     st.header("2. Generate Summary")
#     if st.button("Summarize Content"):
#         if 'extracted_text' in st.session_state:
#             # Placeholder for actual summarization call to Gemini
#             summary_placeholder = "This is a placeholder summary. In the final version, the Gemini CLI would be called to generate a high-quality summary of the content."
#             st.session_state.summary = summary_placeholder + "\n\n**First 500 characters of extracted text:**\n" + st.session_state.extracted_text[:500] + "..."

#     if 'summary' in st.session_state:
#         st.container(border=True).write(st.session_state.summary)

#         # --- Quiz Generator ---
#         st.header("3. Create a Quiz")
#         if st.button("Create Quiz"):
#              # Placeholder for actual quiz generation call to Gemini
#             quiz_placeholder = {
#                 "questions": [
#                     {
#                         "type": "mcq",
#                         "question": "This is a sample Multiple Choice Question. What is the capital of France?",
#                         "options": ["Berlin", "Madrid", "Paris", "Rome"],
#                         "answer": "Paris"
#                     },
#                     {
#                         "type": "short_answer",
#                         "question": "This is a sample Short Answer question. What is the main topic of the document?",
#                         "answer": "Answer would be based on the document content."
#                     },
#                     {
#                         "type": "true_false",
#                         "question": "This is a sample True/False question. The document discusses renewable energy.",
#                         "answer": "True/False based on content"
#                     }
#                 ]
#             }
#             st.session_state.quiz = quiz_placeholder

#     if 'quiz' in st.session_state:
#         st.subheader("Quiz Time!")
#         for i, q in enumerate(st.session_state.quiz['questions']):
#             with st.container(border=True):
#                 st.markdown(f"**Question {i+1}:** {q['question']}")
#                 if q['type'] == 'mcq':
#                     st.radio("Your answer:", q['options'], key=f"q{i}")
#                 elif q['type'] == 'short_answer':
#                     st.text_input("Your answer:", key=f"q{i}")
#                 elif q['type'] == 'true_false':
#                     st.radio("Your answer:", ["True", "False"], key=f"q{i}")
#         st.success("Quiz displayed. In a real app, you could add a 'Submit' button to check answers.")




import io
import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Load environment and configure Gemini ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Functions ---
def extract_pdf_text(uploaded_files):
    """Extract text from PDF(s)."""
    text = ""
    for file in uploaded_files:
        try:
            pdf_reader = PdfReader(io.BytesIO(file.getvalue()))
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            st.error(f"Failed to read {file.name}: {e}")
    return text

def generate_summary(text):
    """Generate a summary using Gemini CLI."""
    if not text.strip():
        return "No text available for summarization."
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(f"Summarize the following study notes in a student-friendly way:\n\n{text}")
    return response.text

def generate_quiz(text):
    """Generate a mixed-style quiz using Gemini CLI."""
    if not text.strip():
        return []
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(f"Create a quiz from the following text with multiple choice, true/false, and short answer questions:\n\n{text}")
    return response.text

def display_quiz(quiz_data):
    """Render quiz in Streamlit."""
    st.subheader("Quiz Time!")
    if isinstance(quiz_data, str):
        st.write(quiz_data)
        return
    for i, q in enumerate(quiz_data.get("questions", [])):
        st.markdown(f"**Question {i+1}:** {q['question']}")
        if q["type"] == "mcq":
            st.radio("Your answer:", q["options"], key=f"q{i}")
        elif q["type"] == "short_answer":
            st.text_input("Your answer:", key=f"q{i}")
        elif q["type"] == "true_false":
            st.radio("Your answer:", ["True", "False"], key=f"q{i}")
        st.markdown("---")

# --- Streamlit App ---
def main():
    st.set_page_config(page_title="Study Notes Summarizer & Quiz Generator", page_icon=":books:", layout="wide")
    st.title("🧠 Study Notes Summarizer & Quiz Generator Agent")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["PDF Summarizer", "Quiz Generator"])

    uploaded_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        text = extract_pdf_text(uploaded_files)
        st.session_state["pdf_text"] = text
        if text:
            st.success(f"Extracted text from {len(uploaded_files)} PDF(s).")
        else:
            st.warning("No text extracted. PDF might be image-based or corrupted.")

    # --- PDF Summarizer ---
    if page == "PDF Summarizer":
        st.header("Generate Summary")
        if st.button("Summarize"):
            if "pdf_text" in st.session_state and st.session_state["pdf_text"]:
                with st.spinner("Generating summary..."):
                    summary = generate_summary(st.session_state["pdf_text"])
                    st.session_state["summary"] = summary
                    st.success("Summary generated!")
            else:
                st.warning("Please upload PDF(s) first.")
        if "summary" in st.session_state:
            st.markdown(st.session_state["summary"])

    # --- Quiz Generator ---
    elif page == "Quiz Generator":
        st.header("Generate Quiz from Study Notes")
        if st.button("Create Quiz"):
            if "pdf_text" in st.session_state and st.session_state["pdf_text"]:
                with st.spinner("Creating quiz..."):
                    quiz = generate_quiz(st.session_state["pdf_text"])
                    st.session_state["quiz"] = quiz
                    st.success("Quiz created!")
            else:
                st.warning("Please upload PDF(s) first.")
        if "quiz" in st.session_state:
            display_quiz(st.session_state["quiz"])

if __name__ == "__main__":
    main()
