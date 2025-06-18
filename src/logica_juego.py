import copy

#Codifcación Denilson
class MorrisGame:
    def __init__(self):
        # Representación del tablero: 24 puntos (0 a 23) conectados como en el Morris tradicional.
        # Cada punto puede estar: 0 (vacío), 1 (blancas), -1 (negras).
        self.tablero = [0] * 24
        self.turno = 1  # (Codificacion Wilson) 1: Fichas Blancas, -1: Fichas Negras // Así es más fácil para separar cuando el jugador humano sea las blancas o negras
        self.fase = "colocacion"  # "colocacion" o "movimiento"
        self.por_colocar = {1:6, -1:6}
        self.en_tablero = {1:0, -1:0}
        self.fin_juego = False
        self.ganador = None
        self.movimientos_validos = self._generar_conexiones()  # Conexiones entre puntos
        self.control = {1: 'humano', -1: 'IA'}
        self.turnos_sin_eliminar = 0

    def set_control(self, control_blancas: str, control_negras: str):
        assert control_blancas in ('humano', 'IA')
        assert control_negras in ('humano', 'IA')
        self.control[1] = control_blancas
        self.control[-1] = control_negras

    def es_turno_IA(self) -> bool:
        return self.control.get(self.turno) == 'IA'

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

    
    def hacer_movimiento(self, origen: int, destino: int = None) -> str or bool:
        if self.fin_juego:
            return False

        jugador = self.turno

        if self.fase == "colocacion":
            if origen < 0 or origen >= 24:
                return False
            if self.tablero[origen] != 0:
                return False
            if self.por_colocar[jugador] == 0:
                return False  # No le quedan fichas por colocar

            # Coloca pieza
            self.tablero[origen] = jugador
            self.por_colocar[jugador] -= 1
            self.en_tablero[jugador] += 1

            # Verificar molino
            if self._verificar_molino(origen):
                # se queda en mismo turno hasta eliminar ficha enemiga
                return "eliminar"

            # Si ambos ya colocaron todas, pasar a fase de movimiento
            if self.por_colocar[1] == 0 and self.por_colocar[-1] == 0:
                self.fase = "movimiento"

            # Cambiar turno
            self._cambiar_turno()
            return True

        else:  # cuando es la fase de movimiento
            # Movimiento normal: el origen debe tener ficha propia y destino vacío y válido
            if origen is None or destino is None:
                return False
            if not (0 <= origen < 24 and 0 <= destino < 24):
                return False
            if self.tablero[origen] != jugador:
                return False
            if self.tablero[destino] != 0:
                return False
            # Verificar adyacencia o vuelo
            if self.en_tablero[jugador] == 3:
                # puede volar a cualquier casilla vacía
                pass
            else:
                if destino not in self.movimientos_validos.get(origen, []):
                    return False

            # Ejecutar movimiento
            self.tablero[origen] = 0
            self.tablero[destino] = jugador

            # Verificar molino
            if self._verificar_molino(destino):
                return "eliminar"
            
            ## Si no se eliminó ninguna ficha, cuenta como turno sin eliminar
            self.turnos_sin_eliminar += 1
            if self.turnos_sin_eliminar >= 50:
                self.fin_juego = True
                self.ganador = 0  # 0 indica empate
                print("Empate: 50 turnos sin eliminar fichas.")
                return True
            # Cambiar turno
            self._cambiar_turno()
            return True

    
    def eliminar_ficha(self, punto: int, simulacion: bool = False) -> bool:
        if self.fin_juego:
            return False
        rival = -self.turno
        if punto < 0 or punto >= 24:
            return False
        if self.tablero[punto] != rival:
            return False
        # No puede eliminar ficha en molino a menos que todas estén en molino
        if self._es_molino(punto, rival) and not self._todas_en_molino(rival):
            return False

        # Elimina ficha
        self.tablero[punto] = 0
        self.en_tablero[rival] -= 1
        self.turnos_sin_eliminar = 0

        if not simulacion:
            print(f"Ficha eliminada en el punto {punto}.")

        # Solo se declara fin del juego si ya es la fase de movimiento
        if self.fase == "movimiento":
            # Si tras eliminar rival tiene <= 2 fichas o no tiene movimientos
            if self.en_tablero[rival] <= 2 or not self._tiene_movimientos(rival):
                self.fin_juego = True
                self.ganador = self.turno
                return True
        
        if self.fase == "colocacion" and self.por_colocar[1] == 0 and self.por_colocar[-1] == 0:
            self.fase = "movimiento"
            if not simulacion:
                print("Cambio de fase: colocación → movimiento")

        # Cambiar turno tras eliminación
        self._cambiar_turno()
        return True

    # Retorna True si en la posición 'punto' se formó un molino para el color en turno.
    def _verificar_molino(self, punto: int) -> bool:
        jugador = self.turno
        for molino in self._molinos_por_punto(punto):
            if all(self.tablero[pos] == jugador for pos in molino):
                return True
        return False

    # Verifica si la ficha en 'punto' forma parte de un molino del jugador dado.
    def _es_molino(self, punto: int, jugador: int) -> bool:
        for molino in self._molinos_por_punto(punto):
            if all(self.tablero[pos] == jugador for pos in molino):
                return True
        return False
    

    # Retorna True si todas las fichas de 'jugador' están en algún molino.
    def _todas_en_molino(self, jugador: int) -> bool:
        return all(
            self._es_molino(i, jugador) 
            for i, val in enumerate(self.tablero) if val == jugador
        )

    # Verifica si el jugador tiene movimientos válidos en la fase de movimiento
    def _tiene_movimientos(self, jugador: int) -> bool:
        for i, val in enumerate(self.tablero):
            if val == jugador:
                if self.en_tablero[jugador] == 3:
                    if any(self.tablero[d] == 0 for d in range(24)):
                        return True
                else:
                    for dest in self.movimientos_validos.get(i, []):
                        if self.tablero[dest] == 0:
                            return True
        return False

    # Devuelve las posibles combinaciones de molino en las que participa el punto
    def _molinos_por_punto(self, punto: int):
        molinos = [
            # Horizontales
            [0, 1, 2],     [3, 4, 5],     [6, 7, 8],
            [9, 10, 11],   [12, 13, 14], [15, 16, 17],
            [18, 19, 20],  [21, 22, 23],

            # Verticales
            [0, 9, 21],    [3, 10, 18],   [6, 11, 15],
            [1, 4, 7],     [16, 19, 22],
            [8, 12, 17],   [5, 13, 20],   [2, 14, 23]
        ]

        return [m for m in molinos if punto in m]

    # Cambia de turno
    def _cambiar_turno(self):
        self.turno *= -1
                       
    # Crea y retorna una copia del estado actual del juego
    def copiar_estado(self):
        nuevo = MorrisGame()
        nuevo.tablero = self.tablero[:]
        nuevo.turno = self.turno
        nuevo.fase = self.fase
        nuevo.por_colocar = self.por_colocar.copy()
        nuevo.en_tablero = self.en_tablero.copy()
        nuevo.fin_juego = self.fin_juego
        nuevo.ganador = self.ganador
        nuevo.movimientos_validos = {k: v[:] for k, v in self.movimientos_validos.items()}
        nuevo.control = self.control.copy()
        return nuevo

    # Retorna una copia del juego luego del movimiento simulado
    def simular_movimiento(self, origen: int, destino: int):
        copia = self.copiar_estado()
        # Para simulación, invocamos hacer_movimiento en copia: no importa que cambie turno en copia.
        _ = copia.hacer_movimiento(origen, destino)
        # Si devuelve "eliminar", la lógica de simulación de IA en Minimax deberá eliminar ficha manualmente
        return copia
