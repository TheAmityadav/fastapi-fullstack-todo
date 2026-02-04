from sqlmodel import SQLModel,Field


class todotable(SQLModel,table=True):
    id : int | None = Field(default=None,primary_key=True)
    todo : str
    is_done : bool = Field(default=False)
    is_deleted : bool = Field(default=False)
    user_id : str = Field(foreign_key="user.id")


