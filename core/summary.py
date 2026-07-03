from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import os

from torch import chunk

def get_llm():
    return ChatMistralAI(model="mistral-small-latest", mistral_api_key=os.getenv("MISTRAL_API_KEY"), temperature=0.2)


def split_transcript(transcript:str)->list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200,
    )
    return text_splitter.split_text(transcript)

def summarize(transcript:str)->str:
    llm = get_llm()
    
    map_prompt = ChatPromptTemplate.from_messages(
        [
            ("system","summarize this portion of a meeting transcript concisely."),
            ("human","{text}"),
        ]
    )
    
    map_chain = map_prompt | llm | StrOutputParser()
    
    
    chunks =  split_transcript(transcript)
    
    chunk_summarize = [map_chain.invoke({"text": chunk}) for chunk in chunks]
    
    combined = "\n\n".join(chunk_summarize)
    
    combine_prompt = ChatPromptTemplate.from_messages(
        [
            ("system","you are an expert meeting summarizer. combine these partial summaries."
             "into one final professional meeting summary into bullets points."
             ),
            ("human","{text}"),
        ]
    )
    
    combine_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x: {"text": x}) | combine_prompt | llm | StrOutputParser()
    )
    
    return combine_chain.invoke(combined)

def generate_title(transcript:str)->str:
    llm = get_llm()
    
    title_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x: {"text": x}) | ChatPromptTemplate.from_messages(
            [
                ("system","you are an expert meeting summarizer. generate a title for this meeting transcript."
                 ),
                ("human","{text}"),
            ]
        ) | llm | StrOutputParser()
    )
    return title_chain.invoke(transcript[:2000])