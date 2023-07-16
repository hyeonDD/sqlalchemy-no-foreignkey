from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    posts = relationship(  # post랑 1대다 관계
        'Post',
        primaryjoin='User.id == Post.owner_id',
        back_populates='owner',
        foreign_keys='Post.owner_id',
        lazy='selectin'
    )

    @property
    def my_posts(self):
        """ 해당 user가 작성한 글들 조회"""
        return [post.title for post in self.posts]
