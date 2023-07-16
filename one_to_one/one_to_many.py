from model.user import User
from model.post import Post

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///one_to_many.db")

session_factory = sessionmaker(autocommit=False,
                               autoflush=False,
                               bind=engine)


def init_db() -> None:
    """
    one_to_many.db파일 생성 및 테이블 생성
    """
    # 모든 model들은 Base를 상속받아서 다른 테이블은 따로 생성해주지 않아도 자동으로 생성됨
    User.metadata.create_all(bind=engine)


def create_user(*, user_in: dict) -> User:
    """
    사용자 만드는 기능
    """
    with session_factory() as session:
        db_obj = User(**user_in)
        session.add(db_obj)
        session.commit()
        # relationship에 매핑시킨 속성 refresh
        session.refresh(db_obj, attribute_names=['posts'])
    return db_obj


def create_post(*, post_in: dict) -> Post:
    """
    글 만드는 기능
    """
    with session_factory() as session:
        db_obj = Post(**post_in)
        session.add(db_obj)
        session.commit()
        # relationship에 매핑시킨 속성 refresh
        session.refresh(db_obj, attribute_names=['owner'])
    return db_obj


def get_user_posts(*, id: int):
    with session_factory() as session:
        query = select(User).filter(User.id == id).limit(1)
        result = session.execute(query)
        data = result.scalars().first()
        return data


if __name__ == '__main__':
    init_db()  # 테이블 생성
    # user는 id,nickname,password 컬럼을 가짐
    user = create_user(user_in={'nickname': 'dev', 'password': 'dev'})
    # post는 id,title,description,owner_id 컬럼을 가짐
    post1 = create_post(post_in={'title': 'o2m test1글 제목입니다',
                                 'description': 'o2m test1 설명', 'owner_id': user.id})
    post2 = create_post(post_in={'title': 'o2m test2글 제목입니다',
                                 'description': 'o2m test2 설명', 'owner_id': user.id})
    # post 에서 글 쓴 user의 nickname 출력 가능
    print(f'post1 글을 쓴 사람은 : {post1.owner_name}입니다.')
    print(f'post2 글을 쓴 사람은 : {post2.owner_name}입니다.')
    # user가 쓴 글 목록 확인
    user = get_user_posts(id=user.id)
    print(
        f'user가 쓴 글목록은 : {user.my_posts}입니다.')
