import secrets
from . import db
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    due_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', back_populates='tasks')


    @property
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at,
            'due_date': self.due_date,
        }
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    token = db.Column(db.String, index=True, unique=True, default="default")
    token_expiration = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5))
    tasks = db.relationship('Task', back_populates='author')


    def set_password(self, plaintext_password):
        self.password = generate_password_hash(plaintext_password)
        self.save()



    def check_password(self, plaintext_password):
        return check_password_hash(self.password, plaintext_password)




    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_password(kwargs.get('password', ''))

    def __init__(self,**kwargs):
        super(User, self).__init__(**kwargs)
        self.get_token()

    def get_token(self):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return {"token": self.token, "token_expiration": self.token_expiration}
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(minutes=5)
        db.session.add(self)
        db.session.commit()
        return {"token": self.token, "token_expiration": self.token_expiration}

    def check_password(self, password):
        return hash(password) == self.password_hash


    @property
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_created': self.date_created,
        }

