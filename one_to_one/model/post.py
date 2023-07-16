from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Post(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String(500))
    owner_id = Column(Integer)

    owner = relationship(  # User랑 1대다 관계
        'User',
        primaryjoin='Post.owner_id == User.id',
        back_populates='posts',
        foreign_keys=owner_id,
        lazy='selectin'
    )

    @property
    def owner_name(self):
        """ 해당 post의 작성자 조회"""
        return self.owner.nickname if self.owner else None
