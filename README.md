🗂️ MultiDocChat – Multi-Document RAG Chatbot

(Work in Progress)


It allows users to upload multiple documents, index them, and chat with the model using information grounded in the uploaded files.

⚠️ Note: This project is currently in active development and not fully completed yet.

How it works
Upload PDFs, TXT, or DOCX files
Upload: Files are uploaded to data/<session_id>/, split, embedded, and saved as a FAISS index in faiss_index/<session_id>/.
Chat: Each request loads the FAISS index for the given session_id and answers using RAG.
Sessions: A simple in-memory history per session on the server (resets on restart). The browser stores session_id in localStorage.
