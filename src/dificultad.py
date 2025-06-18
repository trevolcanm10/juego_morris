class Dificultad:
    NIVELES = {
        "fácil": 2,       # Menor profundidad = IA menos inteligente
        "regular": 3,     # Profundidad media = IA equilibrada
        "difícil": 4,     # Mayor profundidad = IA más inteligente
    }

    def __init__(self, nivel: str = "regular"):
        # Verificar que el nivel proporcionado sea válido
        if nivel not in self.NIVELES:
            raise ValueError(f"Nivel desconocido: {nivel}. Los niveles disponibles son: {', '.join(self.NIVELES.keys())}")
        self.nivel = nivel

    def obtener_profundidad(self) -> int:
        """Devuelve la profundidad de búsqueda para Minimax según el nivel de dificultad."""
        return self.NIVELES[self.nivel]

    @classmethod
    def niveles_disponibles(cls):
        """Devuelve los niveles disponibles para la dificultad."""
        return list(cls.NIVELES.keys())

    def cambiar_nivel(self, nuevo_nivel: str):
        """Permite cambiar el nivel de dificultad si es necesario."""
        if nuevo_nivel not in self.NIVELES:
            raise ValueError(f"Nivel desconocido: {nuevo_nivel}. Los niveles disponibles son: {', '.join(self.NIVELES.keys())}")
        self.nivel = nuevo_nivel
