from db.config.sql_config import create_session
from db.config.sql_ditails import database_uri
from sqlalchemy import text
from db.models.csv1_model import Base, Country, TerrorAttack, Region, Attack, TargetSpecific, Target, Location




def init_db():
    session = create_session(database_uri)
    try:
        engine = session.bind
        Base.metadata.create_all(engine)
        print("All tables created successfully!")
    except Exception as e:
        print(f"Error during database initialization: {e}")
    finally:
        session.remove()


def delete_tables():
    session = create_session(database_uri)
    try:
        # קח את כל הטבלאות
        table_names = [t.name for t in Base.metadata.sorted_tables]

        for table_name in table_names:
            session.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE;"))
            print(f"Table {table_name} deleted successfully!")

        session.commit()
    except Exception as e:
        print(f"Error during table deletion: {e}")
    finally:
        session.remove()

# delete_tables()

