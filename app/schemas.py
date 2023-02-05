from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, EmailStr, conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class postCreate(PostBase):
    pass


class postUpdate(PostBase):
    pass


class postResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class responseOnUpdate(PostBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class userCreate(BaseModel):
    email: EmailStr
    password: str


class userResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class userLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class tokenData(BaseModel):
    id: Optional[str] = None


class postResponseWithOwner(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: userResponse

    class Config:
        orm_mode = True


class postResponseOnUpdateWithOwner(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: userResponse

    class Config:
        orm_mode = True


class Voting(BaseModel):
    post_id: int
    dir: Literal[0, 1]


class PostResponseWithOwnerAndVotes(BaseModel):
    Post: postResponseWithOwner
    votes: int

    class Config:
        orm_mode = True
