import os
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl, computed_field

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


class URLCreate(BaseModel):
    original_url: HttpUrl         

class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    click_count: int
    created_at: datetime

    @computed_field
    @property
    def short_url(self) -> str:
        return f"{BASE_URL}/{self.short_code}"

    class Config:
        from_attributes = True