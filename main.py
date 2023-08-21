from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
db.init_app(app)



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        data = request.form
        title = data["title"]
        author = data["author"]
        rating = float(data["rating"])
        new_book = Book(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route('/edit/<int:id>', methods = ["GET","POST"])
def edit(id):
    edit_book = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    if request.method == "POST":
        new_rating = request.form["new_rating"]
        edit_book.rating = float(new_rating)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", book=edit_book)


@app.route('/delete/<int:id>')
def delete(id):
    delete_book = db.get_or_404(Book, id)
    db.session.delete(delete_book)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5002)

