import pygame
import sys
from dificultad import Dificultad

class Menu:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.ancho, self.alto = pantalla.get_size()
        self.fuente = pygame.font.SysFont("Arial", 30)
        # Definir botones
        self.botones = {
            "PVP": pygame.Rect(self.ancho//2 - 150, self.alto//2 - 80, 300, 50),
            "PVE": pygame.Rect(self.ancho//2 - 150, self.alto//2,     300, 50),
            "EVE": pygame.Rect(self.ancho//2 - 150, self.alto//2 + 80,300, 50),
        }
        # Para PVE/EVE, se pedirá nivel en un paso extra

    def dibujar(self):
        self.pantalla.fill((200,200,200))
        titulo = self.fuente.render("Morris - Selecciona Modo", True, (0,0,0))
        self.pantalla.blit(titulo, (self.ancho//2 - titulo.get_width()//2, 100))
        for clave, rect in self.botones.items():
            # Habilitar PVP y PVE (suponemos que EVE quizá deshabilitado al inicio)
            if clave in ("PVP", "PVE"):
                color = (100,200,100)
            else:
                color = (150,150,150)
            pygame.draw.rect(self.pantalla, color, rect)
            texto = {"PVP":"Jugador vs Jugador", "PVE":"Jugador vs IA", "EVE":"IA vs IA"}[clave]
            surf = self.fuente.render(texto, True, (0,0,0))
            self.pantalla.blit(surf, (
                rect.x + (rect.width - surf.get_width())//2,
                rect.y + (rect.height - surf.get_height())//2
            ))

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
                                # Pedir nivel de IA: por simplicidad, se fija o se elige en consola
                                # Aquí usamos nivel "regular" por defecto; podrías implementar otro menú:
                                nivel = "regular"
                                profundidad = Dificultad(nivel).obtener_profundidad()
                                seleccion = ("PVE", {"nivel": profundidad})
                            else:
                                print(f"Modo {clave} aún no implementado")
            self.dibujar()
            pygame.display.flip()
            reloj.tick(30)
        return seleccion