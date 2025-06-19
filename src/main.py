import pygame
import sys
from menu import Menu
from logica_juego import MorrisGame
from interfaz_pvp import InterfazPVP
from interfaz_pve import InterfazPVE

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Morris - Grupo 9")

    while True:
        menu = Menu(pantalla)
        modo, config = menu.run()
        juego = MorrisGame()
        if modo == "PVP":
            interfaz = InterfazPVP(juego, pantalla=pantalla)
        elif modo == "PVE":
            nivel = config.get("nivel", 3)
            quien_inicia = config.get("quien_inicia", 'jugador')
            interfaz = InterfazPVE(juego, pantalla=pantalla, nivel=nivel, quien_inicia=quien_inicia)
        elif modo == "EVE":
            # Implementación futura
            continue
        else:
            continue
        interfaz.ejecutar()

if __name__ == "__main__":
    main()