class Dificultad:
    NIVELES = {
        "fácil": 2,
        "regular": 3,
        "difícil": 4,
        "extremo": 5
    }
    
    def __init__(self, nivel: str = "regular"):
        if nivel not in self.NIVELES:
            raise ValueError(f"Nivel desconocido: {nivel}")
        self.nivel = nivel

    def obtener_profundidad(self) -> int:
        return self.NIVELES[self.nivel]

    @classmethod
    def niveles_disponibles(cls):
        return list(cls.NIVELES.keys())