MOLINOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (9,10,11), (12,13,14), (15,16,17),
    (18,19,20), (21,22,23),
    (0,9,21), (3,10,18), (6,11,15),
    (1,4,7), (16,19,22), (8,12,17),
    (5,13,20), (2,14,23)
]

def evaluar_tablero(juego, jugador):
    tablero = juego.tablero
    enemigo = -jugador
    valor = 0

    # CONDICIONES DE VICTORIA/DERROTA 
    
    # Victoria inmediata: enemigo tiene ≤ 2 fichas en fase de movimiento
    if juego.fase == "movimiento" and juego.en_tablero[enemigo] <= 2:
        return 100000 if jugador == juego.turno else -100000
    
    # Derrota inmediata: jugador tiene ≤ 2 fichas en fase de movimiento
    if juego.fase == "movimiento" and juego.en_tablero[jugador] <= 2:
        return -100000 if jugador == juego.turno else 100000
    
    # Sin movimientos válidos = derrota
    if juego.fase == "movimiento":
        if not _tiene_movimientos_validos(juego, enemigo):
            return 50000
        if not _tiene_movimientos_validos(juego, jugador):
            return -50000

    # === EVALUACIÓN DE MOLINOS ===
    molinos_propios, molinos_enemigos = _evaluar_molinos(tablero, jugador, enemigo)
    valor += molinos_propios * 1500  # Aumentado el valor de los molinos
    valor -= molinos_enemigos * 1500

    # === AMENAZAS DE MOLINO INMEDIATAS ===
    amenazas_propias, amenazas_enemigas = _evaluar_amenazas_inmediatas(tablero, jugador, enemigo)
    valor += amenazas_propias * 400   # Aumentado el valor de las amenazas
    valor -= amenazas_enemigas * 500  # Las amenazas enemigas son muy peligrosas

    # === EVALUACIÓN DE POTENCIAL DE MOLINO ===
    potencial_propio, potencial_enemigo = _evaluar_potencial_molino(tablero, jugador, enemigo)
    valor += potencial_propio * 50
    valor -= potencial_enemigo * 60

    # === DIFERENCIA DE FICHAS ===
    diferencia_fichas = juego.en_tablero[jugador] - juego.en_tablero[enemigo]
    valor += diferencia_fichas * 120

    # === MOVILIDAD ===
    if juego.fase == "movimiento":
        movilidad_propia = _contar_movimientos_simples(juego, jugador)
        movilidad_enemiga = _contar_movimientos_simples(juego, enemigo)
        valor += (movilidad_propia - movilidad_enemiga) * 8

    # === CONTROL DE POSICIONES CLAVE ===
    if juego.fase == "colocacion":
        control_clave = _evaluar_posiciones_clave(tablero, jugador, enemigo)
        valor += control_clave * 15

    # === PENALIZACIÓN POR FICHAS BLOQUEADAS ===
    if juego.fase == "movimiento":
        fichas_bloqueadas_propias = _contar_fichas_bloqueadas(juego, jugador)
        fichas_bloqueadas_enemigas = _contar_fichas_bloqueadas(juego, enemigo)
        valor -= fichas_bloqueadas_propias * 25
        valor += fichas_bloqueadas_enemigas * 20

    return valor

def _evaluar_molinos(tablero, jugador, enemigo):
    """Evalúa molinos formados y devuelve la cuenta para cada jugador"""
    molinos_propios = 0
    molinos_enemigos = 0
    
    for trio in MOLINOS:
        if all(tablero[i] == jugador for i in trio):
            molinos_propios += 1
        elif all(tablero[i] == enemigo for i in trio):
            molinos_enemigos += 1
    
    return molinos_propios, molinos_enemigos

def _evaluar_amenazas_inmediatas(tablero, jugador, enemigo):
    """Evalúa amenazas de molino inmediatas (2 fichas + 1 vacía)"""
    amenazas_propias = 0
    amenazas_enemigas = 0
    
    for trio in MOLINOS:
        valores = [tablero[i] for i in trio]
        
        if valores.count(jugador) == 2 and valores.count(0) == 1:
            amenazas_propias += 1
        elif valores.count(enemigo) == 2 and valores.count(0) == 1:
            amenazas_enemigas += 1
    
    return amenazas_propias, amenazas_enemigas

def _evaluar_potencial_molino(tablero, jugador, enemigo):
    """Evalúa el potencial de formar molinos (1 ficha + 2 vacías)"""
    potencial_propio = 0
    potencial_enemigo = 0
    
    for trio in MOLINOS:
        valores = [tablero[i] for i in trio]
        
        if valores.count(jugador) == 1 and valores.count(0) == 2:
            potencial_propio += 1
        elif valores.count(enemigo) == 1 and valores.count(0) == 2:
            potencial_enemigo += 1
    
    return potencial_propio, potencial_enemigo

def _evaluar_posiciones_clave(tablero, jugador, enemigo):
    """Evalúa el control de posiciones estratégicamente importantes"""
    # Posiciones que participan en más molinos son más valiosas
    valor_posiciones = {
        1: 4, 4: 4, 7: 4, 10: 4, 13: 4, 16: 4, 19: 4, 22: 4,  # Posiciones que participan en 4 molinos
        3: 3, 5: 3, 9: 3, 11: 3, 12: 3, 14: 3, 18: 3, 20: 3,  # Posiciones que participan en 3 molinos
        0: 2, 2: 2, 6: 2, 8: 2, 15: 2, 17: 2, 21: 2, 23: 2   # Esquinas (2 molinos)
    }
    
    control = 0
    for pos, valor in valor_posiciones.items():
        if tablero[pos] == jugador:
            control += valor
        elif tablero[pos] == enemigo:
            control -= valor
    
    return control

def _contar_fichas_bloqueadas(juego, jugador):
    """Cuenta fichas que no pueden moverse"""
    fichas_bloqueadas = 0
    
    for i in range(24):
        if juego.tablero[i] == jugador:
            # Si el jugador tiene 3 fichas, puede volar
            if juego.en_tablero[jugador] == 3:
                continue
            
            # Verificar si tiene movimientos válidos
            tiene_movimiento = False
            for vecino in juego.movimientos_validos.get(i, []):
                if juego.tablero[vecino] == 0:
                    tiene_movimiento = True
                    break
            
            if not tiene_movimiento:
                fichas_bloqueadas += 1
    
    return fichas_bloqueadas

def _tiene_movimientos_validos(juego, jugador):
    """Verifica si el jugador tiene al menos un movimiento válido."""
    for i in range(24):
        if juego.tablero[i] == jugador:
            # Modo vuelo: puede ir a cualquier casilla vacía
            if juego.en_tablero[jugador] == 3:
                if any(juego.tablero[j] == 0 for j in range(24)):
                    return True
            else:
                # Movimiento normal: verificar adyacentes
                for j in juego.movimientos_validos.get(i, []):
                    if juego.tablero[j] == 0:
                        return True
    return False

def _contar_movimientos_simples(juego, jugador):
    """Cuenta movimientos válidos de forma simple."""
    movimientos = 0
    for i in range(24):
        if juego.tablero[i] == jugador:
            if juego.en_tablero[jugador] == 3:
                # Modo vuelo
                movimientos += sum(1 for j in range(24) if juego.tablero[j] == 0)
            else:
                # Movimiento normal
                movimientos += sum(1 for j in juego.movimientos_validos.get(i, []) 
                                 if juego.tablero[j] == 0)
    return movimientos

def evaluar_eliminacion(juego, posicion_eliminar, jugador_max):
    """Evalúa específicamente el valor de eliminar una ficha en la posición dada"""
    copia = juego.copiar_estado()
    jugador_eliminado = copia.tablero[posicion_eliminar]
    
    if not copia.eliminar_ficha(posicion_eliminar, simulacion=True):
        return float('-inf')  # Eliminación inválida
    
    valor_base = evaluar_tablero(copia, jugador_max)
    bonus = 0
    
    # BONUS: Interrupción de amenazas de molino
    amenazas_interrumpidas = _contar_amenazas_interrumpidas(juego, copia, posicion_eliminar, jugador_eliminado)
    bonus += amenazas_interrumpidas * 800
    
    # BONUS: Reducción de movilidad
    movilidad_antes = _contar_movimientos_simples(juego, jugador_eliminado)
    movilidad_despues = _contar_movimientos_simples(copia, jugador_eliminado)
    reduccion_movilidad = movilidad_antes - movilidad_despues
    bonus += reduccion_movilidad * 15
    
    # BONUS: Valor posicional de la ficha eliminada
    valor_posiciones = {
        1: 50, 4: 50, 7: 50, 10: 50, 13: 50, 16: 50, 19: 50, 22: 50,  # Centros de lados
        3: 30, 5: 30, 9: 30, 11: 30, 12: 30, 14: 30, 18: 30, 20: 30,  # Posiciones intermedias
        0: 20, 2: 20, 6: 20, 8: 20, 15: 20, 17: 20, 21: 20, 23: 20   # Esquinas
    }
    bonus += valor_posiciones.get(posicion_eliminar, 10)
    
    # PENALTY: Si la ficha estaba en un molino (era la única opción)
    if _estaba_en_molino_antes(juego, posicion_eliminar, jugador_eliminado):
        bonus -= 200
    
    return valor_base + bonus

def _contar_amenazas_interrumpidas(juego_antes, juego_despues, posicion, jugador):
    """Cuenta cuántas amenazas de molino se interrumpieron al eliminar la ficha"""
    amenazas_antes = 0
    amenazas_despues = 0
    
    # Contar amenazas antes
    for trio in MOLINOS:
        if posicion in trio:
            valores = [juego_antes.tablero[i] for i in trio]
            if valores.count(jugador) == 2 and valores.count(0) == 1:
                amenazas_antes += 1
    
    # Contar amenazas después
    for trio in MOLINOS:
        if posicion in trio:
            valores = [juego_despues.tablero[i] for i in trio]
            if valores.count(jugador) == 2 and valores.count(0) == 1:
                amenazas_despues += 1
    
    return amenazas_antes - amenazas_despues

def _estaba_en_molino_antes(juego, posicion, jugador):
    """Verifica si la ficha eliminada estaba en un molino"""
    for trio in MOLINOS:
        if posicion in trio:
            if all(juego.tablero[i] == jugador for i in trio):
                return True
    return False