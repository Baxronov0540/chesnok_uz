from pydantic import BaseModel, EmailStr, model_validator
from zxcvbn import zxcvbn
from datetime import datetime


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    password2: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegisterRequest":
        if self.password != self.password2:
            raise ValueError("passwords do not match")

        if len(self.password) < 8:
            raise ValueError("password must be at least 8 characters long")

        if zxcvbn(self.password) and zxcvbn(self.password)["score"] < 4:
            raise ValueError("password is weak")
        return self


class UserRegisterResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
