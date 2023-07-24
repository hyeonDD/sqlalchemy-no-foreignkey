from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Tag(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(500), nullable=False)

    posts = relationship(  # post랑 다대다 관계
        'Post',
        secondary='post_tag',
        primaryjoin='Tag.id == post_tag.c.tag_id',
        secondaryjoin='post_tag.c.post_id == Post.id',
        back_populates='tags',
        lazy='selectin'
    )

    @property
    def in_posts(self):
        return [(post.title, post.description) for post in self.posts]
