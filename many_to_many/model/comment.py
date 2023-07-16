from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Comment(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(500), nullable=False)

    posts = relationship(  # post랑 다대다 관계
        'Post',
        secondary='post_comment',
        primaryjoin='Comment.id == post_comment.c.comment_id',
        secondaryjoin='post_comment.c.post_id == Post.id',
        back_populates='comments',
        lazy='selectin'
    )

    @property
    def in_posts(self):
        return [(post.title, post.description) for post in self.posts]
