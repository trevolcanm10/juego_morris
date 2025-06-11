# evaluacion.py

def evaluar_tablero(tablero, jugador):
    """
    Evalúa el estado del tablero desde la perspectiva del jugador.
    +10 por cada ficha propia
    -10 por cada ficha enemiga
    """
    valor = 0
    valor += tablero.count(jugador) * 10
    valor -= tablero.count(-jugador) * 10

    # Puedes agregar más reglas heurísticas si deseas.
    return valor
