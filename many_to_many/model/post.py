from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Post(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=False)

    comments = relationship(  # comment랑 다대다 관계
        'Comment',
        secondary='post_comment',
        primaryjoin='Post.id == post_comment.c.post_id',
        secondaryjoin='post_comment.c.comment_id == Comment.id',
        back_populates='posts',
        lazy='selectin'
    )

    @property
    def in_comments(self):
        return [comment.content for comment in self.comments]
