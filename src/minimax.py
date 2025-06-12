# minimax.py
import copy
from evaluacion import evaluar_tablero

def obtener_movimientos(juego, jugador):
    """
    Retorna una lista de movimientos válidos: tuplas (origen, destino)
    Si es fase de colocación, destino será None.
    """
    movimientos = []

    if juego.fase == "colocacion":
        for i in range(24):
            if juego.tablero[i] == 0:
                movimientos.append((i, None))  # Colocar ficha
    elif juego.fase == "movimiento":
        for i in range(24):
            if juego.tablero[i] == jugador:
                if juego._puede_volar(jugador):
                    for j in range(24):
                        if juego.tablero[j] == 0:
                            movimientos.append((i, j))
                else:
                    for j in juego.movimientos_validos[i]:
                        if juego.tablero[j] == 0:
                            movimientos.append((i, j))
    return movimientos

def minimax(juego, profundidad, maximizando, alpha=float('-inf'), beta=float('inf')):
    """
    Implementación del algoritmo Minimax con poda alfa-beta.
    Retorna una tupla (valor, mejor_movimiento)
    """
    if profundidad == 0 or juego.fin_juego:
        return evaluar_tablero(juego.tablero, -1), None  # La IA es el jugador -1

    jugador = -1 if maximizando else 1
    posibles = obtener_movimientos(juego, jugador)

    if not posibles:
        return evaluar_tablero(juego.tablero, jugador), None

    mejor_valor = float('-inf') if maximizando else float('inf')
    mejor_movimiento = None

    for movimiento in posibles:
        copia = copy.deepcopy(juego)
        origen, destino = movimiento
        resultado = copia.hacer_movimiento(origen, destino,simulado=True)            
       #Simulación de eliminación si se forma un molino
        if resultado == "eliminar":
            posibles_eliminaciones = [
                i for i in range(24)
                if copia.tablero[i] == -jugador and not copia._es_molino(i, -jugador)
            ]
            if not posibles_eliminaciones:
                # Si todas son molinos, se puede eliminar cualquiera
                posibles_eliminaciones = [
                    i for i in range(24) if copia.tablero[i] == -jugador
                ]
            if posibles_eliminaciones:
                copia.tablero[posibles_eliminaciones[0]] = 0
                copia.fichas_en_tablero[-jugador] -= 1

        valor, _ = minimax(copia, profundidad - 1, not maximizando, alpha, beta)

        if maximizando:
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento
            alpha = max(alpha, mejor_valor)
        else:
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento
            beta = min(beta, mejor_valor)

        if beta <= alpha:
            break  # Poda alfa-beta

    return mejor_valor, mejor_movimiento

