from datetime import datetime
from sqlalchemy import (Column , Integer , String ,
                             DateTime ,TEXT ,ForeignKey)
from sqlalchemy.orm import relationship
#from sqlalchemy import ForeignKey
from flaskr.database import Base

class User(Base):
    __tablename__ = 'users' 
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password  = Column(String(120), unique=True)
    posts = relationship("Post", backref='posts', lazy=True)
    # children = relationship("Child", backref="parent")
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User : %r>' % (self.username)

class Post(Base):
    __tablename__ = 'posts' 
    id = Column(Integer, primary_key=True)
    # author_id = Column(Integer, ForeignKey('User.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")
    created = Column(DateTime)
    title = Column(TEXT)
    body = Column(TEXT)
    
    def __init__(self, user_id=None , user = None ,created =None,title =None , body=None ):
        self.user_id  = user_id
        self.user= user
        self.created = datetime.utcnow()
        self.title = title
        self.body = body 

    def __repr__(self):
        return 'Post :'+self.title
User.posts = relationship("Post", order_by=Post.id, back_populates="user")