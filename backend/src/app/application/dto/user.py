from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class UserDTO(BaseModel):
    user_id: UUID
    username: str
    role: Literal["user", "admin"] = Field(default="user")


class UserWithPasswordDTO(BaseModel):
    user_id: UUID
    username: str
    password: bytes
    role: Literal["user", "admin"] = Field(default="user")


class UserRegistrationDTO(BaseModel):
    username: str
    password: str
    role: Literal["user", "admin"] = Field(default="user")


class UserCredentialsDTO(BaseModel):
    username: str
    password: str


class UserAddDTO(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    username: str
    password: bytes
    role: Literal["user", "admin"] = Field(default="user")
