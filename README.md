# string-analyzer

A RESTful API service that analyzes strings and stores their computed properties with filtering and natural language query support.

## Project Description

The **String Analyzer API** is a FastAPI-based backend service that analyzes input strings, computes useful properties, and stores them in a database for advanced querying. It supports:

- String property analysis (length, palindrome, unique characters, SHA-256 hash, etc)
- Querying stored strings with filters
- Natural language filtering (e.g. "all single word palindromic strings")
- RESTful API design
- Clean **Separation of Concerns** architecture
- Fully tested endpoints

This project is designed to demonstrate clean backend architecture, API design best practices, testing practices, and structured documentation for **professional backend development**.

## Use Cases

This API can be used in:

- Text analysis platforms
- Search and indexing systems
- Backend developer assessments
- NLP data preprocessing

This repository follows **Separation of Concerns** and a clean folder structure.
We structured the project to follow:

- `routes/` for route definitions
- `services/` for business logic
- `models/` for database
- `schemas/` for pydantic models
- `utils/` for helper modules
- `db/` for database configuration
- `tests/` for test cases

## Project Structure

```bash
string-analyzer/
│
├── main.py
├── db/
│   └── database.py
├── models/
│   └── string_analyzer.py
├── routers/
│   ├── __init__.py
│   ├── string_analyzer.py
│   └── filters.py
├── schemas/
│   ├── __init__.py
│   └── string_analyzer.py
├── services/
│   ├── string_service.py
│   └── filter_service.py
├── utils/
│   └── compute.py
└── __init__.py
│
├── tests/
│   └── test_api.py
│
├── requirements.txt
├── .gitignore
├── README.md
├── Procfile
├── runtime.txt
└── .env.example
```

### README – Setup & Usage Instructions

### How to Run Locally

#### 1. Clone Repository

```bash
git clone https://github.com/triplee12/string-analyzer.git
cd string-analyzer
```

#### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate  # Windows
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Environment Variables

Create a `.env` file in the project root:

```bash
DATABASE_URL=sqlite:///./data.db
ENV=development
```

#### 5. Run Application

```bash
uvicorn app.main:app --reload
```

Go to Swagger UI: http://127.0.0.1:8000/docs

### Running Tests

```bash
pytest -v
```

### Dependencies

- FastAPI
- SQLModel
- SQLite
- Pydantic
- Uvicorn
- Pytest
- python-dotenv

Install automatically via `requirements.txt`.

### Deployment Instructions (Railway Approved)

1. Push project to GitHub
2. Go to https://railway.app
3. Select **Deploy from GitHub Repo**
4. Add build command:

```bash
pip install -r requirements.txt
```

5. Add start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT

Or

python -m main
```

6. Deploy

## API Documentation

### Base URL

```URL
http://localhost:8000
```

### 1. Create / Analyze String

**POST /strings**

```json
Request Body:
{
  "value": "string to analyze"
}
```

**201 Created**

```json
{
  "id": "sha256_hash_value",
  "value": "string to analyze",
  "properties": {
    "length": 16,
    "is_palindrome": false,
    "unique_characters": 12,
    "word_count": 3,
    "sha256_hash": "abc123...",
    "character_frequency_map": {
      "s": 2,
      "t": 3
    }
  },
  "created_at": "2025-08-27T10:00:00Z"
}
```

### 2. Get Specific String

**GET /strings/{string_value}**
  **200 OK** – Returns stored string information.

### 3. Get All Strings (with filtering)

**GET /strings**
Query parameters:

```bash
is_palindrome=true
min_length=5
max_length=20
word_count=2
contains_character=a
```

**200 OK** – Returns filtered list.

### 4. Natural Language Filtering

**GET /strings/filter-by-natural-language**

```bash
?query=all single word palindromic strings
```

**200 OK** – AI-powered filter parsing.

### 5. Delete String

**DELETE /strings/{string_value}**
**204 No Content** – Deletes string entry.
