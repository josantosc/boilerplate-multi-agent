from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int = None


class NewPassword(SQLModel):
    token: str
    new_password: str


class Message(SQLModel):
    message: str
