from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Post(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=False)

    tags = relationship(  # tag랑 다대다 관계
        'Tag',
        secondary='post_tag',
        primaryjoin='Post.id == post_tag.c.post_id',
        secondaryjoin='post_tag.c.tag_id == Tag.id',
        back_populates='posts',
        lazy='selectin'
    )

    @property
    def in_tags(self):
        return [tag.content for tag in self.tags]
