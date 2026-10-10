from datetime import date

from sqlalchemy import select

from app import app
from data_models import db, Author, Book


# This code is AI generated to populate the vanilla-db
def seed_data() -> None:
    """Insert default authors and books if they do not already exist."""
    seed_authors = [
        ("George Orwell", date(1903, 6, 25), date(1950, 1, 21)),
        ("Jane Austen", date(1775, 12, 16), date(1817, 7, 18)),
        ("Mary Shelley", date(1797, 8, 30), date(1851, 2, 1)),
        ("F. Scott Fitzgerald", date(1896, 9, 24), date(1940, 12, 21)),
        ("Harper Lee", date(1926, 4, 28), date(2016, 2, 19)),
        ("J. R. R. Tolkien", date(1892, 1, 3), date(1973, 9, 2)),
        ("Ray Bradbury", date(1920, 8, 22), date(2012, 6, 5)),
        ("Agatha Christie", date(1890, 9, 15), date(1976, 1, 12)),
        ("Bram Stoker", date(1847, 11, 8), date(1912, 4, 20)),
        ("Franz Kafka", date(1883, 7, 3), date(1924, 6, 3)),
    ]

    authors_by_name = {}

    for name, birthdate, date_of_death in seed_authors:
        existing_author = db.session.scalar(
            select(Author).where(Author.name == name)
        )

        if existing_author is None:
            existing_author = Author(
                name=name,
                birthdate=birthdate,
                date_of_death=date_of_death,
            )
            db.session.add(existing_author)

        authors_by_name[name] = existing_author

    db.session.flush()

    seed_books = [
        ("9780451524935", "1984", 1949, "George Orwell"),
        ("9780141439518", "Pride and Prejudice", 1813, "Jane Austen"),
        ("9780486282114", "Frankenstein", 1818, "Mary Shelley"),
        ("9780743273565", "The Great Gatsby", 1925, "F. Scott Fitzgerald"),
        ("9780061120084", "To Kill a Mockingbird", 1960, "Harper Lee"),
        ("9780547928227", "The Hobbit", 1937, "J. R. R. Tolkien"),
        ("9781451673319", "Fahrenheit 451", 1953, "Ray Bradbury"),
        ("9780062693662", "Murder on the Orient Express", 1934, "Agatha Christie"),
        ("9780486411095", "Dracula", 1897, "Bram Stoker"),
        ("9780805209990", "The Trial", 1925, "Franz Kafka"),
    ]

    for isbn, title, publication_year, author_name in seed_books:
        existing_book = db.session.scalar(
            select(Book).where(Book.isbn == isbn)
        )

        if existing_book is None:
            new_book = Book(
                isbn=isbn,
                title=title,
                publication_year=publication_year,
                author_id=authors_by_name[author_name].id,
            )
            db.session.add(new_book)

    db.session.commit()
    print("Seed data inserted successfully.")


if __name__ == "__main__":
    with app.app_context():
        seed_data()