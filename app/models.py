from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=True, unique=True)
    email = db.Column(db.String(200), nullable=True, unique=True)
    password = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"