from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


class MyComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('my_product.product_id'), nullable=False)
    user = db.Column(db.String(100), nullable=False, default="0")
    content = db.Column(db.String(1000), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False, default=0)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    embedding = db.Column(JSON)

    product = db.relationship("MyProduct", backref="comments") 

    def __repr__(self) -> str:
        return f"Comment {self.id}"


class MyProduct(db.Model):
    __tablename__ = 'my_product' 

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(1000), nullable=False)
    admin_name = db.Column(db.String(1000), db.ForeignKey('user.username'), nullable=False) 
    active = db.Column(db.Boolean, default=True)
    admin = db.relationship('User', backref='products', lazy=True) 

    def __repr__(self):
        return f"Product {self.product_id}: {self.product_name}"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
