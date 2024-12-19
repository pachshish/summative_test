from flask import Blueprint

from csv_data1.add_csv_to_db import add_csv1_to_db
from services.end_point_service import fatal_attack_service, fatal_area_service

terror_csv_bp = Blueprint('terror_bp', __name__, url_prefix='/terror_csv')

@terror_csv_bp.route('/', methods=['GET'])
def get_pachshish():
    return "Haaa Lirazushhhhhhh :)"

@terror_csv_bp.route('/add_data_from_csv1', methods=['POST'])
def add_data_from_csv1():
    try:
        add_csv1_to_db()
        print("אחלן פחשישששש")
        return 'אחלן פחשישששש', 204
    except Exception as e:
        return f"Failed to send data: {e}", 500

@terror_csv_bp.route('/fatal_attack', methods=['GET'])
def find_fatal_attack():
    try:
        fatal = fatal_attack_service()
        return fatal, 200
    except Exception as e:
        return f"Failed to get fatal attack data: {e}", 500

@terror_csv_bp.route('/fatal_area', methods=['GET'])
def find_fatal_area():
    try:
        fatal_area = fatal_area_service()
        return fatal_area, 200
    except Exception as e:
        return f"Failed to get fatal attack area data: {e}", 500