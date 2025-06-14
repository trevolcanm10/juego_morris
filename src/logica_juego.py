from minimax import minimax
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
        conexiones = {
            0: [1, 9],1: [0, 2, 4],2: [1, 14],
            3: [4, 10],4: [1, 3, 5, 7], 5: [4, 13],
            6: [7, 11],7: [4, 6, 8],8: [7, 12],
            9: [0, 10, 21], 10: [3, 9, 11, 18],11: [6, 10, 15],
            12: [8, 13, 17],13: [5, 12, 14, 20],14: [2, 13, 23],
            15: [11, 16],   16: [15, 17, 19],  17: [12, 16],
            18: [10, 19],   19: [16, 18, 20, 22],20: [13, 19],
            21: [9, 22],    22: [19, 21, 23],  23: [14, 22]
        }

        # Asegurar bidireccionalidad (opcional, pero correcto)
        conexiones_bidireccionales = {}
        for origen, destinos in conexiones.items():
            if origen not in conexiones_bidireccionales:
                conexiones_bidireccionales[origen] = []
            for destino in destinos:
                conexiones_bidireccionales[origen].append(destino)
                if destino not in conexiones_bidireccionales:
                    conexiones_bidireccionales[destino] = []
                if origen not in conexiones_bidireccionales[destino]:
                    conexiones_bidireccionales[destino].append(origen)

        return conexiones_bidireccionales

    
    def hacer_movimiento(self, origen, destino=None,simulado=False):
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
                
                if not simulado:
                    self._cambiar_turno(simulado=simulado)
                return True

        elif self.fase == "movimiento":
            if self.tablero[origen] == jugador:
                if self._puede_volar(jugador) or destino in self.movimientos_validos[origen]:
                    if self.tablero[destino] == 0:
                        self.tablero[origen] = 0
                        self.tablero[destino] = jugador

                        if self._verificar_molino(destino):
                            return "eliminar"
                        
                        self._cambiar_turno(simulado=simulado)
                        return True
        return False

    
    def eliminar_ficha(self, punto):
        rival = -self.turno_jugador
        if self.tablero[punto] == rival:
            if not self._es_molino(punto, rival) or self._todas_en_molino(rival):
                self.tablero[punto] = 0
                self.fichas_en_tablero[rival] -= 1
                if self.fase == "movimiento" and (self.fichas_en_tablero[rival] <= 2 or not self._tiene_movimientos(rival)):
                    self.fin_juego = True
                    self.ganador = self.turno_jugador
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
            # Horizontales
            [0, 1, 2],     [3, 4, 5],     [6, 7, 8],
            [9, 10, 11],   [12, 13, 14], [15, 16, 17],
            [18, 19, 20],  [21, 22, 23],

            # Verticales
            [0, 9, 21],    [3, 10, 18],    
            
            
            [6, 11, 15],
            [1, 4, 7],     [16, 19, 22],
            [8, 12, 17],   [5, 13, 20],   [2, 14, 23]
        ]

        return [m for m in molinos if punto in m]

    def _cambiar_turno(self, simulado=False):
        self.turno_jugador *= -1
        # turno de la IA
        if self.turno_jugador == -1 and not self.fin_juego and not simulado:
            _, mejor_mov = minimax(self, profundidad=3, maximizando=True)
            if mejor_mov:
                origen, destino = mejor_mov
                resultado = self.hacer_movimiento(origen, destino)
                if resultado == "eliminar":
                    self.eliminar_ficha_contraria(-1)
                       



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


    def simular_movimiento(juego_original, origen, destino):
        copia = copy.deepcopy(juego_original)
        copia.hacer_movimiento(origen, destino, simulado=True)
        return copia

    def copiar_estado(self):
        nuevo = MorrisGame()
        nuevo.tablero = self.tablero[:]  # Copia del tablero
        nuevo.turno_jugador = self.turno_jugador
        nuevo.fichas_jugador = self.fichas_jugador
        nuevo.fichas_ia = self.fichas_ia
        nuevo.fichas_en_tablero = self.fichas_en_tablero.copy()
        nuevo.fase = self.fase
        nuevo.movimientos_validos = {k: v[:] for k, v in self.movimientos_validos.items()}
        nuevo.fin_juego = self.fin_juego
        return nuevo

    def eliminar_ficha_contraria(self, jugador):
        if self.fin_juego:
            return

        # Encuentra las posiciones del oponente
        rival = -jugador
        posiciones_contrarias = [i for i, val in enumerate(self.tablero) if val == rival]

        # Intenta eliminar una que no esté en molino
        ficha_a_eliminar = next(
            (pos for pos in posiciones_contrarias if not self._es_molino(pos, rival)),
            None
        )

        # Si todas están en molino, elimina cualquiera
        if ficha_a_eliminar is None and posiciones_contrarias:
            ficha_a_eliminar = posiciones_contrarias[0]

        if ficha_a_eliminar is not None:
            self.tablero[ficha_a_eliminar] = 0
            self.fichas_en_tablero[rival] -= 1
            print(f"Jugador {jugador} eliminó ficha del jugador {rival} en posición {ficha_a_eliminar}")



            if self.fase == "movimiento" and self.fichas_en_tablero[rival] <= 2:
                self.fin_juego = True
                self.ganador = jugador
                print(f"¡Jugador {jugador} gana! El jugador {rival} tiene solo 2 fichas.")
                return
        # Solo cambiar el turno si el juego no terminó
        if not self.fin_juego:
            self.turno_jugador *= -1

            # Si el nuevo turno es de la IA, la IA debe jugar
            if self.turno_jugador == -1:
                _, mejor_mov = minimax(self, profundidad=3, maximizando=True)
                if mejor_mov:
                    origen, destino = mejor_mov
                    resultado = self.hacer_movimiento(origen, destino)
                    if resultado == "eliminar":
                        self.eliminar_ficha_contraria(-1)
