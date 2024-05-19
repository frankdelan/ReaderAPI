from typing import Optional

from api.books.models import Progress, Book


def convert_data(data) -> Optional[Book]:
    """Convert raw data to model"""
    if data:
        return Book(id=data.id,
                title=data.title,
                author=data.author,
                volume=data.volume,
                status=data.status,
                progress=Progress(current_pages=data.current_pages, start_reading_date=data.start_reading_date))

