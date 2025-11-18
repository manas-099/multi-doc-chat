🗂️ MultiDocChat – Multi-Document RAG Chatbot

(Work in Progress)


It allows users to upload multiple documents, index them, and chat with the model using information grounded in the uploaded files.

⚠️ Note: This project is currently in active development and not fully completed yet.

# 🧠 How It Works

## 1. Document Upload
- Users can upload **PDF**, **TXT**, or **DOCX** files.
- Uploaded files are saved under: data/<session_id>/
- Each uploaded document undergoes the following steps:
- **Chunking:** The document is split into smaller text chunks.
- **Embedding:** Each chunk is converted into vector embeddings.
- **Indexing:** Embeddings are stored inside a **FAISS index**.

- The FAISS index for each session is stored at: faiss_index/<session_id>/


---

## 2. Retrieval-Augmented Chat (RAG)
When a user sends a query:

1. The server loads the **FAISS index** for that session.
2. Relevant chunks are retrieved using vector similarity search.
3. Retrieved context + user query is sent to the LLM.
4. The model generates an answer grounded in the uploaded documents.

---

## 3. Session Management
- Each session is assigned a unique **session_id**.


---


