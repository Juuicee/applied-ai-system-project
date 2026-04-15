## Reliability and Evaluation

How reliability is measured:

Hit Rate = correct retrievals / total queries

The system includes basic logging points that allow debugging of:

- Which documents were retrieved
- How chunks were scored
- When no relevant documents were found

# DocuBot – AI Documentation Assistant (RAG System)

## 1. Original Project (Modules 1–3)

This project is an extension of my earlier AI system built in Modules 1–3. The original version focused on building a simple documentation assistant that could load text files and return relevant information using keyword-based retrieval.

The goal of the original system was to explore basic information retrieval techniques and understand how structured text search can improve AI-assisted question answering. It did not include any large language model integration or evaluation framework at the beginning.

---

## 2. Title and Summary

### Title:
**DocuBot – Retrieval-Augmented Documentation Assistant**

### Summary:
DocuBot is an AI-powered assistant that helps developers answer questions about a codebase by combining document retrieval with large language model generation. It uses a Retrieval-Augmented Generation (RAG) pipeline to ensure answers are grounded in actual documentation.

This project matters because it demonstrates how modern AI systems combine search and generation to produce accurate and explainable responses.

---

## 3. Architecture Overview

DocuBot is built using three main components:

- **Retrieval System:**  
  Loads documentation files, tokenizes text, builds a simple inverted index, and retrieves relevant text chunks based on query similarity.

- **LLM Layer:**  
  Uses Google Gemini to generate natural language responses. It is used in both naive mode and RAG mode.

- **Evaluation System:**  
  Measures retrieval performance using predefined sample queries and expected document matches.