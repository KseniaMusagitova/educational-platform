from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmarker, declarative_base
import settings
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator

"""block for common interaction with database"""


# create async engine for interaction with database
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)


#create session for the interaction with database
async_session = sessionmarker(engine, expire_on_comit=False, class_=AsyncSession)

"""block with database models"""

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)


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
        await self.db_session.flush()
        return new_user


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яа-zA-Z\-]+$")

"""block with api models"""


class TunedModel(BaseModel):
    class Config:
        # Tells pydantic to convert even non dict obj to json
        orm_mode = True

class ShowUser(TunedModel):
    user_id: uuid.UUID
    first_name: str
    first_name: str
    email: EmailStr
    is_active: bool

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    @validator("first_name")
    def validate_first_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="First name should contains only letters"
            )
        return value

    @validator("last_name")
    def validate_last_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Last name should contains only letters"
            )
        return value


"""block with api models"""

# create instance of the app
app = FastAPI(title="education-platform")

user_router = APIRouter


async def _create_new_user(body: UserCreate) -> ShowUser:
    async with async_session() as session:
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
async def create_user(body: UserCreate) -> ShowUser:
    return await _create_new_user(body)

