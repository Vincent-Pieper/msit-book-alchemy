import os

from flask import Flask
from data_models import db, Author, Book


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)

db.init_app(app)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)