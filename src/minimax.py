import copy

def minimax(tablero, profundidad, es_maximizador, alpha, beta):
    if profundidad == 0 or evaluar_fin_juego(tablero):
        return evaluar_tablero(tablero), None

    if es_maximizador:
        max_eval = float('-inf')
        mejor_movimiento = None
        for (origen, destino) in generar_movimientos(tablero, -1):  # IA
            nuevo_tablero = simular_movimiento(tablero, origen, destino, -1)
            evaluacion, _ = minimax(nuevo_tablero, profundidad - 1, False, alpha, beta)
            if evaluacion > max_eval:
                max_eval = evaluacion
                mejor_movimiento = (origen, destino)
            alpha = max(alpha, evaluacion)
            if beta <= alpha:
                break
        return max_eval, mejor_movimiento

    else:
        min_eval = float('inf')
        mejor_movimiento = None
        for (origen, destino) in generar_movimientos(tablero, 1):  # Jugador
            nuevo_tablero = simular_movimiento(tablero, origen, destino, 1)
            evaluacion, _ = minimax(nuevo_tablero, profundidad - 1, True, alpha, beta)
            if evaluacion < min_eval:
                min_eval = evaluacion
                mejor_movimiento = (origen, destino)
            beta = min(beta, evaluacion)
            if beta <= alpha:
                break
        return min_eval, mejor_movimiento


# Heurística simple: número de fichas IA - jugador
def evaluar_tablero(tablero):
    return tablero.count(-1) - tablero.count(1)


# Verifica si un jugador tiene 2 o menos fichas
def evaluar_fin_juego(tablero):
    return tablero.count(-1) <= 2 or tablero.count(1) <= 2


# Define las conexiones del tablero (mismo que en logica_juego)
conexiones = {
    0: [1, 9], 1: [0, 2, 4], 2: [1, 14],
    3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13],
    6: [7, 11], 7: [4, 6, 8], 8: [7, 12],
    9: [0, 10, 21], 10: [3, 9, 11, 18], 11: [6, 10, 15],
    12: [8, 13, 17], 13: [5, 12, 14, 20], 14: [2, 13, 23],
    15: [11, 16], 16: [15, 17, 19], 17: [12, 16],
    18: [10, 19], 19: [16, 18, 20, 22], 20: [13, 19],
    21: [9, 22], 22: [19, 21, 23], 23: [14, 22]
}

def generar_movimientos(tablero, jugador):
    movimientos = []
    # Verifica si el jugador está en modo "vuelo"
    if tablero.count(jugador) == 3:
        # Puede moverse a cualquier punto vacío
        for i in range(24):
            if tablero[i] == jugador:
                for j in range(24):
                    if tablero[j] == 0:
                        movimientos.append((i, j))
    else:
        for i in range(24):
            if tablero[i] == jugador:
                for j in conexiones[i]:
                    if tablero[j] == 0:
                        movimientos.append((i, j))
    return movimientos

def simular_movimiento(tablero, origen, destino, jugador):
    nuevo_tablero = tablero.copy()
    nuevo_tablero[origen] = 0
    nuevo_tablero[destino] = jugador
    return nuevo_tablero
