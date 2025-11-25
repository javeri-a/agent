# 🧠 Intelligent Study Notes Agent

This project is a Streamlit web application that acts as an intelligent study assistant. It allows users to upload a PDF, generate a concise summary of its content, and create a quiz to test their knowledge.

This agent was built by the Gemini CLI.

## ✨ Features

- **PDF Upload**: Upload any text-based PDF document.
- **Automatic Summarizer**: Generate a quick summary of the entire document's content.
- **Dynamic Quiz Generator**: Create a multi-format quiz (Multiple Choice, Short Answer, True/False) based on the PDF's text.
- **Simple UI**: A clean, easy-to-use interface built with Streamlit.

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- `pip` for package installation

### Installation

1.  Clone this repository or download the source code.
2.  Navigate to the project directory:
    ```bash
    cd path/to/your/project
    ```
3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  Ensure you are in the project's root directory.
2.  Run the Streamlit application from your terminal:
    ```bash
    streamlit run app.py
    ```
3.  The application will open in a new tab in your web browser.

## 🤖 Gemini CLI Integration (Simulation)

This prototype simulates the integration with a powerful generative model like the one powering Gemini CLI. The placeholders in the code mark where the actual API calls would be made.

### Gemini Prompt for Summarization

To generate the summary, the extracted text from the PDF would be sent to the model with a prompt like this:

```
Summarize the following text in a clean, structured, and meaningful way. The summary should be easy to read and capture the key points of the document.

---
[EXTRACTED PDF TEXT HERE]
---
```

### Gemini Prompt for Quiz Generation

To generate the quiz, the original extracted text would be used to ensure questions cover all key details.

```
Generate a quiz from the following text. Include a mix of question styles:
1. At least 3 Multiple Choice Questions (MCQs).
2. At least 2 Short-Answer Questions.
3. At least 2 True/False Questions.

Ensure the questions cover the main topics and key details from the text. For each question, provide the answer.

---
[EXTRACTED PDF TEXT HERE]
---
```

## 📸 Screenshots

As an AI, I cannot generate screenshots. However, running the Streamlit app will provide a clear visual of the user interface and workflow.
