"""
from flask import Flask, request, jsonify
from mutant_detector.services.mutant_service import is_mutant
from mutant_detector.models import DNARecord, Session
import os
import re

app = Flask(__name__)

def is_valid_dna_sequence(dna_sequence):
    # Validar que sea una matriz NxN
    n = len(dna_sequence)
    if not all(len(row) == n for row in dna_sequence):
        return False
    # Validar que solo contenga los caracteres permitidos (A, T, C, G)
    valid_chars = re.compile("^[ATCG]+$")
    return all(valid_chars.match(row) for row in dna_sequence)

@app.route('/mutant/', methods=['POST'])
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
    
    # Verificar si la secuencia de ADN ya existe en la base de datos
    existing_record = session.query(DNARecord).filter_by(sequence=dna_sequence_str).first()
    
    if existing_record:
        # Si el registro ya existe, retornamos su estado sin intentar guardarlo de nuevo
        if existing_record.is_mutant:
            session.close()
            return jsonify({"message": "Mutant detected"}), 200
        else:
            session.close()
            return jsonify({"message": "Forbidden"}), 403
    
    # Si el ADN no existe, procedemos con la detección e inserción en la base de datos
    is_mutant_result = is_mutant(dna_sequence)
    
    try:
        # Crear y guardar el nuevo registro en la base de datos
        record = DNARecord(sequence=dna_sequence_str, is_mutant=int(is_mutant_result))
        session.add(record)
        session.commit()
    except Exception as e:
        session.rollback()  # Revierte si hay un error
        session.close()
        return jsonify({"message": "Failed to save DNA record"}), 500
    finally:
        session.close()

    # Responder en función de si el ADN es mutante o no
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


"""