
import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

import streamlit as st
import chromadb


st.set_page_config(page_title="MkDocs Assistant", page_icon="image1.png", layout="wide")

load_dotenv()

# --- NEW: Bridge Streamlit Secrets → Environment variable ---
if "GOOGLE_API_KEY" not in os.environ:
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Validate key
if "GOOGLE_API_KEY" not in os.environ or not os.environ["GOOGLE_API_KEY"]:
    st.error("Please set GOOGLE_API_KEY in your .env file or Streamlit Secrets")
    st.stop()
    
# Connect to the DB created 
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
chroma_client = chromadb.PersistentClient(path="mkdocs_db")
collection = chroma_client.get_collection("MkDocs_Guides")


def query_mkdocs(question):
    response = client.models.embed_content( model="text-embedding-004", contents=question )
    query_embedding = response.embeddings[0].values

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5  # k=5 , 5 text chunks that are mathematically closest to this question
    )

    context_docs = results["documents"][0]
    sources = set([m["source"] for m in results["metadatas"][0]])
    context_text = "\n\n---\n\n".join(context_docs)

    
    print("\n" + "="*70)
    print(f"QUESTION: {question}")
    print(f"RETRIEVED CONTEXT:\n{context_text}")
    print("="*70 + "\n")

   
    system_instruction = """You are a specialized Technical Support Assistant for MkDocs.
    STRICT RULES:
    1. Answer using ONLY the provided context.
    2. If the answer is NOT in the context, say: "I cannot find information about this in the MkDocs documentation."
    3. Keep answers technical and concise."""

    user_message = f"""Context:
    {context_text}

    Question: {question}"""

    response = client.models.generate_content(model="gemini-2.0-flash",contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.3
        )
    )

    return response.text, sources

#  UI
col1, col2 = st.columns([1, 5]) 

with col1:
    st.image("image1.png", width=80)

with col2:
    st.title("MkDocs RAG Chat")


if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if "images" in message:
            for img_path in message["images"]:
                st.image(img_path, caption="Retrieved from Documentation")

# React to user input
if prompt := st.chat_input("Ask about MkDocs..."):

    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

  # Display assistant response
    with st.chat_message("assistant"):
        response_text, sources = query_mkdocs(prompt)
        st.markdown(response_text)

        found_images = []
        
        # --- THE FIX: Only show images if the answer is found ---
        if "I cannot find information" not in response_text:
            for source in sources:
                if source.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    st.image(source, caption="Retrieved from Documentation")
                    found_images.append(source)
        
        st.session_state.messages.append({"role": "assistant", "content": response_text,"images": found_images})