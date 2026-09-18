import sys
from pathlib import Path
import time
import json

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.database.database import SessionLocal
from rag.retrieval import retrieve_documents
from app.services.llm import generate_answer


evaluation_questions = [
    "What is the International Space Station?",
    "What type of orbit is commonly used for Earth observation?",
    "What is the purpose of Earth observation satellites?",
    "How does a geostationary orbit work?",
    "What conditions are included in the space environment?",
    "Why do spacecraft need attitude control?",
    "What is a satellite payload?",
    "How can satellite observations support disaster response?",
    "Why is radiation monitoring important for spacecraft?",
    "Why do different spacecraft use different instruments?"
]


def evaluate():
    db = SessionLocal()
    results = []

    try:
        for number, question in enumerate(evaluation_questions, start=1):

            start_time = time.perf_counter()

            documents = retrieve_documents(question, db)

            context = "\n\n".join(
                document.content
                for document in documents
            )

            if context:
                answer = generate_answer(
                    question=question,
                    context=context
                )
            else:
                answer = "No relevant information found."

            latency = time.perf_counter() - start_time

            result = {
                "question_number": number,
                "question": question,
                "answer": answer,
                "sources_retrieved": len(documents),
                "latency_seconds": round(latency, 2)
            }

            results.append(result)

            print(f"\nQuestion {number}: {question}")
            print(f"Answer: {answer}")
            print(f"Sources retrieved: {len(documents)}")
            print(f"Latency: {latency:.2f} seconds")

        output_path = (
            Path(__file__).resolve().parent.parent
            / "evaluation_results.json"
        )

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=2, ensure_ascii=False)

        print("\nEvaluation results saved to evaluation_results.json")

    finally:
        db.close()


if __name__ == "__main__":
    evaluate()