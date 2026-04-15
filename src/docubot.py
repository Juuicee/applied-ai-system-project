"""
Core DocuBot class responsible for:
- Loading documents from the docs/ folder
- Building a simple retrieval index (Phase 1)
- Retrieving relevant snippets (Phase 1)
- Supporting retrieval only answers
- Supporting RAG answers when paired with Gemini (Phase 2)
"""

from src.llm_client import GeminiClient

import os
import glob

import logging

class DocuBot:
    def __init__(self, docs_folder="docs", llm_client=None):
        """
        docs_folder: directory containing project documentation files
        llm_client: optional Gemini client for LLM based answers
        """
        self.docs_folder = docs_folder
        self.llm_client = llm_client

        # Load documents into memory
        self.documents = self.load_documents()  # List of (filename, text)

        # Build a retrieval index (implemented in Phase 1)
        self.index = self.build_index(self.documents)

    # -----------------------------------------------------------
    # Document Loading
    # -----------------------------------------------------------

    def load_documents(self):
        """
        Loads all .md and .txt files inside docs_folder.
        Returns a list of tuples: (filename, text)
        """
        docs = []
        pattern = os.path.join(self.docs_folder, "*.*")
        for path in glob.glob(pattern):
            if path.endswith(".md") or path.endswith(".txt"):
                with open(path, "r", encoding="utf8") as f:
                    text = f.read()
                filename = os.path.basename(path)
                docs.append((filename, text))
        return docs

    # -----------------------------------------------------------
    # Index Construction (Phase 1)
    # -----------------------------------------------------------

    def build_index(self, documents):
        """
        TODO (Phase 1):
        Build a tiny inverted index mapping lowercase words to the documents
        they appear in.

        Example structure:
        {
            "token": ["AUTH.md", "API_REFERENCE.md"],
            "database": ["DATABASE.md"]
        }

        Keep this simple: split on whitespace, lowercase tokens,
        ignore punctuation if needed.
        """
        index = {}
        # TODO: implement simple indexing
        for filename, text in documents:
            words = text.lower().split()

            for word in words:
                # optional: strip simple punctuation
                word = word.strip(".,!?()[]{}:\"'")

                if word not in index:
                    index[word] = []

                if filename not in index[word]:
                    index[word].append(filename)

        return index

    # -----------------------------------------------------------
    # Scoring and Retrieval (Phase 1)
    # -----------------------------------------------------------

    def score_document(self, query, text):
        """
        TODO (Phase 1):
        Return a simple relevance score for how well the text matches the query.

        Suggested baseline:
        - Convert query into lowercase words
        - Count how many appear in the text
        - Return the count as the score
        """
        # TODO: implement scoring
        query_words = query.lower().split()
        text_words = text.lower()

        score = 0
        for word in query_words:
            if word in text_words:
                score += 1

        return score

    def retrieve(self, query, top_k=3):
        """
        TODO (Phase 1):
        Use the index and scoring function to select top_k relevant document snippets.

        Return a list of (filename, text) sorted by score descending.
        """

        # Added logging and guardrail for low confidence retrieval
        logging.basicConfig(level=logging.INFO)

        # Example usage:
        logging.info(f"Retrieving for query: {query}")
        logging.info(f"Top results: {scored_chunks[:3]}")

        results = []
        # TODO: implement retrieval logic
        query_words = query.lower().split()
        scored_chunks = []

        # Split documents into smaller chunks (paragraphs)
        for filename, text in self.documents:
            paragraphs = text.split("\n\n")

            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue

                # Score each paragraph
                score = self.score_document(query, para)

                if score > 0:
                    scored_chunks.append((filename, para, score))

        # Sort by score (highest first)
        scored_chunks.sort(key=lambda x: x[2], reverse=True)

        # Guardrail — refuse if no strong evidence
        if not scored_chunks:
            return []

        if scored_chunks[0][2] < 2:
            logging.warning("Low confidence retrieval — refusing to answer.")
            return []
        
        if not scored_chunks or scored_chunks[0][2] < 2:
            return []

        # Return top_k results (filename, text)
        return [(filename, text) for filename, text, _ in scored_chunks[:top_k]]

    # -----------------------------------------------------------
    # Answering Modes
    # -----------------------------------------------------------

    def answer_retrieval_only(self, query, top_k=3):
        """
        Phase 1 retrieval only mode.
        Returns raw snippets and filenames with no LLM involved.
        """
        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        formatted = []
        for filename, text in snippets:
            formatted.append(f"[{filename}]\n{text}\n")

        return "\n---\n".join(formatted)

    def answer_rag(self, query, top_k=3):
        """
        Phase 2 RAG mode.
        Uses student retrieval to select snippets, then asks Gemini
        to generate an answer using only those snippets.
        """
        if self.llm_client is None:
            raise RuntimeError(
                "RAG mode requires an LLM client. Provide a GeminiClient instance."
            )

        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        return self.llm_client.answer_from_snippets(query, snippets)

    # -----------------------------------------------------------
    # Bonus Helper: concatenated docs for naive generation mode
    # -----------------------------------------------------------

    def full_corpus_text(self):
        """
        Returns all documents concatenated into a single string.
        This is used in Phase 0 for naive 'generation only' baselines.
        """
        return "\n\n".join(text for _, text in self.documents)
