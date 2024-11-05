from flask import Blueprint
from mutant_detector.controllers.mutant_controller import mutant, stats

api_routes = Blueprint('api', __name__)

@api_routes.route('/mutant/', methods=['POST'])
def mutant_route():
    return mutant()

@api_routes.route('/stats', methods=['GET'])
def stats_route():
    return stats()

