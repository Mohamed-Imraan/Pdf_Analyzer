import streamlit as st
import requests
from pypdf import PdfReader

# Page config
st.set_page_config(
    page_title="AI Chat with PDF",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Chat with PDF")
st.write("Upload a PDF and ask questions about the document.")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    if text.strip() == "":
        st.error("No text found in the PDF.")
    else:

        st.success("PDF loaded successfully!")
        st.balloons()

        col1, col2 = st.columns(2)

        # Left column → document preview
        with col1:

            st.subheader("📑 Document Preview")

            with st.expander("Show extracted text"):
                st.write(text[:1500])

        # Right column → AI chat
        with col2:

            st.subheader("🤖 Ask AI")

            question = st.text_area(
                "Ask a question about the document",
                placeholder="Example: What is cloud computing?"
            )

            if st.button("Ask AI"):

                if question.strip() == "":
                    st.warning("Please enter a question.")

                else:

                    prompt = f"""
                    You are an AI assistant.

                    Use the document below to answer the question.

                    Document:
                    {text[:2500]}

                    Question:
                    {question}

                    Answer clearly.
                    """

                    with st.spinner("AI is thinking..."):

                        try:

                            response = requests.post(
                                "http://localhost:11434/api/generate",
                                json={
                                    "model": "llama2",
                                    "prompt": prompt,
                                    "stream": False
                                }
                            )

                            data = response.json()

                            if "response" in data:

                                st.success("Answer Generated")

                                st.write(data["response"])

                            else:
                                st.error("Unexpected response")
                                st.write(data)

                        except Exception as e:

                            st.error("Error connecting to Ollama")
                            st.write(e)