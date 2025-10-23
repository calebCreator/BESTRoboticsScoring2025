from . import db
from sqlalchemy.sql import func

class Match(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default= func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
