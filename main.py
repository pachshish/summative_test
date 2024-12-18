from flask import Flask, Blueprint

from bp.terror_csv_end_point import terror_csv_bp

app = Flask(__name__)

app.register_blueprint(terror_csv_bp)



@app.route('/', methods=['GET'])
def hello_pacjsjiaj():
    return "Hello pachshish"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


