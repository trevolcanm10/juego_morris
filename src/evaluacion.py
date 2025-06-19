MOLINOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (9,10,11), (12,13,14), (15,16,17),
    (18,19,20), (21,22,23),
    (0,9,21), (3,10,18), (6,11,15),
    (1,4,7), (16,19,22), (8,12,17),
    (5,13,20), (2,14,23)
]

POSICIONES_CENTRALES = {1, 4, 7, 10, 13, 16, 19, 22}

def evaluar_tablero(juego, jugador):
    tablero = juego.tablero
    enemigo = -jugador
    valor = 0

    # Diferencia de fichas
    valor += tablero.count(jugador) * 10
    valor -= tablero.count(enemigo) * 15

    # Molinos completos
    for trio in MOLINOS:
        if all(tablero[i] == jugador for i in trio):
            valor += 600
        elif all(tablero[i] == enemigo for i in trio):
            valor -= 150

    # Amenazas de molino
    for trio in MOLINOS:
        valores = [tablero[i] for i in trio]
        if valores.count(jugador) == 2 and valores.count(0) == 1:
            valor += 200
        elif valores.count(enemigo) == 2 and valores.count(0) == 1:
            valor -= 100

    # Movilidad
    valor += contar_movimientos(juego, jugador) * 1
    valor -= contar_movimientos(juego, enemigo) * 3

    # Posiciones centrales
    for i in POSICIONES_CENTRALES:
        if tablero[i] == jugador:
            valor += 3
        elif tablero[i] == enemigo:
            valor -= 3

    # Fichas bloqueadas
    valor -= contar_bloqueadas(juego, jugador) * 3
    valor += contar_bloqueadas(juego, enemigo) * 15

    # Fichas eliminadas
    fichas_eliminadas = 9 - juego.en_tablero[enemigo]
    valor += fichas_eliminadas * 50

    # Bonus por reducir al enemigo a 3 fichas
    if juego.en_tablero[jugador] == 3:
        valor += 100
    if juego.en_tablero[enemigo] <= 3:
        valor += (4 - juego.en_tablero[enemigo]) * 300
        if juego.en_tablero[enemigo] == 3:
            valor += 200
    # Victoria
    if juego.en_tablero[enemigo] <= 2:
        valor += 15000
    elif not juego._tiene_movimientos(enemigo):
        valor += 12000  # Victoria por bloqueo
    return valor

def contar_movimientos(juego, jugador):
    movimientos = 0
    for i in range(24):
        if juego.tablero[i] == jugador:
            if juego.en_tablero[jugador] == 3:
                movimientos += sum(1 for j in range(24) if juego.tablero[j] == 0)
            else:
                movimientos += sum(1 for j in juego.movimientos_validos.get(i, []) if juego.tablero[j] == 0)
    return movimientos

def contar_bloqueadas(juego, jugador):
    bloqueadas = 0
    for i in range(24):
        if juego.tablero[i] == jugador:
            if juego.en_tablero[jugador] > 3:
                if all(juego.tablero[j] != 0 for j in juego.movimientos_validos.get(i, [])):
                    bloqueadas += 1
    return bloqueadas