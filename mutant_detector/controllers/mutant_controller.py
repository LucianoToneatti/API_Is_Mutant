# controllers/mutant_controller.py
from flask import Blueprint, request, jsonify
from services.mutant_service import is_mutant

mutant_bp = Blueprint('mutant_bp', __name__)

@mutant_bp.route('/mutant/', methods=['POST'])
def detect_mutant():
    data = request.get_json()
    dna = data.get("dna")

    if not dna:
        return jsonify({"error": "No DNA sequence provided"}), 400
    
    if is_mutant(dna):
        return jsonify({"message": "Mutant detected"}), 200
    else:
        return jsonify({"message": "Not a mutant"}), 403
