"""
Embedding utilities.

The core RAG system currently uses keyword-based retrieval,
which is explicitly allowed by the assignment.

This module is reserved for optional embedding-based retrieval
as a future improvement.
"""


def create_embedding(text: str):
    """
    Placeholder for future embedding implementation.
    """
    raise NotImplementedError(
        "Embedding-based retrieval is optional and not enabled."
    )