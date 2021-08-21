from flask import Flask, request, flash, url_for, redirect, render_template
from werkzeug.utils import secure_filename
import base64
import datetime
from db import db_init, db
from models import books
import utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite3'
db_init(app)

@app.route('/upload')
def upload_file():
   return render_template('book.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def handle_upload_file():
   if request.method == 'POST':
      #get name and author
      name = request.form['name']
      author = request.form['author']

      #get release-date as string and parse it date object to orm
      rd = request.form['release-date']
      rd = datetime.datetime.strptime(rd, '%Y-%m')

      #get orginal image file
      file = request.files['img']

      stream, min, max, mean, std = utils.deal_img_file(file)
      #create book object and send it orm
      book = books(name, stream.getvalue(), author, rd, min, max, mean, std)
      db.session.add(book)
      db.session.commit()
      return redirect(url_for('show_all', kw="all"))

@app.route('/<string:kw>')
#if base uri /all show all books
def show_all(kw):
  if(kw == "all"):
    l = books.query.all()
  #if search keyword is exist, filter books
  #search as book name and author name and show
  else:
    n = books.query.filter_by(name=kw).all()
    a = books.query.filter_by(author=kw).all()
    l = n + a
  for r in l:
    #encode pictures byte with base64 to give them as src in html img tag
    #pictures cannot shown corectly. Probably, i made mistake in decode op
    #or db data types. Normally Blob data types use to save picture but 
    #when i can try to blob data types, i give error.
    r.img = u'data:image/jpeg;charset=utf-8; base64, {}'.format(base64.b64encode(r.img)) #from stackoverflow
  return render_template('all.html', books = l)

@app.route('/delete/<int:bookID>')
def delete_book(bookID):
  books.query.filter_by(id=bookID).delete()
  db.session.commit()
  return redirect(url_for('show_all', kw="all"))

#get book will change via id and 
#pass them to form to change
@app.route('/update/<int:bookID>')
def update_book(bookID):
  b = books.query.filter_by(id=bookID).first()
  db.session.commit()
  return render_template('book-update.html', book = b)

#change book attribute
@app.route('/updater/<int:bookID>', methods = ['GET', 'POST'])
def update_book_handler(bookID):
  if request.method == 'POST':
    b = books.query.filter_by(id=bookID).first()
    name = request.form['name']
    author = request.form['author']
    rd = request.form['release-date']
    file = request.files['img']
    if(name != ""):
      b.name = name
    if(author != ""):
      b.author = author
    if(rd != ""):
      b.release_date = datetime.datetime.strptime(request.form['release-date'], '%Y-%m')
    if(file):
      stream, min, max, mean, std = utils.deal_img_file(file)
      b.img = stream.getvalue()
      b.min = min
      b.max = max
      b.mean = mean
      b.std = std
    db.session.commit()
  return redirect(url_for('show_all', kw ="all"))
@app.route('/search', methods=['GET', 'POST'])
def search():
  key = request.form['search']
  if(key == ""):
    key = "all"
  return redirect(url_for('show_all', kw = key))


if __name__ == '__main__':
  app.run(debug = True)