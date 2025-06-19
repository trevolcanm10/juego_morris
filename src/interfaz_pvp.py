import pygame
import sys
import os
from logica_juego import MorrisGame

ANCHO, ALTO = 800, 800

class InterfazPVP:
    def __init__(self, juego: MorrisGame, pantalla=None):
        self.ficha_seleccionada = None
        self.color_sombra_valida = (50, 255, 50, 180)  # Verde semitransparente
        self.color_sombra_invalida = (255, 50, 50, 180)  # Rojo semitransparente
        if pantalla is None:
            pygame.init()
            self.pantalla = pygame.display.set_mode((ANCHO,ALTO))
            pygame.display.set_caption("Morris PVP")
        else:
            self.pantalla = pantalla
        
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "sprites"))
        try:
            self.tablero_img = pygame.image.load(os.path.join(base, "tableroo.png")).convert_alpha()
            self.tablero_img = pygame.transform.scale(self.tablero_img, (ANCHO, ALTO))
        except FileNotFoundError:
            print(f"Error: No se encontró {os.path.join(base, 'tableroo.png')}")
            sys.exit()
        
        self.juego = juego
        self.juego.set_control('humano', 'humano')
        self.reloj = pygame.time.Clock()
        self.origen_seleccionado = None
        self.en_modo_eliminacion = False
        self._cargar_assets()
        self.puntos_ui = self._generar_puntos_ui()
        self.fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
        self.fuente_info = pygame.font.SysFont("Arial", 20)

    def _dibujar_sombra(self, posicion, color):
        """Dibuja un círculo semitransparente en la posición indicada."""
        x, y = self.puntos_ui[posicion]
        sombra = pygame.Surface((80, 80), pygame.SRCALPHA)  # Tamaño igual al de las fichas
        pygame.draw.circle(sombra, color, (34, 34), 34)  # Radio 34
        self.pantalla.blit(sombra, (x - 34, y - 34))  # Dibuja centrado

    def _cargar_assets(self):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "sprites"))
        nuevo_tamaño = 60
        try:
            self.ficha_blanca = pygame.image.load(os.path.join(base, "DamaBlanca.png"))
            self.ficha_negra = pygame.image.load(os.path.join(base, "DamaNegra.png"))
            self.ficha_blanca = pygame.transform.scale(self.ficha_blanca, (nuevo_tamaño,nuevo_tamaño))
            self.ficha_negra = pygame.transform.scale(self.ficha_negra, (nuevo_tamaño,nuevo_tamaño))
        except Exception as e:
            print(f"Advertencia: no se cargaron imágenes de fichas: {e}")
            self.ficha_blanca = pygame.Surface((nuevo_tamaño,nuevo_tamaño),pygame.SRCALPHA)
            pygame.draw.circle(self.ficha_blanca, (255,255,255), (nuevo_tamaño//2,nuevo_tamaño//2), nuevo_tamaño//2)
            self.ficha_negra = pygame.Surface((nuevo_tamaño,nuevo_tamaño),pygame.SRCALPHA)
            pygame.draw.circle(self.ficha_negra, (0,0,0), (nuevo_tamaño//2,nuevo_tamaño//2), nuevo_tamaño//2)
            
    def _generar_puntos_ui(self):
        escala = 107.5; offset_x = 90; offset_y = 75
        coords = {
            0:(0,0),1:(3,0),2:(6,0),
            3:(1,1),4:(3,1),5:(5,1),
            6:(2,2),7:(3,2),8:(4,2),
            9:(0,3),10:(1,3),11:(2,3),
            12:(4,3),13:(5,3),14:(6,3),
            15:(2,4),16:(3,4),17:(4,4),
            18:(1,5),19:(3,5),20:(5,5),
            21:(0,6),22:(3,6),23:(6,6)
        }
        puntos = []
        for i in range(24):
            x_log, y_log = coords[i]
            puntos.append((x_log*escala + offset_x, y_log*escala + offset_y))
        return puntos
        
    def dibujar_tablero(self):
        self.pantalla.blit(self.tablero_img, (0, 0))
        # Dibuja sombra si hay una ficha seleccionada
        if self.ficha_seleccionada is not None:
            puede_mover = self.juego._puede_mover(self.ficha_seleccionada)
            if puede_mover and self.juego.tablero[self.ficha_seleccionada] == self.juego.turno:
                color = self.color_sombra_valida
            else:
                color = self.color_sombra_invalida
            self._dibujar_sombra(self.ficha_seleccionada, color)

        radio_ficha = 30
        for i, (x, y) in enumerate(self.puntos_ui):
            val = self.juego.tablero[i]
            if val == 1:
                self.pantalla.blit(self.ficha_blanca, (x-radio_ficha, y-radio_ficha))
            elif val == -1:
                self.pantalla.blit(self.ficha_negra, (x-radio_ficha, y-radio_ficha))
        
        turno = self.juego.turno
        texto = f"Turno: {'Blancas (Jugador 1)' if turno==1 else 'Negras (Jugador 2)'}"
        surf = self.fuente_titulo.render(texto, True, (255,255,255))
        self.pantalla.blit(surf, (400 - surf.get_width()//2, 2))
        
        if self.juego.fase == "colocacion":
            rest1 = self.juego.por_colocar[1]
            surf1 = self.fuente_info.render(f"Por colocar (J1): {rest1}", True, (255,255,255))
            self.pantalla.blit(surf1, (50, ALTO-40))
            rest2 = self.juego.por_colocar[-1]
            surf2 = self.fuente_info.render(f"Por colocar (J2): {rest2}", True, (255,255,255))
            self.pantalla.blit(surf2, (ANCHO-200, ALTO-40))
        
        if self.en_modo_eliminacion:
            aviso = self.fuente_info.render("¡Selecciona ficha a eliminar!", True, (255,100,100))
            self.pantalla.blit(aviso, (400 - aviso.get_width()//2, 60))

    def dibujar_fin_partida(self):
        s = pygame.Surface(self.pantalla.get_size(), pygame.SRCALPHA)
        s.fill((0,0,0,180))
        self.pantalla.blit(s, (0,0))
        ganador = self.juego.ganador or self.juego.turno
        
        if ganador == 0:
            texto = "¡Empate!"
        elif ganador == 1:
            texto = "¡Blancas (Jugador 1) gana!"
        elif ganador == -1:
            texto = "¡Negras (Jugador 2) gana!"
        else:
            texto = "Fin del juego"
            
        surf = self.fuente_titulo.render(texto, True, (255, 215, 0))
        self.pantalla.blit(surf, (400 - surf.get_width()//2, 350))
        
        boton = pygame.Rect(300, 420, 200, 50)
        pygame.draw.rect(self.pantalla, (200,200,200), boton)
        surf_b = self.fuente_info.render("Volver al menú", True, (0,0,0))
        self.pantalla.blit(surf_b, (
            boton.x + (boton.width - surf_b.get_width())//2,
            boton.y + (boton.height - surf_b.get_height())//2
        ))
        return boton

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.juego.fin_juego:
                    return
                
                x,y = evento.pos
                radio_interaccion = 35
                for i,(px,py) in enumerate(self.puntos_ui):
                    if (px-radio_interaccion <= x <= px+radio_interaccion) and (py-radio_interaccion <= y <= py+radio_interaccion):
                        if self.en_modo_eliminacion:
                            self.juego.eliminar_ficha(i)
                            self.en_modo_eliminacion = False
                            self.origen_seleccionado = None
                            self.ficha_seleccionada = None
                        else:
                            if self.juego.fase == "colocacion":
                                res = self.juego.hacer_movimiento(i)
                                if res == "eliminar":
                                    self.en_modo_eliminacion = True
                            else:
                                if self.origen_seleccionado is None:
                                    if self.juego.tablero[i] == self.juego.turno:
                                        self.origen_seleccionado = i
                                        self.ficha_seleccionada = i
                                else:
                                    res = self.juego.hacer_movimiento(self.origen_seleccionado, i)
                                    if res == "eliminar":
                                        self.en_modo_eliminacion = True
                                    self.origen_seleccionado = None
                                    self.ficha_seleccionada = None
                        break

    def ejecutar(self):
        boton_volver = None
        while True:
            self.manejar_eventos()
            self.dibujar_tablero()
            if self.juego.fin_juego:
                boton_volver = self.dibujar_fin_partida()
            
            pygame.display.flip()
            self.reloj.tick(30)
            
            if self.juego.fin_juego and boton_volver:
                for evento in pygame.event.get(pygame.MOUSEBUTTONDOWN):
                    if evento.button == 1 and boton_volver.collidepoint(evento.pos):
                        return
