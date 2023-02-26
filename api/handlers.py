from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from api.models import UserCreate, ShowUser
from db.dals import UserDAL
from db.session import get_db
from fastapi import Depends


user_router = APIRouter() #подвязывает пути


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                first_name=body.first_name,
                last_name=body.last_name,
                email=body.email,
            )
            return ShowUser(
                user_id=user.user_id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_active=user.is_active,
        )


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, db)