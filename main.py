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
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)


"""block for interaction with database in business context"""