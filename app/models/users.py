from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional


def current_time():
    return datetime.now().isoformat()


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    full_name: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=current_time())


class UserCreate(UserBase):
    password: str


class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str = None


class UserUpdate(UserBase):
    email: str = None  # type: ignore
    password: str = None


class UserUpdateMe(SQLModel):
    full_name: str = None
    email: str = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


class Users(UserBase, table=True):
    __tablename__ = 'users'

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    #filters: List['CampaignContactFilter'] = Relationship(back_populates="owner")
    #status_campaigns: List['StatusCampaign'] = Relationship(back_populates="owner")
    #flows: List['NotificationFlow'] = Relationship(back_populates="owner")
    #campaigns: List['Campaigns'] = Relationship(back_populates="owner")
    #clients: List['Clients'] = Relationship(back_populates="owner")


class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: List[UserPublic]
    count: int
