from sqlmodel import create_engine,Session,SQLModel
from auth.models import User
from todo.models import todotable
from .settings import setting


engine = create_engine(setting.DB_URL,echo=True)


def create_db_on_start():
    print("🟢 Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("🟢 Tables registered:", SQLModel.metadata.tables.keys())


def get_db():
    with Session(engine) as session:
        yield session
        
