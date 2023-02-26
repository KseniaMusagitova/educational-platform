import re
import uuid
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator


"""block with api models"""
LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        # Tells pydantic to convert even non dict obj to json
        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    first_name: str
    last_name: str
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


