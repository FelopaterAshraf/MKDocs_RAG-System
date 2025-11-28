
# 📘 MkDocs RAG Assistant

This is a Retrieval-Augmented Generation (RAG) system designed to answer questions about MkDocs documentation.
It uses Google's Gemini models for text generation and embedding, along with ChromaDB as the vector store.

---

## ✨ Features

* **Hybrid Chunking**
  Uses Markdown headers + recursive character splitting to preserve documentation structure.

* **Data Cleaning**
  Removes HTML artifacts, code fences, markdown noise, and tiny micro-chunks under 100 characters.

* **Multimodal Support**
  Retrieves and displays images found in the documentation.

* **Interactive UI (Streamlit)**
  A clean chat interface for asking MkDocs-related questions.

* **Guardrails**
  LLM answers only using retrieved context and avoids hallucinations.

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/FelopaterAshraf/MKDocs_RAG-System.git
cd MKDocs_RAG-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API Key

Create a `.env` file in the project directory:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

---

## ▶️ Usage

### 1. Initialize the Vector Database

Open and run the **`RAG__System.ipynb`** notebook.

This will:

* Download the MkDocs documentation
* Clean & chunk the text
* Generate embeddings using `text-embedding-004`
* Build the ChromaDB vector store

### 2. Run the Chat Application (Streamlit)

```bash
streamlit run rag_app.py
```

The assistant will start and load the previously created embedding database.

---

## 📁 Files Description

* **`RAG__System.ipynb`**
  Jupyter Notebook containing the full pipeline: extraction, cleaning, chunking, embedding, visualization, and DB creation.

* **`rag_app.py`**
  Streamlit chat interface + RAG inference logic.

* **`requirements.txt`**
  List of required Python libraries.

* **`mkdocs_db/`**
  Persistent ChromaDB storage (created after running the notebook).


---

