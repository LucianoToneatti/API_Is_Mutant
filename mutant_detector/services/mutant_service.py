def is_mutant(dna):
    n = len(dna)
    matrix = [list(row) for row in dna]  # Convertimos el array de Strings en una matriz de caracteres
    sequence_count = 0

    # Función para verificar las secuencias en las tres direcciones
    for i in range(n):
        for j in range(n):
            if (check_horizontal(matrix, i, j, n) or
                check_vertical(matrix, i, j, n) or
                check_diagonal(matrix, i, j, n)):
                sequence_count += 1
                if sequence_count > 1:
                    return True  # Mutante

    return False  # No es mutante


def check_horizontal(matrix, row, col, n):
    """Verifica si hay una secuencia horizontal de cuatro letras iguales."""
    if col + 3 < n:
        return (matrix[row][col] == matrix[row][col + 1] ==
                matrix[row][col + 2] == matrix[row][col + 3])
    return False


def check_vertical(matrix, row, col, n):
    """Verifica si hay una secuencia vertical de cuatro letras iguales."""
    if row + 3 < n:
        return (matrix[row][col] == matrix[row + 1][col] ==
                matrix[row + 2][col] == matrix[row + 3][col])
    return False


def check_diagonal(matrix, row, col, n):
    """Verifica si hay una secuencia diagonal de cuatro letras iguales."""
    # Diagonal de izquierda a derecha
    if row + 3 < n and col + 3 < n:
        if (matrix[row][col] == matrix[row + 1][col + 1] ==
            matrix[row + 2][col + 2] == matrix[row + 3][col + 3]):
            return True

    # Diagonal de derecha a izquierda
    if row + 3 < n and col - 3 >= 0:
        if (matrix[row][col] == matrix[row + 1][col - 1] ==
            matrix[row + 2][col - 2] == matrix[row + 3][col - 3]):
            return True

    return False

###PRUEBA PARA VERIFICAR SI ES MUTANTE###

dna = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
print(is_mutant(dna))  
