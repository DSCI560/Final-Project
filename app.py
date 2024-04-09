import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from langchain import HuggingFacePipeline
import pandas as pd
import psycopg2
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from io import BytesIO
from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from PIL import Image




# Database connection (skeleton code)
def connect_to_database():
    conn = psycopg2.connect(
        host="your_host",
        database="your_database",
        user="your_username",
        password="your_password"
    )
    return conn


def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    return text


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceEmbeddings(
    #     model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain




def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            
    image_mappings = {
        "bmi": "img/bmi.jpeg",
        "obesity risks": "img/risk_of_overweight.jpeg",
        "healthy lifestyle": "img/healthy_lifestyle.jpeg"
    }

    # video_mappings = {
    #     "exercise": {"path": "vid/exercise.mp4", "timestamp": "1:30"},
    #     "healthy diet": {"path": "vid/healthy_diet.mp4", "timestamp": "2:15"},
    #     "weight loss tips": {"path": "vid/weight_loss_tips.mp4", "timestamp": "0:45"}
    # }

    # Check if the user's question contains any of the specified keywords
    for keyword, image_path in image_mappings.items():
        if keyword.lower() in user_question.lower():
            # Read the image file and display it using Streamlit
            image = Image.open(image_path)
            st.image(image, caption=f"Image related to: {keyword}")
            break

    # # Check if the user's question contains any of the specified keywords for videos
    # for keyword, video_data in video_mappings.items():
    #     if keyword.lower() in user_question.lower():
    #         video_path = video_data["path"]
    #         timestamp = video_data["timestamp"]

    #         # Read the video file and display it using Streamlit
    #         video_file = open(video_path, 'rb')
    #         video_bytes = video_file.read()

    #         # Create the video URL with the timestamp
    #         video_url = f"data:video/mp4;base64,{base64.b64encode(video_bytes).decode()}"
    #         video_url += f"#t={timestamp}"

    #         # Display the video with the timestamp
    #         st.video(video_url)

    #         # Display the timestamp information
    #         st.write(f"Video timestamp: {timestamp}")
    #         break





def main():
    load_dotenv()
    st.set_page_config(page_title="Course TA HealthEdBot")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Hi this is HealthEdBot, TA of Obesity and Health Course")
    user_question = st.text_input("Ask away your questions about the course:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your Uploads")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)
                

        website_url = st.text_input("Enter a website URL to scrape:")
        if st.button("Scrape Website"):
            with st.spinner("Scraping website"):
                # scrape website
                scraped_text = scrape_website(website_url)

                # get the text chunks
                text_chunks = get_text_chunks(scraped_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()
