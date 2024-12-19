from flask import Blueprint
from services.maps_service import fatal_area_service

maps_bp = Blueprint('maps_func_bp', __name__, url_prefix='/maps')


@maps_bp.route('/fatal_area', methods=['GET'])
def find_fatal_area():
    try:
        fatal_area = fatal_area_service()
        return fatal_area, 200
    except Exception as e:
        return f"Failed to get fatal attack area data: {e}", 500
