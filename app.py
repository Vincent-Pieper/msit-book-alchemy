import os
from datetime import date

from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import select

from data_models import db, Author, Book


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)


db.init_app(app)


def get_authors() -> list[Author]:
    """Return all authors ordered by name."""
    stmt = select(Author).order_by(Author.name)
    return db.session.scalars(stmt).all()


def get_books(sort_by: str, search_query: str | None = None) -> list[Book]:
    """Return books ordered by the selected sorting option and optionally filtered by title."""
    if sort_by == "published":
        stmt = select(Book).order_by(Book.publication_year)
    elif sort_by == "author":
        stmt = select(Book).join(Author).order_by(Author.name)
    else:
        stmt = select(Book).order_by(Book.title)

    if search_query:
        stmt = stmt.where(Book.title.ilike(f"%{search_query}%"))

    return db.session.scalars(stmt).all()


@app.route("/add_author", methods=["GET"])
def get_add_author_page():
    """Render the form for adding a new author."""
    return render_template("add_author.html")


@app.route("/add_author", methods=["POST"])
def create_author():
    """Create a new author from form data."""
    name = request.form["name"]
    birthdate = request.form["birthdate"]
    date_of_death = request.form["date_of_death"]

    birthdate = date.fromisoformat(birthdate)

    if date_of_death == "":
        date_of_death = None
    else:
        date_of_death = date.fromisoformat(date_of_death)

    new_author = Author(
        name=name,
        birthdate=birthdate,
        date_of_death=date_of_death,
    )

    db.session.add(new_author)
    db.session.commit()

    return render_template(
        "add_author.html",
        message=f"Author '{name}' added successfully.",
    )


@app.route("/add_book", methods=["GET"])
def get_add_book_page():
    """Render the form for adding a new book."""
    return render_template(
        "add_book.html",
        authors=get_authors(),
    )


@app.route("/add_book", methods=["POST"])
def create_book():
    """Create a new book from form data."""
    isbn = request.form["isbn"]
    title = request.form["title"]
    publication_year = request.form["publication_year"]
    author_id = request.form["author_id"]

    new_book = Book(
        isbn=isbn,
        title=title,
        publication_year=int(publication_year),
        author_id=int(author_id),
    )

    db.session.add(new_book)
    db.session.commit()

    return render_template(
        "add_book.html",
        authors=get_authors(),
        message=f"Book '{title}' added successfully.",
    )


@app.route("/", methods=["GET"])
def get_home_page():
    """Render the library homepage with sorting and keyword search."""
    sort_by = request.args.get("sort_by", "title")
    search_query = request.args.get("search", "").strip()
    message = request.args.get("message")

    books = get_books(sort_by, search_query)

    if search_query and not books:
        message = f"No books found for '{search_query}'."

    return render_template(
        "home.html",
        books=books,
        sort_by=sort_by,
        search_query=search_query,
        message=message,
    )


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id: int):
    """Delete a book by ID and redirect to the homepage."""
    book = db.session.get(Book, book_id)

    if book is None:
        return redirect(url_for(
            "get_home_page",
            message="Book not found.",
        ))

    title = book.title

    db.session.delete(book)
    db.session.commit()

    return redirect(url_for(
        "get_home_page",
        message=f"Book '{title}' deleted successfully.",
    ))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)