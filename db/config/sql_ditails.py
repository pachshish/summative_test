from sqlalchemy.orm import declarative_base


# database_uri = "postgresql://admin:1234@postgres:5432/finish_projects"
# הגדרת ה-URI של חיבור לבסיס הנתונים
database_uri = "postgresql://admin:1234@localhost:5432/summative_test"

Base = declarative_base()
