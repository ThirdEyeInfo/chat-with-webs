import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from dotenv import load_dotenv

load_dotenv()

def load_document_from_url(url):
    loader = WebBaseLoader(url)
    document = loader.load()
    return document

def get_documents_chunks(document):
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(documents=document)
    return document_chunks

def get_embeddings():
    return OpenAIEmbeddings()

def get_vectorestore_for_saved_chunks(document_chunks):
    # vector_stores = Chroma.from_documents(document_chunks, get_embeddings(), persist_directory="db")
    # vector_stores.persist()
    vector_stores = Chroma.from_documents(document_chunks, get_embeddings())
    return vector_stores

# Conversation chain
def get_context_retriever_chain(retriever):
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to this conversation")
    ])

    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    return retriever_chain

def get_conversational_rag_chain(retriever_chain):
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

    stuff_documents_chains = create_stuff_documents_chain(llm, prompt)

    return create_retrieval_chain(retriever_chain, stuff_documents_chains)

def get_response(user_query):
    retriever_chain = get_context_retriever_chain(st.session_state.retriever)
    conversational_rag_chain = get_conversational_rag_chain(retriever_chain)
    
    response = conversational_rag_chain.invoke({
            "chat_history":st.session_state.chat_history,
            "input": user_query
        })
    return response["answer"]

st.set_page_config(page_title="Chat with websites", page_icon=":robot:")

with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")

st.title("Chat with websites")

if website_url is None or website_url == "":
    st.info("Please enter a website URL")
else:

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am a bot. How can I help you?")
        ]
    if 'retriever' not in st.session_state:
        document = load_document_from_url(website_url)
        document_chunks = get_documents_chunks(document)
        st.session_state.retriever = get_vectorestore_for_saved_chunks(document_chunks).as_retriever()

    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)