from . import db
from sqlalchemy import Column, Integer, String

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    score = Column(Integer, default=0)
