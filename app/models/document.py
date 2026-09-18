from sqlalchemy import Column, Integer, String, Text
from app.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    title = Column(String, nullable=False)
    source = Column(String, nullable=False)
    source_url = Column(String, nullable=True)
    date = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=False)