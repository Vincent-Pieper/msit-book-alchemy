from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


db = SQLAlchemy()


class Author(db.Model):
    """Represent an author in the library."""

    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    birthdate: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_of_death: Mapped[date | None] = mapped_column(Date, nullable=True)

    books: Mapped[list["Book"]] = relationship(back_populates="author")

    def __str__(self) -> str:
        return (
            f"{self.name}, "
            f"born in {self.birthdate}, "
            f"deceased in {self.date_of_death}"
        )

    def __repr__(self) -> str:
        return (
            f"Author("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"birthdate={self.birthdate!r}, "
            f"date_of_death={self.date_of_death!r})"
        )


class Book(db.Model):
    """Represent a book in the library."""

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    author: Mapped["Author"] = relationship(back_populates="books")

    def __str__(self) -> str:
        return (
            f"{self.title}, "
            f"published in {self.publication_year}"
        )

    def __repr__(self) -> str:
        return (
            f"Book("
            f"id={self.id!r}, "
            f"isbn={self.isbn!r}, "
            f"title={self.title!r}, "
            f"publication_year={self.publication_year!r}, "
            f"author_id={self.author_id!r})"
        )