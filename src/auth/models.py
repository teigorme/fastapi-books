from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from src.database.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
