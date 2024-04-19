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
import base64
import os
from datetime import datetime



# Database connection (skeleton code)
# def connect_to_database():
#     conn = psycopg2.connect(
#         host="your_host",
#         database="your_database",
#         user="your_username",
#         password="your_password"
#     )
#     return conn


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




def save_image(image, keyword):
    # Create a directory to store the images if it doesn't exist
    os.makedirs("saved_images", exist_ok=True)
    
    # Generate a unique filename for the image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{keyword}_{timestamp}.png"
    filepath = os.path.join("saved_images", filename)
    
    # Save the image to the specified filepath
    image.save(filepath)
    
    return filename


# def get_conversation_chain(vectorstore):
#     llm = ChatOpenAI()
#     # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

#     memory = ConversationBufferMemory(
#         memory_key='chat_history', return_messages=True)
#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=vectorstore.as_retriever(),
#         memory=memory
#     )
#     return conversation_chain

def get_conversation_chain(vectorstore=None):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    
    if vectorstore is None:
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            memory=memory
        )
    else:
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
    
    return conversation_chain



def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    display_image = False
    # display_video = False


    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            if "![Image](" in message.content:
                image_url = message.content.split("(")[1].split(")")[0]
                st.image(image_url)
            
            else:
                st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            # if not display_image:
            #     st.write(bot_template.replace(
            #         "{{MSG}}", message.content), unsafe_allow_html=True)
    
            
    image_mappings = {
        "bmi": "img/bmi.png",
        "obesity risks": "img/risk_of_overweight.png",
        "healthy lifestyle": "img/healthy_lifestyle.png"
    }

    video_mappings = {
        "bmi": {"url": "https://www.youtube.com/watch?v=PpuiO6WJxic", "timestamp": "1m18s"},
        "obesity facts": {"url": "https://www.youtube.com/watch?v=d6gS5-02VYM", "timestamp": "23s"},
        "child obesity rate": {"url": "https://www.youtube.com/watch?v=ZpbZ33Dc53E", "timestamp": "5s"},
        "obesity effects on nervous system": {"url": "https://www.youtube.com/watch?v=Ss1yx9FwTWQ", "timestamp": "33s"},
        "obesity impact on nerve system": {"url": "https://www.youtube.com/watch?v=Ss1yx9FwTWQ", "timestamp": "33s"}
    }

    
    for keyword, image_path in image_mappings.items():
        if keyword.lower() in user_question.lower():
            # Open the image using PIL
            image = Image.open(image_path)

            # display_image(image, keyword)
    
            # Convert the image to PNG format
            png_image = BytesIO()
            image.save(png_image, format='PNG')
            png_image.seek(0)
            
            # Ensure the image size is less than 4 MB
            png_image_bytes = png_image.getvalue()
            if len(png_image_bytes) >= 4 * 1024 * 1024:  # 4 MB in bytes
                # Resize the image to fit within the size limit
                image.thumbnail((1024, 1024))  # Adjust the size as needed
                resized_png_image = BytesIO()
                image.save(resized_png_image, format='PNG')
                resized_png_image.seek(0)
                png_image_bytes = resized_png_image.getvalue()
                # st.session_state.chat_history.append(AIMessage(content=f"![Image](data:image/png;base64,{base64.b64encode(png_image_bytes).decode()})"))
            
            # Use the OpenAI API to create an image variation
            client = OpenAI()
            response = client.images.create_variation(
                image=png_image_bytes,
                n=1,
                model="dall-e-2",
                size="1024x1024"
            )
            
            # Get the URL of the generated image variation
            image_url = response.data[0].url
            
            # Display the generated image using Streamlit
            # st.image(image_url, caption=f"Image related to: {keyword}")
            st.image(image, caption=f"Image related to: {keyword}")

            if keyword in video_mappings:
                video_data = video_mappings[keyword]
                video_url = video_data["url"]
                timestamp = video_data["timestamp"]
                
                # # Create the video URL with the timestamp
                # video_link = f"{video_url}&t={timestamp}"
                # # Display the video link with the timestamp
                # st.markdown(f"Related video: [Link]({video_link})")

                
                # Display the video using Streamlit's `st.video`
                st.video(video_url, start_time=timestamp)
                    

            display_image = True
            break



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

