import copy
#Codifcación Denilson
class MorrisGame:
    def __init__(self):
        # Representación del tablero: 24 puntos (0 a 23) conectados como en el Morris tradicional.
        # Cada punto puede estar: 0 (vacío), 1 (jugador), -1 (IA).
        self.tablero = [0] * 24
        self.turno_jugador = 1  # 1: humano, -1: IA
        self.fase = "colocacion"  # "colocacion" o "movimiento"
        self.fichas_jugador = 6  # Fichas restantes por colocar
        self.fichas_ia = 6 
        self.fichas_en_tablero = {1: 0, -1: 0}
        self.fin_juego = False
        self.movimientos_validos = self._generar_conexiones()  # Conexiones entre puntos

    def _generar_conexiones(self):
        """Define las conexiones válidas entre puntos para movimientos (grafo del tablero)."""
        return {
            0: [1, 9], 1: [0, 2, 4], 2: [1, 14],  # Anillo exterior
            3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13],  # Líneas centrales
            6: [7, 11], 7: [4, 6, 8], 8: [7, 12],  # Anillo interior
            9: [0, 10, 21], 10: [3, 9, 11, 18], 11: [6, 10, 15],
            12: [8, 13, 17], 13: [5, 12, 14, 20], 14: [2, 13, 23],
            15: [11, 16], 16: [15, 17, 19], 17: [12, 16],
            18: [10, 19], 19: [16, 18, 20, 22], 20: [13, 19],
            21: [9, 22], 22: [19, 21, 23], 23: [14, 22]
        }

    
    def hacer_movimiento(self, origen, destino=None):
        if self.fin_juego:
            return False

        jugador = self.turno_jugador

        if self.fase == "colocacion":
            if self.tablero[origen] == 0:
                if (jugador == 1 and self.fichas_jugador == 0) or (jugador == -1 and self.fichas_ia == 0):
                    return False  # No debe colocar más fichas
                
                self.tablero[origen] = jugador
                if jugador == 1:
                    self.fichas_jugador -= 1
                else:
                    self.fichas_ia -= 1
                self.fichas_en_tablero[jugador] += 1

                if self._verificar_molino(origen):
                    return "eliminar"
                
                # Solo cambiar a fase de movimiento si ya no quedan fichas por colocar para ambos
                if self.fichas_jugador == 0 and self.fichas_ia == 0:
                    self.fase = "movimiento"

                self._cambiar_turno()
                return True

        elif self.fase == "movimiento":
            if self.tablero[origen] == jugador:
                if self._puede_volar(jugador) or destino in self.movimientos_validos[origen]:
                    if self.tablero[destino] == 0:
                        self.tablero[origen] = 0
                        self.tablero[destino] = jugador

                        if self._verificar_molino(destino):
                            return "eliminar"
                        
                        self._cambiar_turno()
                        return True
        return False

    
    def eliminar_ficha(self, punto):
        rival = -self.turno_jugador
        if self.tablero[punto] == rival:
            if not self._es_molino(punto, rival) or self._todas_en_molino(rival):
                self.tablero[punto] = 0
                self.fichas_en_tablero[rival] -= 1
                if self.fichas_en_tablero[rival] <= 2 or not self._tiene_movimientos(rival):
                    self.fin_juego = True
                return True
        return False

    def _puede_volar(self, jugador):
        return self.fichas_en_tablero[jugador] == 3

    def _verificar_molino(self, punto):
        jugador = self.turno_jugador
        for molino in self._molinos_por_punto(punto):
            if all(self.tablero[pos] == jugador for pos in molino):
                return True
        return False

    def _es_molino(self, punto, jugador):
        for molino in self._molinos_por_punto(punto):
            if all(self.tablero[pos] == jugador for pos in molino):
                return True
        return False
    

    #Todas se encuentran en molino
    def _todas_en_molino(self, jugador):
        return all(
            self._es_molino(i, jugador) 
            for i, val in enumerate(self.tablero) if val == jugador
        )

    def _tiene_movimientos(self, jugador):
        for i, val in enumerate(self.tablero):
            if val == jugador:
                if self._puede_volar(jugador):
                    if any(self.tablero[d] == 0 for d in range(24)):
                        return True
                for dest in self.movimientos_validos[i]:
                    if self.tablero[dest] == 0:
                        return True
        return False

    def _molinos_por_punto(self, punto):
        """Devuelve las posibles combinaciones de molino en las que participa el punto."""
        molinos = [
            # Anillo exterior
            [0, 1, 2], [3, 4, 5], [5, 6, 7],  # Horizontales
            [0, 3, 5], [2, 4, 7], [1, 4, 6],  # Verticales

            # Anillo medio
            [8, 9, 10], [11, 12, 13], [13, 14, 15],
            [8, 11, 13], [10, 12, 15], [9, 12, 14],

            # Anillo interior
            [16, 17, 18], [19, 20, 21], [21, 22, 23],
            [16, 19, 21], [18, 20, 23], [17, 20, 22],

            # Conexiones cruzadas entre anillos
            [0, 8, 16], [1, 9, 17], [2, 10, 18],
            [3, 11, 19], [4, 12, 20], [5, 13, 21],
            [6, 14, 22], [7, 15, 23]
        ]

        return [m for m in molinos if punto in m]

    def _cambiar_turno(self):
        self.turno_jugador *= -1

    def estado_actual(self):
        return {
            'tablero': self.tablero.copy(),
            'turno': self.turno_jugador,
            'fase': self.fase,
            'fichas_jugador': self.fichas_jugador,
            'fichas_ia': self.fichas_ia,
            'fichas_en_tablero': self.fichas_en_tablero.copy(),
            'fin': self.fin_juego
        }
