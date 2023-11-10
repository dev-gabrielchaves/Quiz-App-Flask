from app import db

# Table responsible for saving the users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=True, unique=True)
    email = db.Column(db.String(200), nullable=True, unique=True)
    password = db.Column(db.String(60), nullable=True)
    
    # Establish a one-to-many relationship with UserScore
    scores = db.relationship('UserScore', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"

# Table responsible for saving the user's scores    
class UserScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float)

    # Define a foreign key relationship with the User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"UserScore('{self.score}', '{self.user_id}')"