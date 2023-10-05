from sqlalchemy.orm import validates
from sqlalchemy import MetaData, ForeignKey
from flask_sqlalchemy import SQLAlchemy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define a one-to-many relationship with User_blogposts
    blogposts = db.relationship('User_blogposts', backref='user')

    def __repr__(self):
        return f'(id={self.id}, username={self.username} email={self.email})'

class Blogpost(db.Model):
    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(100))
    rating = db.Column(db.String())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define a one-to-many relationship with User_blogposts
    users = db.relationship('User_blogposts', backref='blogpost')

    def __repr__(self):
        return f'(id={self.id}, name={self.name} description={self.description})'

    @validates('description')
    def checks_description(self, key, description):
        if len(description) < 100:
            return description

class User_blogposts(db.Model):
    __tablename__ = 'user_blogposts'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String())
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    blogpost_id = db.Column(db.Integer, ForeignKey('blogposts.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define many-to-one relationships with User and Blogpost
    

    def __repr__(self):
        return f'(id={self.id}, userID={self.user_id} rating={self.rating}) blogpostID={self.blogpost_id}'

    @validates('rating')
    def checks_rating(self, key, rating):
        if rating in ['Good', 'Awesome', 'Fantastic']:
            raise ValueError("Rating must be a value either 'Good', 'Awesome', or 'Fantastic'")
        else:
            return rating
        
        
