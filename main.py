
import streamlit as st

from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate


def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(
        temperature=0.5, openai_api_key=openai_api_key, model_name="text-davinci-003"
    )
    return llm


def getFile():
    if file is not None:
        return file.getvalue().decode('utf-8').splitlines() 
    

def processText():
    if file is not None:
        text_splitter = CharacterTextSplitter()
        with open(file.name) as f:
            moby_dick = f.read()
            texts = text_splitter.split_text(moby_dick)
        return texts
    else:
        return ""


def run():
    docs = [Document(page_content=t) for t in processText()[:3]]
    chain = load_summarize_chain(load_LLM(st.secrets["OPENAI_KEY"]), chain_type="map_reduce", verbose=True)
    return chain.run(docs)

st.title("Main")

st.write("## Summarize this book")


file = st.file_uploader("Upload a file", type="txt")
st.session_state["file"] = file

numberOfDocuments = 0
fileName = ""
if st.button("Process book into documents", disabled=(file is None)):
    st.write("Number of small document chunks:")
    numberOfDocuments = st.write(len(processText()))
    fileName = st.write(file.name)

resultOfSummarization = ""
if st.button("Run", disabled=(file is None or numberOfDocuments == 0)):
    if file is not None:
        resultOfSummarization = run()  

        

message = f"Summarize: {file.name}" if file is not None else "No file selected"
st.write(message)
st.write(resultOfSummarization)






