def numero_mas_frecuente(lista):
    max_repeticiones = 0
    resultado = None

    for numero in set(lista):
        repeticiones = lista.count(numero)
        if repeticiones > max_repeticiones or (repeticiones == max_repeticiones and (resultado is None or numero < resultado)):
            max_repeticiones = repeticiones
            resultado = numero

    return resultado
