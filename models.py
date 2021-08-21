from db import db

class books(db.Model):
  id = db.Column('student_id', db.Integer(), primary_key = True)
  name = db.Column('name', db.String(100))
  img = db.Column('img', db.LargeBinary())
  author = db.Column('author', db.String(100))
  release_date = db.Column('release_date', db.Date())
  min = db.Column('min', db.Float())
  max = db.Column('max', db.Float())
  mean = db.Column('mean', db.Float())
  std = db.Column('std', db.Float())
  def __init__(self, name, img, author , release_date, min, max, mean, std):
   self.name = name
   self.img = img
   self.author = author
   self.release_date = release_date
   self.min = min
   self.max = max
   self.mean = mean
   self.std = std