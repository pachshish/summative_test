from db.config.sql_config import create_session
from db.config.sql_ditails import database_uri, Base


# add the models
# Initialize the database



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
