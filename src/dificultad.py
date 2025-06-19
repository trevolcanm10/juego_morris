class Dificultad:
    NIVELES = {
        "fácil": 1,
        "regular": 2,
        "difícil": 3,
        "extremo": 4
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
