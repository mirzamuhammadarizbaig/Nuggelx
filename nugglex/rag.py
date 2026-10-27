import os, re, requests
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PDF_PATH = os.path.join(os.path.dirname(__file__), "data", "nugglex_menu.pdf")
OLLAMA_URL = "https://ollama.com/api/chat"


def load_chunks(path, size=600, overlap=100):
    """Step 1: read the PDF and split it into overlapping chunks."""
    text = "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
    text = re.sub(r"[ \t]+", " ", text)
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size].strip())
        start += size - overlap
    return [c for c in chunks if c]


class NuggleXRAG:
    def __init__(self):
        self.chunks = load_chunks(PDF_PATH)
        # Step 2: index chunks (TF-IDF vectors)
        self.vec = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.matrix = self.vec.fit_transform(self.chunks)

    def retrieve(self, question, k=4):
        """Step 3: find the chunks most similar to the question."""
        scores = cosine_similarity(self.vec.transform([question]), self.matrix)[0]
        top = scores.argsort()[::-1][:k]
        return [self.chunks[i] for i in top if scores[i] > 0]

    def answer(self, question, history=None):
        """Step 4: give the retrieved context + question to the LLM."""
        context = "\n---\n".join(self.retrieve(question)) or "No relevant info found."
        system = (
            "You are NuggleBot, the friendly assistant of NUGGLEX Restaurant. "
            "Answer ONLY using the context below. If the answer is not in the context, "
            "say you don't have that info and suggest contacting the restaurant. "
            "Keep answers short and friendly. Use plain text only: no tables, no headers; a short list with '- ' is fine. \n\nCONTEXT:\n" + context
        )
        messages = [{"role": "system", "content": system}]
        messages += (history or [])[-6:]
        messages.append({"role": "user", "content": question})

        r = requests.post(
            OLLAMA_URL,
            headers={"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]},
            json={"model": os.getenv("OLLAMA_MODEL", "gpt-oss:120b"),
                  "messages": messages, "stream": False},
            timeout=90,
        )
        r.raise_for_status()
        return r.json()["message"]["content"]
