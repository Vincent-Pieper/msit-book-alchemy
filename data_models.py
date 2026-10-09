from datetime import date

from sqlalchemy import String, Integer, Date, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_of_death: Mapped[date | None] = mapped_column(Date, nullable=True)

    def __str__(self) -> str:
        return (
            f"{self.name}, "
            f"born in {self.birth_date}, "
            f"deceased in {self.date_of_death}"
        )

    def __repr__(self) -> str:
        return (
            f"ID: {self.id} -- "
            f"name: {self.name} -- "
            f"born: {self.birth_date} -- "
            f"died {self.date_of_death}"
        )


class Book(db.Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    publication_year: Mapped[int] = mapped_column(Integer)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    def __str__(self) -> str:
        return (
            f"{self.title}, "
            f"published in {self.publication_year}, "
        )

    def __repr__(self) -> str:
        return (
            f"ID: {self.id} -- "
            f"title: {self.title} -- "
            f"published: {self.publication_year} -- "
            f"isbn {self.isbn}"
        )

