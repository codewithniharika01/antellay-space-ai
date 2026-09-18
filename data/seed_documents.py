import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.database.database import SessionLocal
from app.models.document import Document


db = SessionLocal()

document = Document(
    document_id="doc_001",
    title="International Space Station",
    source="NASA",
    date="2026",
    content=(
        "The International Space Station (ISS) is a modular space station "
        "in low Earth orbit. It serves as a microgravity and space environment "
        "research laboratory where scientific research and technology "
        "demonstrations are conducted."
    ),
    category="Space Missions"
)

db.add(document)
db.commit()
db.close()

print("Document added successfully!")