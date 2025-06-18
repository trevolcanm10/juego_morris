import pygame
import sys
from menu import Menu
from logica_juego import MorrisGame
from interfaz_pvp import InterfazPVP
from interfaz_pve import InterfazPVE
from interfaz_eve import InterfazEVE

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Morris - Grupo 9")

    # Crear una instancia del juego antes de pasarla al menú
    juego = MorrisGame()
    while True:
        # Mostrar menú
        menu = Menu(pantalla,juego)
        modo, config = menu.run()
        if modo == "PVP":
            interfaz = InterfazPVP(juego, pantalla=pantalla)
        elif modo == "PVE":
            nivel = config.get("nivel", 3)
            interfaz = InterfazPVE(juego, pantalla=pantalla, nivel=nivel)
        elif modo == "EVE":
            # Podrías pedir dos niveles; aquí usamos mismos
            nivel1 = config.get("nivel_blancas", 3)
            nivel2 = config.get("nivel_negras", 3)
            interfaz = InterfazEVE(juego, pantalla=pantalla,
                                  nivel_blancas=nivel1, nivel_negras=nivel2)
        else:
            continue
        interfaz.ejecutar()
        # Al volver de ejecutar (cuando se pulsa “Volver al menú”), reinicia bucle
if __name__ == "__main__":
    main()