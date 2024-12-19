from flask import Flask, Blueprint

from bp.terror_csv_end_point import terror_csv_bp
from db.config.init_db import init_db
from db.config.sql_config import create_database_if_not_exists

app = Flask(__name__)


# פרטי מסד הנתונים
# db_name = "summative_test"
# user = "postgres"
# password = "1234"

# יצירת מסד נתונים אם לא קיים
# create_database_if_not_exists(db_name, user, password)

init_db()
app.register_blueprint(terror_csv_bp)


@app.route('/', methods=['GET'])
def hello_pacjsjiaj():
    return "Hello pachshish"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


