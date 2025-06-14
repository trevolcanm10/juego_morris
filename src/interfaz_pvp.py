import pygame
import sys
import os
from logica_juego import MorrisGame

class InterfazPVP:
    def __init__(self, juego: MorrisGame, pantalla=None):
        if pantalla is None:
            pygame.init()
            self.pantalla = pygame.display.set_mode((800,800))
            pygame.display.set_caption("Morris PVP")
        else:
            self.pantalla = pantalla
        self.juego = juego
        # Configurar control: ambas blancas y negras humano
        self.juego.set_control('humano', 'humano')
        self.reloj = pygame.time.Clock()
        self.origen_seleccionado = None
        self.en_modo_eliminacion = False
        # Cargar assets de fichas
        self._cargar_assets()
        self.puntos_ui = self._generar_puntos_ui()
        self.fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
        self.fuente_info = pygame.font.SysFont("Arial", 20)

    def _cargar_assets(self):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "sprites"))
        try:
            self.ficha_blanca = pygame.image.load(os.path.join(base, "DamaBlanca.png"))
            self.ficha_negra  = pygame.image.load(os.path.join(base, "DamaNegra.png"))
            self.ficha_blanca = pygame.transform.scale(self.ficha_blanca, (40,40))
            self.ficha_negra  = pygame.transform.scale(self.ficha_negra,  (40,40))
        except Exception as e:
            print(f"Advertencia: no se cargaron imágenes de fichas: {e}")
            self.ficha_blanca = pygame.Surface((40,40),pygame.SRCALPHA)
            pygame.draw.circle(self.ficha_blanca, (255,255,255), (20,20), 20)
            self.ficha_negra  = pygame.Surface((40,40),pygame.SRCALPHA)
            pygame.draw.circle(self.ficha_negra, (0,0,0), (20,20), 20)

    def _generar_puntos_ui(self):
        escala = 100; offset = 100
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
        puntos=[]
        for i in range(24):
            x_log, y_log = coords[i]
            x = x_log*escala + offset
            y = y_log*escala + offset
            puntos.append((x,y))
        return puntos

    def dibujar_tablero(self):
        self.pantalla.fill((245,245,220))
        # Dibujar líneas del tablero
        pygame.draw.rect(self.pantalla, (0,0,0), (100,100,600,600), 3)
        pygame.draw.rect(self.pantalla, (0,0,0), (200,200,400,400), 3)
        pygame.draw.rect(self.pantalla, (0,0,0), (300,300,200,200), 3)
        pygame.draw.line(self.pantalla, (0,0,0), (400,100),(400,300),3)
        pygame.draw.line(self.pantalla, (0,0,0), (400,500),(400,700),3)
        pygame.draw.line(self.pantalla, (0,0,0), (100,400),(300,400),3)
        pygame.draw.line(self.pantalla, (0,0,0), (500,400),(700,400),3)
        # Dibujar puntos y fichas
        for i,(x,y) in enumerate(self.puntos_ui):
            pygame.draw.circle(self.pantalla, (100,100,100), (x,y), 10)
            val = self.juego.tablero[i]
            if val == 1:
                self.pantalla.blit(self.ficha_blanca, (x-20,y-20))
            elif val == -1:
                self.pantalla.blit(self.ficha_negra, (x-20,y-20))
        # Texto turno arriba-centro
        turno = self.juego.turno
        texto = f"Turno: {'Blancas (Jugador 1)' if turno==1 else 'Negras (Jugador 2)'}"
        surf = self.fuente_titulo.render(texto, True, (0,0,0))
        self.pantalla.blit(surf, (400 - surf.get_width()//2, 20))
        # Contador en fase colocación
        if self.juego.fase == "colocacion":
            # Blancas a la izquierda
            rest1 = self.juego.por_colocar[1]
            surf1 = self.fuente_info.render(f"Por colocar: {rest1}", True, (0,0,0))
            self.pantalla.blit(surf1, (50 - surf1.get_width()//2, 100))
            # Negras a la derecha
            rest2 = self.juego.por_colocar[-1]
            surf2 = self.fuente_info.render(f"Por colocar: {rest2}", True, (0,0,0))
            self.pantalla.blit(surf2, (750 - surf2.get_width()//2, 100))
        # Mensaje de eliminación
        if self.en_modo_eliminacion:
            aviso = self.fuente_info.render("¡Selecciona ficha a eliminar!", True, (200,0,0))
            self.pantalla.blit(aviso, (400 - aviso.get_width()//2, 60))

    def dibujar_fin_partida(self):
        s = pygame.Surface(self.pantalla.get_size(), pygame.SRCALPHA)
        s.fill((0,0,0,180))
        self.pantalla.blit(s, (0,0))
        ganador = self.juego.ganador
        if ganador is None:
            # Inferir: quien hizo el último movimiento ganador es el color actual
            ganador = self.juego.turno
        texto = f"¡{'Blancas (Jugador 1)' if ganador==1 else 'Negras (Jugador 2)'} gana!"
        surf = self.fuente_titulo.render(texto, True, (255,255,255))
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
                for i,(px,py) in enumerate(self.puntos_ui):
                    if (px-25 <= x <= px+25) and (py-25 <= y <= py+25):
                        if self.en_modo_eliminacion:
                            ok = self.juego.eliminar_ficha(i)
                            if ok:
                                print("Ficha eliminada correctamente.")
                                self.en_modo_eliminacion = False
                            else:
                                print("No puedes eliminar esa ficha.")
                            self.origen_seleccionado = None
                        else:
                            if self.juego.fase == "colocacion":
                                res = self.juego.hacer_movimiento(i)
                                if res == "eliminar":
                                    self.en_modo_eliminacion = True
                                    print("¡Molino! Selecciona ficha a eliminar.")
                                elif res:
                                    print(f"Ficha colocada en {i}.")
                                else:
                                    print("Movimiento inválido.")
                            else:
                                # fase movimiento
                                if self.origen_seleccionado is None:
                                    if self.juego.tablero[i] == self.juego.turno:
                                        self.origen_seleccionado = i
                                        print(f"Origen seleccionado: {i}")
                                    else:
                                        print("Selecciona una de tus fichas.")
                                else:
                                    destino = i
                                    res = self.juego.hacer_movimiento(self.origen_seleccionado, destino)
                                    if res == "eliminar":
                                        self.en_modo_eliminacion = True
                                        print("¡Molino! Selecciona ficha a eliminar.")
                                    elif res:
                                        print(f"Movido {self.origen_seleccionado} → {destino}")
                                    else:
                                        print("Movimiento inválido.")
                                    self.origen_seleccionado = None
                        break

    def ejecutar(self):
        boton_volver = None
        while True:
            # Eventos
            self.manejar_eventos()
            # Dibujar tablero o fin
            self.dibujar_tablero()
            if self.juego.fin_juego:
                boton_volver = self.dibujar_fin_partida()
            pygame.display.flip()
            self.reloj.tick(30)
            # Si fin, manejar botón volver
            if self.juego.fin_juego and boton_volver:
                for evento in pygame.event.get(pygame.MOUSEBUTTONDOWN):
                    if evento.button == 1 and boton_volver.collidepoint(evento.pos):
                        return