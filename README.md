A REST API built with FastAPI and PostgreSQL that shortens long URLs into 6-character codes, redirects to the original, and tracks click counts.

## Tech Stack

- Python 3.13
- FastAPI, Uvicorn
- PostgreSQL, SQLAlchemy
- Pydantic (validation)
- python-dotenv (configuration)

## Features

- Shorten any valid URL into a 6-character code (invalid URLs are rejected)
- Redirect to the original URL using the short code
- Track click count per URL
- View all shortened URLs with stats
- Update or delete existing URLs
- Full short_url returned in every response

## Project Structure


url-shortener/
├── database.py       # DB connection, session, get_db dependency
├── models.py         # SQLAlchemy table model
├── schemas.py        # Pydantic request/response schemas
├── main.py           # FastAPI app and endpoints
├── requirements.txt
├── .env.example
└── README.md


## Setup

*1. Clone the repository*
bash
git clone https://github.com/YOUR_USERNAME/url-shortener.git
cd url-shortener


*2. Create and activate a virtual environment*
bash
python -m venv venv
venv\Scripts\activate


*3. Install dependencies*
bash
pip install -r requirements.txt


*4. Create the PostgreSQL database*
sql
CREATE DATABASE url_shortener;


*5. Configure environment variables*

Copy .env.example to .env and put in your PostgreSQL password:

DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost:5432/url_shortener
BASE_URL=http://127.0.0.1:8000


*6. Run the app*
bash
uvicorn main:app --reload


*7. Open the API docs*

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /shorten | Create a short URL |
| GET | /urls | List all URLs with stats |
| GET | /stats/{short_code} | Stats for one short URL |
| PUT | /urls/{url_id} | Update the original URL |
| DELETE | /urls/{url_id} | Delete a URL |
| GET | /{short_code} | Redirect to the original URL |

## Example

*Request*
json
POST /shorten
{ "original_url": "https://www.google.com/search?q=fastapi" }


*Response*
json
{
  "id": 1,
  "original_url": "https://www.google.com/search?q=fastapi",
  "short_code": "aB3xYz",
  "click_count": 0,
  "created_at": "2026-10-03T18:00:00",
  "short_url": "http://127.0.0.1:8000/aB3xYz"
}


Opening http://127.0.0.1:8000/aB3xYz redirects to the original URL and increases click_count by 1.

## Author

Hemnath