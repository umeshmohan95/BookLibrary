import sqlite3

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


##create table

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    auther = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float(250), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

db.create_all()

# new_book = Book(id=1, title="Harry Potter", auther="J. K. Rowling", rating=9.3)
# db.session.add(new_book)
# db.session.commit()


###################### using SQLite


# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()

# cursor.execute("CREATE TABLE books (id INTEGER PRIMAERY KEY,"
#                "title varchar(250) NOT NULL UNIQUE,"
#                "auther varchar(250) NOT NULL,"
#                "rating FLOAT NOT NULL)")


# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

# all_books = []


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books = all_books)


@app.route('/add', methods=['GET','POST'])
def addBook():
    if request.method == 'POST':

        ####using SQLite
        book_name = request.form['title']
        book_auther = request.form['auther']
        book_rating = request.form['rating']
        # new_book = {
        #     'title' : book_name,
        #     'auther' : book_auther,
        #     'rating' : book_rating
        # }
        #
        # all_books.append(new_book)

        new_book = Book(title=book_name, auther=book_auther , rating=book_rating)
        db.session.add(new_book)
        db.session.commit()



        all_books = db.session.query(Book).all()

        print(all_books[0].title)

        # return render_template('index.html', books = all_books)
        return redirect(url_for('home'))

    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)
