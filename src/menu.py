import pygame
import sys
from dificultad import Dificultad  # Asegúrate de que esté importado
from interfaz_pve import InterfazPVE

class Menu:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.ancho, self.alto = pantalla.get_size()
        self.fuente = pygame.font.SysFont("Arial", 30)
        self.botones = {
            "PVP": pygame.Rect(self.ancho//2 - 150, self.alto//2 - 80, 300, 50),
            "PVE": pygame.Rect(self.ancho//2 - 150, self.alto//2, 300, 50),
            "EVE": pygame.Rect(self.ancho//2 - 150, self.alto//2 + 80, 300, 50),
        }
        self.dificultades = ["fácil", "regular", "difícil"]
        self.seleccion_dificultad = None  # Para guardar la dificultad seleccionada

    def dibujar(self):
        self.pantalla.fill((200, 200, 200))
        titulo = self.fuente.render("Morris - Selecciona Modo", True, (0, 0, 0))
        self.pantalla.blit(titulo, (self.ancho//2 - titulo.get_width()//2, 100))
        for clave, rect in self.botones.items():
            color = (100, 200, 100) if clave in ("PVP", "PVE") else (150, 150, 150)
            pygame.draw.rect(self.pantalla, color, rect)
            texto = {"PVP": "Jugador vs Jugador", "PVE": "Jugador vs IA", "EVE": "IA vs IA"}[clave]
            surf = self.fuente.render(texto, True, (0, 0, 0))
            self.pantalla.blit(surf, (rect.x + (rect.width - surf.get_width())//2, rect.y + (rect.height - surf.get_height())//2))

    def dibujar_seleccion_dificultad(self):
        self.pantalla.fill((200, 200, 200))
        titulo = self.fuente.render("Selecciona Dificultad", True, (0, 0, 0))
        self.pantalla.blit(titulo, (self.ancho//2 - titulo.get_width()//2, 100))
        
        # Mostrar las opciones de dificultad
        for i, dificultad in enumerate(self.dificultades):
            rect = pygame.Rect(self.ancho//2 - 150, self.alto//2 + i*60, 300, 50)
            pygame.draw.rect(self.pantalla, (100, 200, 100), rect)
            surf = self.fuente.render(dificultad.capitalize(), True, (0, 0, 0))
            self.pantalla.blit(surf, (rect.x + (rect.width - surf.get_width())//2, rect.y + (rect.height - surf.get_height())//2))
        
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
                                # Ir a la pantalla de selección de dificultad
                                self.dibujar_seleccion_dificultad()
                                pygame.display.flip()

                                while not self.seleccion_dificultad:
                                    for ev in pygame.event.get():
                                        if ev.type == pygame.QUIT:
                                            pygame.quit(); sys.exit()
                                        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                                            for i, dificultad in enumerate(self.dificultades):
                                                rect = pygame.Rect(self.ancho//2 - 150, self.alto//2 + i*60, 300, 50)
                                                if rect.collidepoint(ev.pos):
                                                    self.seleccion_dificultad = dificultad
                                                    break
                                # Al finalizar la selección de dificultad
                                profundidad = Dificultad(self.seleccion_dificultad).obtener_profundidad()
                                seleccion = ("PVE", {"nivel": profundidad})
                            elif clave == "EVE":
                                # Aún no implementado
                                pass
            self.dibujar()
            pygame.display.flip()
            reloj.tick(30)
        return seleccion
