### Reflection

**Core concept students needed to understand:** Using search to find relevant info first makes AI answers more accurate.

**Where students may struggle:** Designing an effective retrieval pipeline and deciding how to split, score, and rank text chunks can be confusing.

**Where AI was helpful vs misleading:** AI suggestions helped with coding ideas but sometimes gave confusing or wrong solutions so must be very wary of that!

**One way you’d guide a student without giving the answer:** Have them follow a question through the system to see where bad or irrelevant results come from and have them get their answer from there!

Overall, combining retrieval with AI gives much better answers than AI alone. Students must learn the importance of grounding answers in evidence, carefully structuring data, and thinking critically about the systems behavior. While AI can speed up coding and reasoning, understanding the underlying logic is key to building a reliable system!

## Comparing Retrieval, Generation, and RAG

Naive LLM = fluent but unreliable
Retrieval Only = reliable but not user-friendly
RAG = best balance of accuracy and usability

RAG is only as good as its retrieval. If retrieval fails, generation has nothing reliable to use.

# DocuBot

DocuBot is a small documentation assistant that helps answer developer questions about a codebase.  
It can operate in three different modes:

1. **Naive LLM mode**  
   Sends the entire documentation corpus to a Gemini model and asks it to answer the question.

2. **Retrieval only mode**  
   Uses a simple indexing and scoring system to retrieve relevant snippets without calling an LLM.

3. **RAG mode (Retrieval Augmented Generation)**  
   Retrieves relevant snippets, then asks Gemini to answer using only those snippets.

The docs folder contains realistic developer documents (API reference, authentication notes, database notes), but these files are **just text**. They support retrieval experiments and do not require students to set up any backend systems.

---

## Setup

### 1. Install Python dependencies

    pip install -r requirements.txt

### 2. Configure environment variables

Copy the example file:

    cp .env.example .env

Then edit `.env` to include your Gemini API key:

    GEMINI_API_KEY=your_api_key_here

If you do not set a Gemini key, you can still run retrieval only mode.

---

## Running DocuBot

Start the program:

    python main.py

Choose a mode:

- **1**: Naive LLM (Gemini reads the full docs)  
- **2**: Retrieval only (no LLM)  
- **3**: RAG (retrieval + Gemini)

You can use built in sample queries or type your own.

---

## Running Retrieval Evaluation (optional)

    python evaluation.py

This prints simple retrieval hit rates for sample queries.

---

## Modifying the Project

You will primarily work in:

- `docubot.py`  
  Implement or improve the retrieval index, scoring, and snippet selection.

- `llm_client.py`  
  Adjust the prompts and behavior of LLM responses.

- `dataset.py`  
  Add or change sample queries for testing.

---

## Requirements

- Python 3.9+
- A Gemini API key for LLM features (only needed for modes 1 and 3)
- No database, no server setup, no external services besides LLM calls
