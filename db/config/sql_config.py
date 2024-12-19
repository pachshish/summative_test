from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from psycopg2 import connect
import psycopg2.errors


def create_session(database_uri: str) -> scoped_session:
    """Create a scoped session using SQLAlchemy."""
    engine = create_engine(database_uri)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return scoped_session(SessionLocal)



def create_database_if_not_exists(db_name, user, password, host="localhost"):
    """יוצרת מסד נתונים אם לא קיים."""
    try:
        # חיבור למסד הנתונים הראשי (postgres)
        conn = connect(f"dbname=postgres user={user} password={password} host={host}")
        conn.autocommit = True
        cursor = conn.cursor()

        # בדיקה אם מסד הנתונים קיים
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"מסד הנתונים '{db_name}' נוצר בהצלחה!")
        else:
            print(f"מסד הנתונים '{db_name}' כבר קיים.")
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"שגיאה ביצירת מסד הנתונים: {e}")
