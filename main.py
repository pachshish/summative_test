from flask import Flask, Blueprint

from bp.graphes_bp import graphs_bp
from bp.maps import maps_bp
from bp.terror_csv_end_point import terror_csv_bp
from db.config.init_db import init_db


app = Flask(__name__)

init_db()
app.register_blueprint(terror_csv_bp)
app.register_blueprint(maps_bp)
app.register_blueprint(graphs_bp)


@app.route('/', methods=['GET'])
def hello_pacjsjiaj():
    return "Hello pachshish"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


