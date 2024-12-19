from flask import Blueprint

from csv_data1.add_csv_to_db import add_csv1_to_db
from services.end_point_service import fatal_attack_service, top_5_groups_with_casualties_service

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


@terror_csv_bp.route('/top_5_groups_with_casualties', methods=['GET'])
def find_top_5_groups_with_casualties():
    try:
        top_5_groups = top_5_groups_with_casualties_service()
        return top_5_groups, 200
    except Exception as e:
        return f"Failed to get top 5 groups with casualties data: {e}", 500