# 외래키 없는 일대다 관계 create table문 확인

## sqlalchemy의 metadata.create_all로 생성되는 user 테이블 출력
```shell
CREATE TABLE user (
        id INTEGER NOT NULL,
        nickname VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL,
        PRIMARY KEY (id)
)
```

## sqlalchemy의 metadata.create_all로 생성되는 post 테이블 출력
```shell
CREATE TABLE post (
        id INTEGER NOT NULL,
        title VARCHAR(255),
        description VARCHAR(500),
        owner_id INTEGER,
        PRIMARY KEY (id)
)
```

### post들은 user를 조회할 수 있음
post들의 user를 조회
```python
print(f'post1 글을 쓴 사람은 : {post1.owner.nickname}입니다.')
print(f'post2 글을 쓴 사람은 : {post2.owner.nickname}입니다.')
```
출력
```shell
post1 글을 쓴 사람은 : dev입니다.
post2 글을 쓴 사람은 : dev입니다.
```

### user는 post들을 조회할 수 있음
user가 post들을 작성한 post들을 조회
```python
user = get_user_posts(id=user.id)
print(f'user가 쓴 글목록은 : {user.my_posts}입니다.')
```
출력
```shell
user가 쓴 글목록은 : ['test1글 제목입니다', 'test2글 제목입니다']입니다.
```