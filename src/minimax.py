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
    else:
        for i in range(24):
            if juego.tablero[i] == jugador:
                # Vuelo
                if juego.en_tablero[jugador] == 3:
                    for j in range(24):
                        if juego.tablero[j] == 0:
                            movimientos.append((i, j))
                else:
                    for j in juego.movimientos_validos.get(i, []):
                        if juego.tablero[j] == 0:
                            movimientos.append((i, j))
    return movimientos

def minimax(juego, profundidad: int, maximizando: bool,
            alpha: float = float('-inf'), beta: float =float('inf')):
    """
    Implementación del algoritmo Minimax con poda alfa-beta.
    Retorna una tupla (valor, mejor_movimiento)
    """
    if profundidad == 0 or juego.fin_juego:
        # Se evalua desde la perspectiva de IA (negras = -1)
        return evaluar_tablero(juego.tablero, -1), None

    jugador = -1 if maximizando else 1
    movimientos = obtener_movimientos(juego, jugador)
    if not movimientos:
        # No hay movimientos: evaluar estado
        return evaluar_tablero(juego.tablero, jugador), None
    mejor_valor = float('-inf') if maximizando else float('inf')
    mejor_movimiento = None

    for movimiento in movimientos:
        origen, destino = movimiento
        copia = juego.copiar_estado()
        resultado = copia.hacer_movimiento(origen, destino)            
        #  Si se formó molino, simular eliminación para copia
        if resultado == "eliminar":
            # Elegir una eliminación “simple”: primera ficha enemiga no en molino o cualquiera si todas
            rival = -jugador
            posiciones = [i for i, v in enumerate(copia.tablero) if v == rival and not copia._es_molino(i, rival)]
            if not posiciones:
                posiciones = [i for i, v in enumerate(copia.tablero) if v == rival]
            if posiciones:
                copia.eliminar_ficha(posiciones[0], simulacion=True)

        # Recursión
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

