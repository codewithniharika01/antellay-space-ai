from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk


def retrieve_documents(
    query: str,
    db: Session,
    limit: int = 3
):
    keywords = query.lower().split()

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

        searchable_text = (
            f"{document.title} "
            f"{document.category} "
            f"{chunk.content}"
        ).lower()

        score = sum(
            1
            for keyword in keywords
            if keyword in searchable_text
        )

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