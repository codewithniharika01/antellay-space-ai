import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.database.database import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from rag.processing import clean_text, chunk_text


def ingest_documents():
    json_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "documents.json"
    )

    with open(json_path, "r", encoding="utf-8") as file:
        documents = json.load(file)

    db = SessionLocal()

    try:
        for item in documents:
            existing_document = (
                db.query(Document)
                .filter(Document.document_id == item["document_id"])
                .first()
            )

            if existing_document:
                document = existing_document
            else:
                cleaned_content = clean_text(item["content"])

                document = Document(
                    document_id=item["document_id"],
                    title=item["title"],
                    source=item["source"],
                    source_url=item.get("source_url"),
                    date=item.get("date"),
                    content=cleaned_content,
                    category=item["category"],
                )

                db.add(document)
                db.flush()

            existing_chunks = (
                db.query(DocumentChunk)
                .filter(
                    DocumentChunk.document_id
                    == item["document_id"]
                )
                .count()
            )

            if existing_chunks > 0:
                continue

            cleaned_content = clean_text(item["content"])
            chunks = chunk_text(
                cleaned_content,
                chunk_size=80
            )

            for index, chunk in enumerate(chunks):
                document_chunk = DocumentChunk(
                    document_id=item["document_id"],
                    chunk_index=index,
                    content=chunk,
                )

                db.add(document_chunk)

        db.commit()

        total_chunks = db.query(DocumentChunk).count()

        print(
            f"Successfully processed {len(documents)} documents."
        )
        print(
            f"Total chunks in knowledge base: {total_chunks}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    ingest_documents()