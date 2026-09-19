** ANTELLAY Space Intelligence API



*A mini Space Intelligence API built using FastAPI, SQLite, SQLAlchemy, JWT authentication, Retrieval-Augmented Generation (RAG), and an open-source instruct LLM.



** Project Overview



*This project was developed as part of the ANTELLAY SPACE Backend + AI/LLM Engineering Intern assignment.



*The API provides:



\- Satellite CRUD operations

\- JWT-based authentication

\- Space knowledge base

\- Keyword-based RAG retrieval

\- LLM-powered question answering

\- Source attribution

\- Space-related Q\&A dataset

\- RAG evaluation and API tests



\## Tech Stack



\- Python

\- FastAPI

\- SQLAlchemy

\- SQLite

\- Pydantic

\- JWT

\- bcrypt

\- Hugging Face Inference API

\- Qwen2.5-1.5B-Instruct

\- pytest



** Project Structure



*text

antellay-space-ai/

│

├── app/

│   ├── auth/

│   ├── database/

│   ├── models/

│   ├── routes/

│   ├── schemas/

│   ├── services/

│   └── main.py

│

├── data/

│   └── documents.json

│

├── rag/

│   ├── ingestion.py

│   ├── processing.py

│   ├── retrieval.py

│   └── embeddings.py

│

├── tests/

│   ├── test\_api.py

│   ├── test\_rag.py

│   └── evaluate\_rag.py

│

├── qa\_dataset.jsonl

├── evaluation\_results.json

├── requirements.txt

├── .env.example

├── .gitignore

└── README.md

API Endpoints:-



Authentication:

POST /auth/register

POST /auth/login



Satellites:
POST   /satellites

GET    /satellites

GET    /satellites/{id}

PUT    /satellites/{id}

DELETE /satellites/{id}
Satellite creation, update and deletion are protected using JWT authentication.

AI / RAG:
POST /ask
The /ask endpoint retrieves relevant knowledge-base content and passes the retrieved context to the LLM.



The response includes:



Question

Answer

Source title

Source

Source URL

Category



Knowledge Base:


The project contains 10 curated public space-related documents covering:



Space Missions

Orbit

Earth Observation

Space Environment

Space Technology



The sources are based on publicly available NASA and NASA-affiliated information.



The current retrieval system uses keyword-based scoring. Title and category matches receive higher priority than general content matches.




RAG Pipeline:



Public Space Sources

&#x20;       ↓

Document Records

&#x20;       ↓

Text Cleaning

&#x20;       ↓

Chunking

&#x20;       ↓

SQLite Knowledge Base

&#x20;       ↓

Keyword Retrieval

&#x20;       ↓

Relevant Context

&#x20;       ↓

LLM

&#x20;       ↓

Answer + Sources


LLM: The project integrates an open-source instruct model through Hugging Face hosted inference: 

Qwen/Qwen2.5-1.5B-Instruct  



The application does not train the full LLM. Retrieved knowledge-base context is provided to the model to generate grounded answers.



Dataset:

The project contains 30+ space-related question-answer pairs covering:



Satellite

Orbit

Earth Observation

Space Missions

Space Environment

Space Technology



Testing:

Automated tests cover:



Satellite API behavior

Missing satellite handling

RAG retrieval



The RAG evaluation also includes novel test questions and records response latency and retrieved sources.


Hallucination Handling:

The LLM prompt instructs the model to answer using only the retrieved context.



If relevant context is unavailable, the API returns:

No relevant information found in the knowledge base.

The API also returns source information with generated answers to improve traceability.





Deployment:--



Live API:



https://antellay-space-ai.onrender.com



Swagger documentation:



https://antellay-space-ai.onrender.com/docs



GitHub:



https://github.com/codewithniharika01/antellay-space-ai



Deployment Note:

The application uses hosted Hugging Face inference so that the Render deployment does not require large local ML model dependencies.



The external inference service may become temporarily unavailable because of provider limits or quota restrictions. The API handles this gracefully and still returns retrieved knowledge-base sources instead of returning an internal server error.



Security:

Secrets such as:



SECRET\_KEY

HF\_TOKEN



are stored in environment variables and are not committed to GitHub.



Future Improvements:-

Possible future improvements include:



\-Embedding-based semantic retrieval

\-Vector database integration

\-Improved evaluation metrics

\-Better document extraction and chunking

\-More knowledge-base sources

\-LLM provider fallback

\-Monitoring and observability

\-Satellite intelligence endpoint using NORAD data



Author:

Niharika Bharti














