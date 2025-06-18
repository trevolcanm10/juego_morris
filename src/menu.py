import pygame
import sys
from dificultad import Dificultad
#menu.py
class Menu:
    def __init__(self, pantalla,juego):
        self.pantalla = pantalla
        self.juego = juego #Aquí inicializamos self.juego
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

    # Esta función permitirá al jugador elegir quién empieza la partida.
    def elegir_quien_inicia(self):
        """Permite que el jugador elija quién inicia la partida."""
        self.pantalla.fill((200, 200, 200))  # Limpiar pantalla
        #Definir las áreas para los clics
        area_jugador = pygame.Rect(self.ancho // 2 - 150, self.alto // 2 - 50, 300, 50)  # Área para que el jugador elija
        area_ia = pygame.Rect(self.ancho // 2 - 150, self.alto // 2 + 20, 300, 50)  # Área para que la IA elija

        #Mensaje
        mensaje = self.fuente.render("¿Quién inicia? (1: Jugador, 2: IA)", True, (0, 0, 0))
        self.pantalla.blit(mensaje, (self.ancho // 2 - mensaje.get_width() // 2, self.alto // 2 - 100))
         # Dibujar las opciones
        pygame.draw.rect(self.pantalla, (100, 200, 100), area_jugador)
        pygame.draw.rect(self.pantalla, (200, 100, 100), area_ia)

        texto_jugador = self.fuente.render("Jugador", True, (0, 0, 0))
        texto_ia = self.fuente.render("IA", True, (0, 0, 0))

        self.pantalla.blit(texto_jugador, (area_jugador.x + (area_jugador.width - texto_jugador.get_width()) // 2,
                                           area_jugador.y + (area_jugador.height - texto_jugador.get_height()) // 2))
        self.pantalla.blit(texto_ia, (area_ia.x + (area_ia.width - texto_ia.get_width()) // 2,
                                      area_ia.y + (area_ia.height - texto_ia.get_height()) // 2))
                                      
        pygame.display.flip()
        
        #Dibujar las opciones
        seleccion = None
        while seleccion is None:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    if area_jugador.collidepoint(mx, my):
                        seleccion = 'jugador'
                    elif area_ia.collidepoint(mx, my):
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
                                # Pedir nivel de IA: por simplicidad, se fija o se elige en consola
                                # Aquí usamos nivel "regular" por defecto; podrías implementar otro menú:
                                nivel = "regular"
                                profundidad = Dificultad(nivel).obtener_profundidad()
                                seleccion = ("PVE", {"nivel": profundidad})
                                #Opción de elección quién inicia
                                seleccion_quien_inicia = self.elegir_quien_inicia() #nueva funcion
                                self.juego.establecer_turno_inicial(seleccion_quien_inicia) #ajustamos el turno
                                return seleccion
                            else:
                                print(f"Modo {clave} aún no implementado")
            self.dibujar()
            pygame.display.flip()
            reloj.tick(30)
        return seleccion