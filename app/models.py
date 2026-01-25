from datetime import datetime

from sqlalchemy import BigInteger,Integer,String,Boolean,ForeignKey,DateTime,func,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database import Base

class BaseModel(Base):
    __abstract__ = True

    id:Mapped[int]=mapped_column(BigInteger,primary_key=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=func.now())
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=func.now(),onupdate=func.now())

class Media(Base):
    __tablename__="medias" 

    id:Mapped[int]=mapped_column(BigInteger,primary_key=True)
    url:Mapped[str]=mapped_column(String(100))


    user:Mapped["User"]=relationship("User",back_populates="avatar")
    post_media:Mapped[list["PostMedia"]]=relationship("PostMedia",back_populates="media")

class PostMedia(Base):
    __tablename__ = "post_medias"

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("medias.id"), primary_key=True)

    post:Mapped["Post"]=relationship("Post",back_populates="post_media")
    media:Mapped["Media"]=relationship("Media",back_populates="post_media")

    def __repr__(self):
        return f"PostMedia({self.post_id} - {self.media_id})"

class Post(BaseModel):
    __tablename__="posts"

    title:Mapped[str]=mapped_column(String(255))
    slug:Mapped[str]=mapped_column(String(100),unique=True)
    body:Mapped[str]=mapped_column(Text)
    category_id:Mapped[int]=mapped_column(ForeignKey("categories.id"))
    views_count:Mapped[int]=mapped_column(BigInteger,default=0)
    likes_count:Mapped[int]=mapped_column(BigInteger,default=0)
    comments_count:Mapped[int]=mapped_column(BigInteger,default=0)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True)

    #relationship
    category:Mapped["Category"]=relationship("Category",back_populates="posts")
    post_tags:Mapped[list["PostTag"]]=relationship("PostTag",back_populates="post")
    comments:Mapped[list["Comments"]]=relationship("Comments",back_populates="post")
    post_media:Mapped[list["PostMedia"]]=relationship("PostMedia",back_populates="post")

    def __repr__(self):
        return self.title
    

class User(BaseModel):
    __tablename__="users"

    proffesion_id:Mapped[str]=mapped_column(ForeignKey("proffesions.id"))
    email:Mapped[str]=mapped_column(String(100),unique=True)
    avatar_id:Mapped[int]=mapped_column(ForeignKey("medias.id"),onupdate="SET NULL")
    password_hash:Mapped[str]=mapped_column(String(100),nullable=False)
    first_name:Mapped[str]=mapped_column(String(100),nullable=True)
    last_name:Mapped[str]=mapped_column(String(100),nullable=True)
    bio:Mapped[str]=mapped_column(Text,nullable=True)
    post_count:Mapped[int]=mapped_column(BigInteger,default=0)
    post_read_count:Mapped[int]=mapped_column(BigInteger,default=0)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True)
    is_staff:Mapped[bool]=mapped_column(Boolean,default=True)
    is_supperuser:Mapped[bool]=mapped_column(Boolean,default=True)

    proffesion:Mapped["Proffesion"]=relationship("Proffesion",back_populates="users")
    avatar:Mapped["Media"]=relationship("Media",back_populates="user")
    comments:Mapped[list["Comments"]]=relationship("Comments",back_populates="user")


    def __repr__(self):
        return f"User({self.id})"
    
class   Proffesion(Base):
    __tablename__="proffesions"

    id:Mapped[int]=mapped_column(BigInteger,primary_key=True)
    name:Mapped[str]=mapped_column(String(100))

    users:Mapped[list["User"]]=relationship("User",back_populates="proffesion")


class Tag(Base):
    __tablename__="tags"
    id:Mapped[int]=mapped_column(BigInteger,primary_key=True)
    name:Mapped[str]=mapped_column(String(100))
    slug:Mapped[str]=mapped_column(String(100))

    post_tags:Mapped[list["PostTag"]]=relationship("PostTag",back_populates="tag")

class PostTag(Base):
    __tablename__="post_tags"

    post_id:Mapped[int]=mapped_column(ForeignKey("posts.id"),primary_key=True)
    tag_id:Mapped[int]=mapped_column(ForeignKey("tags.id"),primary_key=True)

    post:Mapped["Post"]=relationship("Post",back_populates="post_tags")
    tag:Mapped["Tag"]=relationship("Tag",back_populates="post_tags")



class Category(Base):
    __tablename__="categories"
    id:Mapped[int]=mapped_column(BigInteger,primary_key=True)
    name:Mapped[str]=mapped_column(String(100))
    slug:Mapped[str]=mapped_column(String(100))

    posts:Mapped[list["Post"]]=relationship("Post",back_populates="category")
    
class Comments(Base):
    __tablename__="comments"
    id:Mapped[int]=mapped_column(BigInteger,primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
    text:Mapped[str]=mapped_column(Text)
    post_id:Mapped[int]=mapped_column(ForeignKey("posts.id"))

    user:Mapped["User"]=relationship("User",back_populates="comments")
    post:Mapped["Post"]=relationship("Post",back_populates="comments")

