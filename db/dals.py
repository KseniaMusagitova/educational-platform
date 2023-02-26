from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

"""block for interaction with database in business context"""
class UserDAL:
    # Data Access Layer for operating user info
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, first_name: str, last_name: str, email: str
    ) -> User:
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush() # асинхронная добавка данных в postgres с помощью команды flush
        return new_user
