from typing import Union
from model.post import Post
from model.comment import Comment
from model.post_comment import Post_Comment

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("sqlite:///many_to_many.db")

session_factory = sessionmaker(autocommit=False,
                               autoflush=False,
                               bind=engine)


def init_db() -> None:
    """
    many_to_many.db파일 생성 및 테이블 생성
    """
    # 모든 model들은 Base를 상속받아서 다른 테이블은 따로 생성해주지 않아도 자동으로 생성됨
    Post.metadata.create_all(bind=engine)


def create_post(*, session: Session, post_in: dict) -> Post:
    """
    글 만드는 기능
    """
    db_obj = Post(**post_in)
    session.add(db_obj)
    session.commit()
    # relationship에 매핑시킨 속성 refresh
    session.refresh(db_obj, attribute_names=['comments'])
    return db_obj


def create_comment(*, session: Session, comment_in: dict) -> Comment:
    """
    댓글 만드는 기능
    """
    db_obj = Comment(**comment_in)
    session.add(db_obj)
    session.commit()
    # relationship에 매핑시킨 속성 refresh
    session.refresh(db_obj, attribute_names=['posts'])
    return db_obj


def get_model_multi(*, session: Session, model: Union[Post, Post_Comment, Comment]) -> Union[Post, Post_Comment, Comment]:
    query = select(model)
    result = session.execute(query)
    data = result.scalars().all()
    return data


if __name__ == '__main__':
    init_db()  # 테이블 생성
    session = session_factory()

    post1 = create_post(session=session, post_in={'title': 'm2m test1글 제목입니다',
                                                  'description': 'm2m test1 설명'})
    post2 = create_post(session=session, post_in={'title': 'm2m test2글 제목입니다',
                                                  'description': 'm2m test2 설명'})

    comment1 = create_comment(session=session, comment_in={
                              'content': 'm2m test1 댓글1 입니다.'})
    comment2 = create_comment(session=session, comment_in={
                              'content': 'm2m test1 댓글2 입니다.'})
    comment3 = create_comment(session=session, comment_in={
                              'content': 'm2m test2 댓글3 입니다.'})
    comment4 = create_comment(session=session, comment_in={
                              'content': 'm2m test2 댓글4 입니다.'})

    # 중간 테이블인 post_comment에 post와 comment 저장

    comment1.posts.append(post1)
    comment2.posts.append(post1)
    comment3.posts.append(post2)
    comment4.posts.append(post2)
    session.commit()

    # post로 확인
    print('post1의 댓글들')
    print(post1.in_comments)
    print('post2의 댓글들')
    print(post2.in_comments)
    # comment로 확인
    print(f'comment1은 이 글의{comment1.in_posts} 댓글입니다.')
    print(f'comment2은 이 글의{comment2.in_posts} 댓글입니다.')
    print(f'comment3은 이 글의{comment3.in_posts} 댓글입니다.')
    print(f'comment4은 이 글의{comment4.in_posts} 댓글입니다.')
