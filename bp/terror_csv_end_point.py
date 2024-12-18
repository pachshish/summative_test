from flask import Blueprint

terror_csv_bp = Blueprint('terror_bp', __name__, url_prefix='/terror_csv')

@terror_csv_bp.route('/', methods=['GET'])
def get_pachshish():
    return "Haaa Lirazushhhhhhh :)"