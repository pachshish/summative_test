from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def create_session(database_uri: str) -> scoped_session:
    """Create a scoped session using SQLAlchemy."""
    engine = create_engine(database_uri)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return scoped_session(SessionLocal)