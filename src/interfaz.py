
import pygame
import sys
import os

class InterfazMorris:
    def __init__(self, juego):
        pygame.init()
        self.juego = juego
        self.pantalla = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Morris - Grupo 9")
        self.reloj = pygame.time.Clock()
        self.cargar_assets()
        self.origen_seleccionado = None #Control de movimientos en dicha fase
        self.puntos_ui = self._generar_puntos_ui()
        self.en_modo_eliminacion = False
        self.fuente = pygame.font.SysFont("Arial", 24)

    def cargar_assets(self):
        """Carga imágenes de las fichas."""
        try:
            self.ficha_blanca = pygame.image.load(os.path.join("..","assets", "sprites", "DamaBlanca.png"))
            self.ficha_negra = pygame.image.load(os.path.join("..","assets", "sprites", "DamaNegra.png"))
            self.ficha_blanca = pygame.transform.scale(self.ficha_blanca, (40, 40))
            self.ficha_negra = pygame.transform.scale(self.ficha_negra, (40, 40))
        except FileNotFoundError as e:
            print(f"Error al cargar assets: {e}")
            sys.exit()

    def _generar_puntos_ui(self):
        """Genera las coordenadas en píxeles para cada punto del tablero (usando coordenadas lógicas)."""
        escala = 100
        offset = 100  # margen para centrar el tablero

        coordenadas_logicas = {
            0: (0, 0),     1: (3, 0),     2: (6, 0),
            3: (1, 1),     4: (3, 1),     5: (5, 1),
            6: (2, 2),     7: (3, 2),     8: (4, 2),
            9: (0, 3),    10: (1, 3),    11: (2, 3),
            12: (4, 3),    13: (5, 3),    14: (6, 3),
            15: (2, 4),    16: (3, 4),    17: (4, 4),
            18: (1, 5),    19: (3, 5),    20: (5, 5),
            21: (0, 6),    22: (3, 6),    23: (6, 6)
        }

        return [(x * escala + offset, y * escala + offset) for i in range(24) for x, y in [coordenadas_logicas[i]]]


    def dibujar_tablero(self):
        """Dibuja el tablero completo con líneas y puntos."""
        self.pantalla.fill((245, 245, 220))  # Fondo beige
        
        # Dibujar los 3 cuadrados concéntricos
        pygame.draw.rect(self.pantalla, (0, 0, 0), (100, 100, 600, 600), 3)  # Exterior
        pygame.draw.rect(self.pantalla, (0, 0, 0), (200, 200, 400, 400), 3)  # Medio 
        pygame.draw.rect(self.pantalla, (0, 0, 0), (300, 300, 200, 200), 3)  # Interior
        
        # Dibujar líneas cruzadas
        pygame.draw.line(self.pantalla, (0, 0, 0), (400, 100), (400, 300), 3)  # Arriba
        pygame.draw.line(self.pantalla, (0, 0, 0), (400, 500), (400, 700), 3)  # Abajo
        pygame.draw.line(self.pantalla, (0, 0, 0), (100, 400), (300, 400), 3)  # Izquierda
        pygame.draw.line(self.pantalla, (0, 0, 0), (500, 400), (700, 400), 3)  # Derecha
        
        # Dibujar puntos y fichas
        for i, (x, y) in enumerate(self.puntos_ui):
            pygame.draw.circle(self.pantalla, (100, 100, 100), (x, y), 10)  # Puntos grises
            if self.juego.tablero[i] == 1:
                self.pantalla.blit(self.ficha_blanca, (x-20, y-20))
            elif self.juego.tablero[i] == -1:
                self.pantalla.blit(self.ficha_negra, (x-20, y-20))
        
        # Mostrar turno actual
        texto = self.fuente.render(f"Turno: {'Jugador' if self.juego.turno_jugador == 1 else 'IA'}", True, (0, 0, 0))
        self.pantalla.blit(texto, (20, 20))

    def manejar_eventos(self):
        #Registra eventos como clicks,teclas,cerrar ventana
        for evento in pygame.event.get():
            #Usuario cierra la ventana
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Evento clickMouse    
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                #Colocación de fichas o movimientos
                for i, (px, py) in enumerate(self.puntos_ui):
                    #Areas de clickeo 50 x 50
                    if (px-25 <= x <= px+25) and (py-25 <= y <= py+25):
                        if self.en_modo_eliminacion:
                            if self.juego.eliminar_ficha(i):
                                self.en_modo_eliminacion = False
                                print("Ficha eliminada correctamente.")
                            else:
                                print("No puedes eliminar esa ficha.")
                        else:
                            if self.juego.fase == "colocacion":
                                resultado = self.juego.hacer_movimiento(i)
                                if resultado =="eliminar":
                                    self.en_modo_eliminacion = True
                                    print("¡Molino formado! Selecciona una ficha del oponente para eliminar.")
                            else: #Fase de movimiento
                                if self.juego.fichas_jugador > 0 or self.juego.fichas_ia > 0:
                                    print("Ambos jugadores deben colocar sus 6 fichas antes de mover.")
                                    return
                                if self.origen_seleccionado is None:
                                    if self.juego.tablero[i] == self.juego.turno_jugador:
                                        self.origen_seleccionado = i
                                        print(f"Ficha seleccionada en {i}. Ahora elige destino.")
                                    else:
                                        print("Debes seleccionar una de tus propias fichas.")
                                else:
                                    destino = i
                                    resultado = self.juego.hacer_movimiento(self.origen_seleccionado, destino)
                                    if resultado == "eliminar":
                                        self.en_modo_eliminacion = True
                                        print("¡Molino formado! Selecciona una ficha del oponente para eliminar.")
                                    elif resultado:
                                        print(f"Movimiento de {self.origen_seleccionado} a {destino} realizado.")
                                    else:
                                        print("Movimiento inválido. Intenta nuevamente.")
                                    self.origen_seleccionado = None
                        break

    def ejecutar(self):
        while True:
            self.manejar_eventos()
            self.dibujar_tablero()
            pygame.display.flip()
            self.reloj.tick(30)