import pygame
import sys
from dificultad import Dificultad

class Menu:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.ancho, self.alto = pantalla.get_size()
        self.fuente = pygame.font.SysFont("Arial", 30)
        self.botones = {
            "PVP": pygame.Rect(self.ancho//2 - 150, self.alto//2 - 80, 300, 50),
            "PVE": pygame.Rect(self.ancho//2 - 150, self.alto//2, 300, 50),
        }
        self.dificultades = Dificultad.niveles_disponibles()
        self.seleccion_dificultad = None

    def dibujar(self):
        self.pantalla.fill((200, 200, 200))
        titulo = self.fuente.render("Morris - Selecciona Modo", True, (0, 0, 0))
        self.pantalla.blit(titulo, (self.ancho//2 - titulo.get_width()//2, 100))
        for clave, rect in self.botones.items():
            color = (100, 200, 100) if clave in ("PVP", "PVE") else (150, 150, 150)
            pygame.draw.rect(self.pantalla, color, rect)
            texto = {"PVP":"Jugador vs Jugador", "PVE":"Jugador vs IA", "EVE":"IA vs IA"}[clave]
            surf = self.fuente.render(texto, True, (0, 0, 0))
            self.pantalla.blit(surf, (rect.x + (rect.width - surf.get_width())//2, rect.y + (rect.height - surf.get_height())//2))

    def dibujar_seleccion_dificultad(self):
        self.pantalla.fill((200, 200, 200))
        titulo = self.fuente.render("Selecciona Dificultad", True, (0, 0, 0))
        self.pantalla.blit(titulo, (self.ancho//2 - titulo.get_width()//2, 100))
        for i, dificultad in enumerate(self.dificultades):
            rect = pygame.Rect(self.ancho//2 - 150, self.alto//2 + i*60, 300, 50)
            pygame.draw.rect(self.pantalla, (100, 200, 100), rect)
            surf = self.fuente.render(dificultad.capitalize(), True, (0, 0, 0))
            self.pantalla.blit(surf, (rect.x + (rect.width - surf.get_width())//2, rect.y + (rect.height - surf.get_height())//2))

    def elegir_quien_inicia(self):
        self.pantalla.fill((200, 200, 200))
        titulo = self.fuente.render("¿Quién inicia?", True, (0, 0, 0))
        self.pantalla.blit(titulo, (self.ancho//2 - titulo.get_width()//2, 100))
        
        boton_jugador = pygame.Rect(self.ancho//2 - 150, self.alto//2 - 50, 300, 50)
        boton_ia = pygame.Rect(self.ancho//2 - 150, self.alto//2 + 50, 300, 50)
        
        pygame.draw.rect(self.pantalla, (100, 200, 100), boton_jugador)
        pygame.draw.rect(self.pantalla, (200, 100, 100), boton_ia)
        
        texto_jugador = self.fuente.render("Jugador (Blancas)", True, (0, 0, 0))
        texto_ia = self.fuente.render("IA (Negras)", True, (0, 0, 0))
        
        self.pantalla.blit(texto_jugador, (boton_jugador.x + (boton_jugador.width - texto_jugador.get_width())//2,
                                           boton_jugador.y + (boton_jugador.height - texto_jugador.get_height())//2))
        self.pantalla.blit(texto_ia, (boton_ia.x + (boton_ia.width - texto_ia.get_width())//2,
                                      boton_ia.y + (boton_ia.height - texto_ia.get_height())//2))
                                      
        pygame.display.flip()
        
        seleccion = None
        while seleccion is None:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if boton_jugador.collidepoint(evento.pos):
                        seleccion = 'jugador'
                    elif boton_ia.collidepoint(evento.pos):
                        seleccion = 'ia'
        return seleccion

    def run(self):
        reloj = pygame.time.Clock()
        seleccion = None
        while seleccion is None:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    mx, my = evento.pos
                    for clave, rect in self.botones.items():
                        if rect.collidepoint(mx, my):
                            if clave == "PVP":
                                seleccion = ("PVP", {})
                            elif clave == "PVE":
                                self.dibujar_seleccion_dificultad()
                                pygame.display.flip()
                                dificultad_seleccionada = None
                                while dificultad_seleccionada is None:
                                    for ev in pygame.event.get():
                                        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                                            for i, dif in enumerate(self.dificultades):
                                                rect = pygame.Rect(self.ancho//2 - 150, self.alto//2 + i*60, 300, 50)
                                                if rect.collidepoint(ev.pos):
                                                    dificultad_seleccionada = dif
                                quien_inicia = self.elegir_quien_inicia()
                                prof = Dificultad(dificultad_seleccionada).obtener_profundidad()
                                seleccion = ("PVE", {"nivel": prof, "quien_inicia": quien_inicia})
            self.dibujar()
            pygame.display.flip()
            reloj.tick(30)
        return seleccion