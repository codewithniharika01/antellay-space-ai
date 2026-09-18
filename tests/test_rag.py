import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.database.database import SessionLocal
from rag.retrieval import retrieve_documents


def test_retrieval_returns_results():
    db = SessionLocal()

    try:
        results = retrieve_documents("space station", db)

        assert len(results) > 0

        assert any(
            "International Space Station" in result["document"].title
            for result in results
        )

        assert any(
            result["chunk"].content
            for result in results
        )

    finally:
        db.close()