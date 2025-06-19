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
    valor += tablero.count(jugador) * 15
    valor -= tablero.count(enemigo) * 12

    # Molinos completos
    for trio in MOLINOS:
        if all(tablero[i] == jugador for i in trio):
            valor += 500
        elif all(tablero[i] == enemigo for i in trio):
            valor -= 100

    # Amenazas de molino
    for trio in MOLINOS:
        valores = [tablero[i] for i in trio]
        if valores.count(jugador) == 2 and valores.count(0) == 1:
            valor += 150
        elif valores.count(enemigo) == 2 and valores.count(0) == 1:
            valor -= 75
        if valores.count(jugador) == 1 and valores.count(0) == 2:
            valor += 20

    # Movilidad
    valor += contar_movimientos(juego, jugador) * 2
    valor -= contar_movimientos(juego, enemigo) * 2

    # Posiciones centrales
    for i in POSICIONES_CENTRALES:
        if tablero[i] == jugador:
            valor += 5
        elif tablero[i] == enemigo:
            valor -= 5

    # Fichas bloqueadas
    valor -= contar_bloqueadas(juego, jugador) * 5
    valor += contar_bloqueadas(juego, enemigo) * 10

    # Fichas eliminadas
    fichas_eliminadas = 9 - juego.en_tablero[enemigo]
    valor += fichas_eliminadas * 50

    # Modo vuelo
    if juego.en_tablero[jugador] == 3:
        valor += 50
    if juego.en_tablero[enemigo] == 3:
        valor += 100

    # Victoria
    if juego.en_tablero[enemigo] <= 2:
        valor += 10000

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