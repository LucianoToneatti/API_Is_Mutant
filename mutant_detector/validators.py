import re

def is_valid_dna_sequence(dna_sequence):
    n = len(dna_sequence)
    if not all(len(row) == n for row in dna_sequence):
        return False
    valid_chars = re.compile("^[ATCG]+$")
    return all(valid_chars.match(row) for row in dna_sequence)

