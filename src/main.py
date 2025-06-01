from logica_juego import MorrisGame
from interfaz import InterfazMorris

def main():
    juego = MorrisGame()
    interfaz = InterfazMorris(juego)
    interfaz.ejecutar()
if __name__=="__main__":
    main()