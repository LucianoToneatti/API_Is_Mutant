from flask import Flask, request, jsonify
from mutant_detector.services.mutant_service import is_mutant
from mutant_detector.models import DNARecord, Session
import os

app = Flask(__name__)

@app.route('/mutant/', methods=['POST'])
def mutant():
    data = request.get_json()
    dna_sequence = data.get('dna')
    
    if not dna_sequence:
        return jsonify({"message": "DNA sequence is required"}), 400
    
    is_mutant_result = is_mutant(dna_sequence)
    session = Session()

    # Intentar guardar el registro de ADN
    try:
        record = DNARecord(sequence=",".join(dna_sequence), is_mutant=int(is_mutant_result))
        session.add(record)
        session.commit()
    except Exception as e:
        session.rollback()  # Revierte si hay un error
        return jsonify({"message": "Failed to save DNA record"}), 500
    finally:
        session.close()

    if is_mutant_result:
        return jsonify({"message": "Mutant detected"}), 200
    else:
        return jsonify({"message": "Forbidden"}), 403  # Cambiado de "Not a mutant" a "Forbidden"

@app.route('/stats', methods=['GET'])
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

if __name__ == "__main__":
    # Render establece la variable de entorno PORT para el puerto
    port = int(os.environ.get("PORT", 5000))  # 5000 es el puerto por defecto
    app.run(host='0.0.0.0', port=port)

