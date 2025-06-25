import copy
from evaluacion import evaluar_tablero
from logica_juego import MorrisGame

def obtener_movimientos_ordenados(juego, jugador):
    """Obtiene movimientos ordenados por prioridad para mejorar la poda alfa-beta"""
    movimientos = []
    
    if juego.fase == "colocacion":
        # En fase de colocación, prioritizar movimientos que pueden formar molinos
        movimientos_prioritarios = []
        movimientos_normales = []
        
        for i in range(24):
            if juego.tablero[i] == 0:
                # Simular colocación para verificar si forma molino
                copia = juego.copiar_estado()
                copia.tablero[i] = jugador
                if copia._verificar_molino_manual(i, jugador):
                    movimientos_prioritarios.append((i, None))
                else:
                    # También prioritizar movimientos que bloquean molinos enemigos
                    rival = -jugador
                    copia_rival = juego.copiar_estado()
                    copia_rival.tablero[i] = rival
                    if copia_rival._verificar_molino_manual(i, rival):
                        movimientos_prioritarios.append((i, None))
                    else:
                        movimientos_normales.append((i, None))
        
        movimientos = movimientos_prioritarios + movimientos_normales
    else:
        # En fase de movimiento, ordenar por potencial de formar molinos
        movimientos_prioritarios = []
        movimientos_normales = []
        
        for i in range(24):
            if juego.tablero[i] == jugador:
                destinos = []
                if juego.en_tablero[jugador] == 3:
                    destinos = [j for j in range(24) if juego.tablero[j] == 0]
                else:
                    destinos = [j for j in juego.movimientos_validos.get(i, []) if juego.tablero[j] == 0]
                
                for destino in destinos:
                    # Verificar si este movimiento forma un molino
                    copia = juego.copiar_estado()
                    copia.tablero[i] = 0
                    copia.tablero[destino] = jugador
                    
                    if copia._verificar_molino_manual(destino, jugador):
                        movimientos_prioritarios.append((i, destino))
                    else:
                        movimientos_normales.append((i, destino))
        
        movimientos = movimientos_prioritarios + movimientos_normales
    
    return movimientos

def minimax(juego, profundidad: int, maximizando: bool, jugador_max: int,
            alpha: float = float('-inf'), beta: float = float('inf'), nivel: int = 0):
    
    # Condición de parada mejorada
    if profundidad == 0 or juego.fin_juego:
        return evaluar_tablero(juego, jugador_max), None

    jugador_actual = juego.turno
    movimientos = obtener_movimientos_ordenados(juego, jugador_actual)
    
    if not movimientos:
        # Si no hay movimientos, evaluar como posición terminal
        return evaluar_tablero(juego, jugador_max), None

    mejor_valor = float('-inf') if maximizando else float('inf')
    mejor_movimiento = None
    
    for movimiento in movimientos:
        origen, destino = movimiento
        copia = juego.copiar_estado()
        resultado = copia.hacer_movimiento(origen, destino)

        # Manejo mejorado de eliminación de fichas
        if resultado == "eliminar":
            rival = -jugador_actual
            mejor_eliminacion = elegir_mejor_eliminacion(copia, rival, jugador_max, maximizando)
            if mejor_eliminacion is not None:
                copia.eliminar_ficha(mejor_eliminacion, simulacion=True)

        # Llamada recursiva
        valor, _ = minimax(copia, profundidad - 1, not maximizando, jugador_max, alpha, beta, nivel + 1)
        
        # Actualizar mejor movimiento
        if maximizando:
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento
            alpha = max(alpha, valor)
        else:
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento
            beta = min(beta, valor)
        
        # Poda alfa-beta
        if beta <= alpha:
            break

    return mejor_valor, mejor_movimiento

def elegir_mejor_eliminacion(juego, rival, jugador_max, maximizando):
    """Elige la mejor ficha rival para eliminar usando evaluación estratégica"""
    from evaluacion import evaluar_eliminacion
    
    fichas_eliminables = juego.obtener_fichas_eliminables(rival)
    
    if not fichas_eliminables:
        return None
    
    if len(fichas_eliminables) == 1:
        return fichas_eliminables[0]
    
    # Evaluar cada posible eliminación
    mejor_valor = float('-inf') if maximizando else float('inf')
    mejor_posicion = fichas_eliminables[0]
    
    for pos in fichas_eliminables:
        valor = evaluar_eliminacion(juego, pos, jugador_max)
        
        if maximizando and valor > mejor_valor:
            mejor_valor = valor
            mejor_posicion = pos
        elif not maximizando and valor < mejor_valor:
            mejor_valor = valor
            mejor_posicion = pos
    
    return mejor_posicion

def minimax_eliminacion(juego, jugador_max, profundidad_max=2):
    """Minimax específico para decidir eliminaciones con profundidad limitada"""
    from evaluacion import evaluar_eliminacion
    
    rival = -juego.turno
    fichas_eliminables = juego.obtener_fichas_eliminables(rival)
    
    if not fichas_eliminables:
        return None
    
    if len(fichas_eliminables) == 1:
        return fichas_eliminables[0]
    
    mejor_valor = float('-inf')
    mejor_posicion = fichas_eliminables[0]
    
    for pos in fichas_eliminables:
        # Simular eliminación
        copia = juego.copiar_estado()
        if copia.eliminar_ficha(pos, simulacion=True):
            # Evaluar posición resultante con minimax limitado
            valor, _ = minimax(copia, profundidad_max, False, jugador_max)
            
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_posicion = pos
    
    return mejor_posicion