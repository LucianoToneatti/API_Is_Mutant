# main.py
from flask import Flask, request, jsonify
from services.mutant_service import is_mutant
from models import DNARecord, Session

app = Flask(__name__)

@app.route('/mutant/', methods=['POST'])
def mutant():
    data = request.get_json()
    dna_sequence = data.get('dna')
    
    if not dna_sequence:
        return jsonify({"message": "DNA sequence is required"}), 400
    
    is_mutant_result = is_mutant(dna_sequence)
    session = Session()

    # Store the DNA record in the database
    record = DNARecord(sequence=",".join(dna_sequence), is_mutant=int(is_mutant_result))
    session.add(record)
    session.commit()
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

if __name__ == '__main__':
    app.run(debug=True)
