from flask import Blueprint, request, jsonify
from mutant_detector.services.mutant_service import is_mutant
from mutant_detector.models import DNARecord, Session
from mutant_detector.validators import is_valid_dna_sequence

mutant_bp = Blueprint('mutant_bp', __name__)

@mutant_bp.route('/mutant/', methods=['POST'])
def mutant():
    data = request.get_json()
    dna_sequence = data.get('dna')

    if not dna_sequence:
        return jsonify({"message": "DNA sequence is required"}), 400

    # Validar formato de ADN
    if not is_valid_dna_sequence(dna_sequence):
        return jsonify({"message": "Formato de ADN Incorrecto"}), 400

    # Convertir la secuencia a un string unificado para almacenarlo en la base de datos
    dna_sequence_str = ",".join(dna_sequence)
    session = Session()

    existing_record = session.query(DNARecord).filter_by(sequence=dna_sequence_str).first()

    if existing_record:
        if existing_record.is_mutant:
            session.close()
            return jsonify({"message": "Mutant detected"}), 200
        else:
            session.close()
            return jsonify({"message": "Forbidden"}), 403

    is_mutant_result = is_mutant(dna_sequence)

    try:
        record = DNARecord(sequence=dna_sequence_str, is_mutant=int(is_mutant_result))
        session.add(record)
        session.commit()
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({"message": "Failed to save DNA record"}), 500
    finally:
        session.close()

    if is_mutant_result:
        return jsonify({"message": "Mutant detected"}), 200
    else:
        return jsonify({"message": "Forbidden"}), 403

@mutant_bp.route('/stats', methods=['GET'])
def stats():
    session = Session()
    mutant_count = session.query(DNARecord).filter_by(is_mutant=1).count()
    human_count = session.query(DNARecord).filter_by(is_mutant=0).count()
    session.close()

    ratio = mutant_count / human_count if human_count > 0 else 0
    return jsonify({
        "count_mutant_dna": mutant_count,
        "count_human_dna": human_count,
        "ratio": ratio
    }), 200



