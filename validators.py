from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl, validator


class PropertyModel(BaseModel):
    id: str
    source: str
    url: Optional[str] = None
    title: str
    location: str
    price: Optional[float] = None
    surface: Optional[float] = None
    price_per_sqm: Optional[float] = None
    dpe: Optional[str] = 'N/A'
    dpe_value: Optional[int] = None
    images: List[str] = []
    contact_name: Optional[str] = ''
    contact_phone: Optional[str] = ''
    contact_email: Optional[str] = ''
    posted_date: Optional[datetime] = None

    @validator('url', pre=True, always=True)
    def empty_url_to_none(cls, v):
        if v in (None, '', 'N/A'):
            return None
        return v

    @validator('posted_date', pre=True, always=True)
    def parse_posted_date(cls, v):
        if v in (None, '', 'N/A'):
            return None
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except Exception:
                return None
        return v


def validate_property(prop: dict) -> dict:
    """Validate and return the normalized dict (pydantic-jsonable)."""
    model = PropertyModel(**prop)
    data = model.dict()
    # ensure images are strings
    data['images'] = [str(i) for i in data.get('images') or []]
    # posted_date to isoformat
    if data.get('posted_date'):
        data['posted_date'] = data['posted_date'].isoformat()
    return data
