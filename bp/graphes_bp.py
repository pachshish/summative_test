import matplotlib.pyplot as plt
from flask import Blueprint

from services.graphs_service import get_attack_graphs

graphs_bp = Blueprint('graphs_func_bp', __name__, url_prefix='/graphs')

@graphs_bp.route('/frequency_of_attacks')
def find_frequency_of_attacks():
    try:
        result = get_attack_graphs()
        return result, 200
    except Exception as e:
        return str(e), 500


