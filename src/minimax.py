import copy
from evaluacion import evaluar_tablero

def obtener_movimientos(juego, jugador):
    movimientos = []
    if juego.fase == "colocacion":
        for i in range(24):
            if juego.tablero[i] == 0:
                movimientos.append((i, None))
    else:
        for i in range(24):
            if juego.tablero[i] == jugador:
                if juego.en_tablero[jugador] == 3:
                    for j in range(24):
                        if juego.tablero[j] == 0:
                            movimientos.append((i, j))
                else:
                    for j in juego.movimientos_validos.get(i, []):
                        if juego.tablero[j] == 0:
                            movimientos.append((i, j))
    return movimientos

def minimax(juego, profundidad: int, maximizando: bool, jugador_max: int,
            alpha: float = float('-inf'), beta: float = float('inf'), nivel: int = 0):
    if profundidad == 0 or juego.fin_juego:
        return evaluar_tablero(juego, jugador_max), None

    jugador_actual = juego.turno
    movimientos = obtener_movimientos(juego, jugador_actual)
    if not movimientos:
        return evaluar_tablero(juego, jugador_max), None

    evaluaciones = []
    for movimiento in movimientos:
        origen, destino = movimiento
        copia = juego.copiar_estado()
        resultado = copia.hacer_movimiento(origen, destino)

        if resultado == "eliminar":
            rival = -jugador_actual
            posiciones = [i for i, v in enumerate(copia.tablero) if v == rival and not copia._es_molino(i, rival)]
            if not posiciones:
                posiciones = [i for i, v in enumerate(copia.tablero) if v == rival]
            if posiciones:
                copia.eliminar_ficha(posiciones[0], simulacion=True)

        valor, _ = minimax(copia, profundidad - 1, not maximizando, jugador_max, alpha, beta, nivel + 1)
        evaluaciones.append((valor, movimiento))

        if maximizando:
            alpha = max(alpha, valor)
            if beta <= alpha:
                break
        else:
            beta = min(beta, valor)
            if beta <= alpha:
                break

    if not evaluaciones:
        return evaluar_tablero(juego, jugador_max), None

    if maximizando:
        mejor_valor, mejor_movimiento = max(evaluaciones, key=lambda x: x[0])
    else:
        mejor_valor, mejor_movimiento = min(evaluaciones, key=lambda x: x[0])

    return mejor_valor, mejor_movimiento