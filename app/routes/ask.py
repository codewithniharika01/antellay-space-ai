from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from rag.retrieval import retrieve_documents
from app.services.llm import generate_answer

router = APIRouter(prefix="/ask", tags=["AI / RAG"])


@router.post("")
def ask_question(
    question: str,
    db: Session = Depends(get_db)
):
    results = retrieve_documents(question, db)

    context = "\n\n".join(
        result["chunk"].content
        for result in results
    )

    if context:
        answer = generate_answer(
            question=question,
            context=context
        )
    else:
        answer = "No relevant information found."

    sources = [
        {
            "title": result["document"].title,
            "source": result["document"].source,
            "source_url": result["document"].source_url,
            "category": result["document"].category
        }
        for result in results
    ]

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }