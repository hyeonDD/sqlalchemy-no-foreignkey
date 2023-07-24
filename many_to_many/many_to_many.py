from typing import Union
from model.post import Post
from model.tag import Tag
from model.post_tag import Post_Tag

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
    session.refresh(db_obj, attribute_names=['tags'])
    return db_obj


def create_tag(*, session: Session, tag_in: dict) -> Tag:
    """
    태그 만드는 기능
    """
    db_obj = Tag(**tag_in)
    session.add(db_obj)
    session.commit()
    # relationship에 매핑시킨 속성 refresh
    session.refresh(db_obj, attribute_names=['posts'])
    return db_obj


def get_model_multi(*, session: Session, model: Union[Post, Post_Tag, Tag]) -> Union[Post, Post_Tag, Tag]:
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

    tag1 = create_tag(session=session, tag_in={
        'content': 'm2m test1 태그1 입니다.'})
    tag2 = create_tag(session=session, tag_in={
        'content': 'm2m test1 태그2 입니다.'})
    tag3 = create_tag(session=session, tag_in={
        'content': 'm2m test2 태그3 입니다.'})
    tag4 = create_tag(session=session, tag_in={
        'content': 'm2m test2 태그4 입니다.'})

    # 중간 테이블인 post_tag에 post와 tag 저장

    tag1.posts.append(post1)
    tag2.posts.append(post1)
    tag3.posts.append(post2)
    tag4.posts.append(post2)
    session.commit()

    # post로 확인
    print('post1의 태그들')
    print(post1.in_tags)
    print('post2의 태그들')
    print(post2.in_tags)
    # tag로 확인
    print(f'tag1은 이 글의{tag1.in_posts} 태그입니다.')
    print(f'tag2은 이 글의{tag2.in_posts} 태그입니다.')
    print(f'tag3은 이 글의{tag3.in_posts} 태그입니다.')
    print(f'tag4은 이 글의{tag4.in_posts} 태그입니다.')
