import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()  # to load the variables added in the .env file
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def get_pdf_text(pdf):
    text = ""

    for i in pdf:
        pdf_text = PdfReader(i)
        for page in pdf_text.pages:
            text += page.extract_text()

    return text


def convert_chuncks(text):
    split = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunk = split.split_text(text)

    return chunk


def convert_vector(chunk):
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector = FAISS.from_texts(chunk, embedding)
    vector.save_local("FAISS_vector")


def convo():
    template_str = """
  Answer the question in detail using the provided context. Ensure all relevant details are included. If the answer is not within the provided context, respond with "answer is not available in the context." Do not provide incorrect information.

  Context: {context}

  Question: {question}

  Answer:

"""

    model = ChatGoogleGenerativeAI(model="gemini-pro")

    prompt = PromptTemplate(template=template_str,
                            input_variables=["context", "question"])

    qa_chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return qa_chain


def user_input(question):
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    data = FAISS.load_local("FAISS_vector", embedding,
                            allow_dangerous_deserialization=True)

    docs = data.similarity_search(question)

    chain = convo()

    output = chain.invoke({"input_documents": docs, "question": question},
                          return_only_outputs=True)

    print(output)
    st.write("Reply: ", output["output_text"])


def main():
    # Set page configuration with an icon and expanded layout
    st.set_page_config(page_title="Chat PDF", layout="wide")

    # Header with custom styling
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Chat with PDF using Gemini Pro</h1>",
                unsafe_allow_html=True)

    # User question input with a prompt and better alignment
    st.markdown("<p style='text-align: center; font-size: 18px;'>Ask a Question from the PDF Files</p>",
                unsafe_allow_html=True)
    user_question = st.text_input(
        "", key="user_question", label_visibility="collapsed")

    # Process user question
    if user_question:
        user_input(user_question)

    # Sidebar for file upload and processing
    with st.sidebar:
        st.title("Menu:")
        st.markdown(
            "<p style='font-size: 16px;'>Upload your PDF Files and Click on the Submit & Process Button</p>", unsafe_allow_html=True)
        pdf_docs = st.file_uploader(
            "", accept_multiple_files=True, label_visibility="collapsed")

        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = convert_chuncks(raw_text)
                convert_vector(text_chunks)
                st.success("Done")


if __name__ == "__main__":
    main()
