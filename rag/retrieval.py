import re

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk


STOPWORDS = {
    "what",
    "is",
    "are",
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "to",
    "for",
    "in",
    "on",
    "why",
    "how",
    "does",
    "do",
    "can",
    "this",
    "that",
    "with",
    "from",
    "about",
}


def tokenize(text: str) -> set[str]:
    words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

    normalized_words = set()

    for word in words:
        if word.endswith("s") and len(word) > 3:
            word = word[:-1]

        if word not in STOPWORDS and len(word) > 2:
            normalized_words.add(word)

    return normalized_words

def retrieve_documents(
    query: str,
    db: Session,
    limit: int = 3
):
    query_words = tokenize(query)

    if not query_words:
        return []

    chunks = db.query(DocumentChunk).all()

    scored_chunks = []

    for chunk in chunks:
        document = (
            db.query(Document)
            .filter(
                Document.document_id == chunk.document_id
            )
            .first()
        )

        if not document:
            continue

        title_words = tokenize(document.title)
        category_words = tokenize(document.category)
        content_words = tokenize(chunk.content)

        score = 0

        # Title matches are strongest
        score += len(query_words & title_words) * 5

        # Category matches are useful
        score += len(query_words & category_words) * 3

        # Content matches
        score += len(query_words & content_words)

        # Boost important exact topic matches
        if "radiation" in query_words:
           if "radiation" in title_words:
              score += 20
        if "radiation" in category_words:
              score += 10
        if "radiation" in content_words:
              score += 8

        if "payload" in query_words:
           if "payload" in title_words:
            score += 20
           if "payload" in content_words:
            score += 8
            
        if score > 0:
            scored_chunks.append(
                (score, document, chunk)
            )

    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        {
            "document": document,
            "chunk": chunk
        }
        for score, document, chunk in scored_chunks[:limit]
    ]