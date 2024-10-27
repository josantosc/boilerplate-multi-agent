from sqlmodel import Session, create_engine, select, QueuePool

from app.crud.user_crud import create_user
from app.core.config import settings
from app.models.users import Users, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI),
                       poolclass=QueuePool,
                       pool_size=10,
                       max_overflow=20,
                       pool_timeout=30,
                       pool_recycle=1800,
                       echo=True)


def init_db(session: Session) -> None:
    user = session.exec(
        select(Users).where(Users.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name=settings.FIRST_FULL_NAME,
            is_superuser=True,
        )
        create_user(session=session, user_create=user_in)
