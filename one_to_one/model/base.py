from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()  # sqlalchemy의 declarative base로 동작하도록 클래스를 설정
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        # 자동으로 __tablename__을 상속한 클래스 이름 소문자로로 만들어 주는 기능
        return cls.__name__.lower()
