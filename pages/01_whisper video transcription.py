# Path: pages/01_whisper video transcription.py

import streamlit as st
from moviepy.editor import *
import tempfile
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI
import openai

llm = OpenAI(temperature=0)


def summarize(transcription):
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(transcription)
    docs = [Document(page_content=t) for t in texts[:3]]
    prompt_template = """Write a concise summary in markdown format of the following:
    {text}
    CONCISE SUMMARY:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT)
    return chain.run(docs)


def tasks(transcription):
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(transcription)
    docs = [Document(page_content=t) for t in texts[:3]]
    prompt_template = """Extract the possible tasks and people responsible, in a markdown format list, of the following:
    {text}
    TASKS:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT)
    return chain.run(docs)


def save_file_to_tmp(file):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a temporary file path
        temp_file_path = os.path.join(temp_dir, file.name)

        temp_output_file_path = os.path.join(temp_dir, "extracted_audio.mp3")
        # Save the file into the temporary folder
        with open(temp_file_path, "wb") as f:
            f.write(file.read())

        extract_audio_from_video(temp_file_path, temp_output_file_path)

        transcript = "not ready"
        with open(temp_output_file_path, "rb") as f:
            transcript = openai.Audio.transcribe(
                file=f,
                model="whisper-1",
                response_format="text",
            )
            return transcript


def extract_audio_from_video(video_file, output_audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(output_audio_file)


def app():
    st.title("Pixelspace Experiments")
    st.write("This is the transcription audio page.")


st.title("WhisperAI Transcription service")


audioFile = st.file_uploader("Upload a file", type="mp4")
if audioFile is not None:
    with st.spinner("Whisper is processing your file..."):
        with st.expander("Video"):
            st.video(audioFile)

        st.session_state["audioFile"] = audioFile
        transcription = save_file_to_tmp(audioFile)

        with st.expander("Transcription"):
            st.write(transcription)

        st.session_state["audioTranscription"] = transcription

        summary = summarize(transcription)

        st.write("## Summary")
        st.markdown(summary)

        tasks = tasks(transcription)
        st.write("## Tasks")
        st.markdown(tasks)

        st.success(f"Transcription complete!")
