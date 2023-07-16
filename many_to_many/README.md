# 외래키 없는 다대다 관계 create table문 확인

## sqlalchemy의 metadata.create_all로 생성되는 post 테이블 출력
```shell
CREATE TABLE post (
        id INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        description VARCHAR(500) NOT NULL,
        PRIMARY KEY (id)
)
```

## sqlalchemy의 metadata.create_all로 생성되는 comment 테이블 출력
```shell
CREATE TABLE comment (
        id INTEGER NOT NULL,
        content VARCHAR(500) NOT NULL,
        PRIMARY KEY (id)
)
```

## sqlalchemy의 metadata.create_all로 생성되는 post_comment 테이블 출력
```shell
CREATE TABLE post_comment (
        post_id INTEGER NOT NULL,
        comment_id INTEGER NOT NULL,
        PRIMARY KEY (post_id, comment_id)
)
```

### post들은 comment들을 조회할 수 있음
post들의 comment를 조회
```python
print('post1의 댓글들')
print(post1.in_comments)
print('post2의 댓글들')
print(post2.in_comments)
```
출력
```shell
# post로 확인
post1의 댓글들
['m2m test1 댓글1 입니다.', 'm2m test1 댓글2 입니다.']
post2의 댓글들
['m2m test2 댓글3 입니다.', 'm2m test2 댓글4 입니다.']
```

### comment들은 post들을 조회할 수 있음
comment가 작성된 post들을 조회
```python
# comment로 확인
print(f'comment1은 이 글의{comment1.in_posts} 댓글입니다.')
print(f'comment2은 이 글의{comment2.in_posts} 댓글입니다.')
print(f'comment3은 이 글의{comment3.in_posts} 댓글입니다.')
print(f'comment4은 이 글의{comment4.in_posts} 댓글입니다.')
```
출력
```shell
comment1은 이 글의[('m2m test1글 제목입니다', 'm2m test1 설명')] 댓글입니다.
comment2은 이 글의[('m2m test1글 제목입니다', 'm2m test1 설명')] 댓글입니다.
comment3은 이 글의[('m2m test2글 제목입니다', 'm2m test2 설명')] 댓글입니다.
comment4은 이 글의[('m2m test2글 제목입니다', 'm2m test2 설명')] 댓글입니다.
```