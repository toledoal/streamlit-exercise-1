# Path: pages/01_whisper video transcription.py

import streamlit as st
from moviepy.editor import *
import tempfile
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain import LLMChain, OpenAI
import openai

llm = OpenAI(temperature=0)


def summarize(transcription):
    text_splitter = CharacterTextSplitter(
        separator=". ",
        chunk_size=3000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(transcription)
    print(len(texts))
    print(texts[0])
    docs = [Document(page_content=t) for t in texts]
    print(len(docs))

    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
    return chain.run(docs)


def tasks(transcription):
    text_splitter = CharacterTextSplitter(
        separator=". ",
        chunk_size=3000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(transcription)
    docs = [Document(page_content=t) for t in texts[:2]]
    print(docs)

    prompt_template = """Extract the possible tasks of the CONTEXT, like in the following example:
    EXAMPLE:
    TASKS:
    1. Create an object (assign to Mariana)
    2. Assign the task to Pedro (assign to Pedro)
    3. Recreate the design and image (assign to Josh)
    4. Call the client (not yet assigned)
    CONTEXT:
    {text}
    TASKS:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])

    # list comprehension to create a list of load_summarize_chain objects
    # chain = load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT, verbose=True)

    # list comprehension to run each document through its corresponding chain

    tasks = [
        load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT, verbose=True).run(
            [doc]
        )
        for doc in docs
    ]

    prompt_template = "Create a single list and remove duplicated information: {text}?"

    llm_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))

    text = " ".join(tasks)

    result = llm_chain(text)
    return result["text"]


def save_audio_to_tmp(file):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a temporary file path
        temp_file_path = os.path.join(temp_dir, file.name)

        with open(temp_file_path, "wb") as f:
            f.write(file.read())

        # temp_output_file_path = os.path.join(temp_dir, "extracted_audio.mp3")
        # # Save the file into the temporary folder
        transcript = ""
        with open(temp_file_path, "rb") as f:
            transcript = openai.Audio.transcribe(
                file=f,
                model="whisper-1",
                response_format="text",
            )
        return transcript


# extract_audio_from_video(temp_file_path, temp_output_file_path)


def save_video_to_tmp(file):
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


audioFile = st.file_uploader("Upload a file", type=["mp4", "mp3"])

if audioFile is not None:
    with st.spinner("Whisper is processing your file..."):
        st.write(audioFile.type)
        if audioFile.type == "audio/mpeg":
            with st.expander("Audio"):
                st.audio(audioFile)
                transcription = save_audio_to_tmp(audioFile)
        else:
            audioFile.type == "video/mp4"
            with st.expander("Video"):
                st.video(audioFile)
                transcription = save_video_to_tmp(audioFile)

        st.session_state["audioFile"] = audioFile

        with st.expander("Transcription"):
            st.write(transcription)

        st.session_state["audioTranscription"] = transcription

        summary = summarize(transcription)

        st.write("## Summary")
        st.markdown(summary)

        tasks = tasks(transcription)
        st.write("## Tasks")
        st.write(tasks)

        st.success(f"Transcription complete!")
