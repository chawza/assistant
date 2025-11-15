from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(title="Email", description="The email address of the user", unique=True)
    password: str = Field(title="Password", description="The password of the user", default="")
