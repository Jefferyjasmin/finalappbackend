from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    income = db.Column(db.Integer, unique=False, nullable =False)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "income": self.income,
            "user_name": self.user_name
            
            # do not serialize the password, its a security breach
        }



class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable =False)

    def __repr__(self):
        return '<Expense %r>' % self.label
    
    def serialize(self):
         return {
            "id": self.id,
            "value": self.value,   
            "label": self.label
            # do not serialize the password, its a security breach
        }
class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120), unique=True, nullable=False)
    user_name = db.Column(db.String(120), unique=True, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "password": self.password,
            "user_name": self.user_name
            
            # do not serialize the password, its a security breach
        }