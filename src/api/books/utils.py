from api.books.schemas import BookSchema, ProgressSchema


def convert_data(data):
    progress = ProgressSchema(current_pages=data.current_pages, start_reading_date=data.start_reading_date)
    return BookSchema(id=data.id, title=data.title, author=data.author, volume=data.volume, status=data.status,
                      progress=progress)

