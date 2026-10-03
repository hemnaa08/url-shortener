from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import random
import string

import models
import schemas
from database import engine, Base, get_db

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Generate random short code
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


# POST - Create short URL
@app.post("/shorten", response_model=schemas.URLResponse)
def create_short_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()

    # Make sure short code is unique
    while db.query(models.URL).filter(models.URL.short_code == short_code).first():
        short_code = generate_short_code()

    # Build row object (str() converts HttpUrl to plain text)
    db_url = models.URL(
        original_url=str(url.original_url),
        short_code=short_code
    )

    db.add(db_url)       # Stage
    db.commit()          # Save
    db.refresh(db_url)   # Load new id
    return db_url        # Return item


# GET - Get all URLs
@app.get("/urls", response_model=list[schemas.URLResponse])
def get_all_urls(db: Session = Depends(get_db)):
    return db.query(models.URL).all()


# GET - Get stats for a specific short code
@app.get("/stats/{short_code}", response_model=schemas.URLResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(
        models.URL.short_code == short_code
    ).first()

    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    return db_url


# PUT - Update original URL
@app.put("/urls/{url_id}", response_model=schemas.URLResponse)
def update_url(url_id: int, url: schemas.URLCreate, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.id == url_id).first()

    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    db_url.original_url = str(url.original_url)   # Set new value
    db.commit()                                   # Save
    db.refresh(db_url)                            # Reload
    return db_url                                 # Return item


# DELETE - Delete a URL
@app.delete("/urls/{url_id}")
def delete_url(url_id: int, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.id == url_id).first()

    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    db.delete(db_url)    # Delete
    db.commit()          # Save
    return {"message": "URL deleted successfully"}


# GET - Redirect by short code (keep this LAST)
@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(
        models.URL.short_code == short_code
    ).first()

    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    # Increment click count
    db_url.click_count += 1
    db.commit()

    return RedirectResponse(url=db_url.original_url)