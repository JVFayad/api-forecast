import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Forecast(db.Model):
    __tablename__ = 'forecast'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    rain_probab = db.Column(db.Float, nullable=False)
    rain_prect = db.Column(db.Float, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)
    min_temp = db.Column(db.Float, nullable=False)