from sqlalchemy import Column, Integer
from .base import Base


class Post_Comment(Base):  # 테이블명 때문에 _ 로 이어줌
    post_id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, primary_key=True)
