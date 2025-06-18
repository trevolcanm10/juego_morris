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
            alpha: float = float('-inf'), beta: float =float('inf'), nivel:int = 0):
    """
    Implementación del algoritmo Minimax con poda alfa-beta.
    Retorna una tupla (valor, mejor_movimiento)
    """
    if profundidad == 0 or juego.fin_juego:
        # Se evalua desde la perspectiva de IA (negras = -1)
        return evaluar_tablero(juego,-1), None

    jugador = -1 if maximizando else 1
    movimientos = obtener_movimientos(juego, jugador)
    if not movimientos:
        # No hay movimientos: evaluar estado
        return evaluar_tablero(juego, jugador), None
    
    evaluaciones=[]
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
            if maximizando:
                valor_bonus = 150
            else:
                valor_bonus = -150

        # Recursión
        valor, _ = minimax(copia, profundidad - 1, not maximizando, alpha, beta, nivel + 1)
        if resultado == "eliminar":
            valor += valor_bonus
        evaluaciones.append((valor,movimiento))
        
        if maximizando:
            alpha = max(alpha, valor)
        else:
            beta = min(beta, valor)

        if beta <= alpha:
            break  # Poda alfa-beta
    
    if nivel == 0:
        evaluaciones.sort(reverse=maximizando, key=lambda x: x[0])
        rol = "IA" if maximizando else "Jugador"
        print(f"\nTop 4 movimientos para {rol} ({jugador}):")
        for i, (val, mov) in enumerate(evaluaciones[:4]):
            print(f"{i+1}. Movimiento: {mov}, Valor: {val}")
    # Elegir mejor movimiento según si estamos maximizando o minimizando
    mejor_valor, mejor_movimiento = (
        max(evaluaciones, key=lambda x: x[0]) if maximizando else min(evaluaciones, key=lambda x: x[0])
    )
            
    return mejor_valor, mejor_movimiento

