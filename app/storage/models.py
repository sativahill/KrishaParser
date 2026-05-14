from typing import Optional

from sqlmodel import SQLModel, Field


class Listing(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    krisha_id: int = Field(
        unique=True,
        index=True
    )

    title: str

    price: int

    rooms: Optional[int] = None

    address: Optional[str] = None

    area: Optional[str] = None

    floor: Optional[str] = None

    phone: Optional[str] = None

    description: Optional[str] = None

    url: str

    status: str = "NEW"

    created_at: Optional[str] = None

class SearchProfile(
    SQLModel,
    table=True
):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    name: str

    city_slug: str

    rooms: str

    price_to: int

    who: int = 1