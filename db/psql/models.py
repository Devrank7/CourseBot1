from sqlalchemy import Column, Integer, String, Enum, BigInteger

from db.psql.connect import Base
from db.psql.enums.enums import Roles


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, nullable=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    roles = Column(Enum(Roles), default=Roles.USER)