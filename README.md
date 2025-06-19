# Juego de Morris en Python

Este proyecto es una implementación del clásico **Juego de Morris** (también conocido como **Nine Men's Morris** o **Mills**) en Python. El juego permite jugar en los modos **Jugador vs Jugador (PVP)** y **Jugador vs IA (PVE)**, y está construido con la librería **pygame** para la interfaz gráfica y **numpy** para optimizaciones de cálculo.

## Descripción

El objetivo del juego es alinear tres fichas en una fila (ya sea horizontal o vertical) para formar un **molino**. Cuando un jugador forma un molino, puede eliminar una ficha del oponente. El juego termina cuando un jugador reduce a su oponente a dos fichas o lo bloquea completamente, impidiendo que realice movimientos.

Este proyecto incluye:

- **Lógica de juego**: El tablero tiene 24 puntos conectados, y las fichas se colocan y se mueven entre los puntos. Además, incluye la eliminación de fichas cuando se forma un molino.
- **Interfaz gráfica**: Usando **pygame**, se visualiza el tablero y las fichas, y se permite la interacción del jugador.
- **IA**: En el modo **PVE**, un algoritmo **Minimax** con poda **alfa-beta** decide los movimientos de la inteligencia artificial.

## Estructura del Proyecto

El proyecto está organizado en varios archivos de Python, cada uno con un propósito específico:

### 1. **dificultad.py**
   - Contiene la clase `Dificultad`, que define los niveles de dificultad del juego (fácil, regular, difícil, extremo) y su respectiva profundidad para la IA.

### 2. **logica_juego.py**
   - Contiene la clase `MorrisGame`, que maneja la lógica del juego, incluyendo la representación del tablero, el turno de los jugadores, la colocación y el movimiento de las fichas, la eliminación de fichas y la detección de molinos.

### 3. **evaluacion.py**
   - Contiene la función `evaluar_tablero()`, que evalúa el estado del juego y asigna una puntuación al tablero, considerando factores como la diferencia de fichas, los molinos formados, la amenaza de molinos, la movilidad de las piezas, el control de las posiciones centrales, y más. Esta evaluación es crucial para la toma de decisiones de la inteligencia artificial en el algoritmo **Minimax**.

### 4. **interfaz_pve.py**
   - Implementa la interfaz gráfica para el modo **PVE** (Jugador vs IA). Permite que el jugador se enfrente contra la IA, mostrando el tablero y gestionando los eventos de entrada.

### 5. **interfaz_pvp.py**
   - Implementa la interfaz gráfica para el modo **PVP** (Jugador vs Jugador). Permite que dos jugadores jueguen en el mismo dispositivo, mostrando el tablero y gestionando los eventos de entrada.

### 6. **main.py**
   - Es el archivo principal que ejecuta el juego. Permite al usuario elegir entre los modos **PVP** o **PVE** desde el menú y arranca la interfaz correspondiente.

### 7. **menu.py**
   - Define el menú principal que permite seleccionar el modo de juego y la dificultad en el caso del modo **PVE**.

### 8. **minimax.py**
   - Implementa el algoritmo **Minimax** con poda **alfa-beta** para la inteligencia artificial en el modo **PVE**.

## Requisitos

### Dependencias

- **Python 3.x** (se recomienda una versión 3.6 o superior)
- **pygame**: para la interfaz gráfica y la interacción del usuario.
- **numpy**: aunque no está explícitamente mencionado en los archivos cargados, se recomienda instalarlo para futuras optimizaciones de cálculos o si es necesario para el manejo eficiente de arrays.

#### Instalación de dependencias con `conda`

Si prefieres usar **conda** para gestionar tus entornos y dependencias, puedes crear un entorno específico para este proyecto y luego instalar las dependencias necesarias.

1. Crea un entorno de **conda** para el proyecto:

   ```bash
   conda create --name morris_game python=3.8
2. Activa el entorno:
   ```bash
   conda activate morris_game
3.Instala las dependencias utilizando conda (y pip cuando no estén disponibles en el repositorio de conda):

    ```bash
    conda install pygame numpy
    pip install pygame numpy
Ejecución
  Para ejecutar el juego, simplemente corre el siguiente comando:
     ```bash
     
    python main.py
  El programa iniciará el menú donde podrás elegir entre los modos:
    1.PVP: Jugador vs Jugador (dos jugadores en el mismo dispositivo).
    2.PVE: Jugador vs IA, con la opción de seleccionar el nivel de dificultad y quién inicia la partida.

 Modo de Juego
  -Fase de colocación: Los jugadores colocan sus fichas en el tablero. En esta fase, pueden colocar fichas en cualquier punto vacío.
  
  -Fase de movimiento: Después de que ambos jugadores hayan colocado todas sus piezas, pueden moverlas por el tablero.
  
  -Eliminación: Cuando un jugador forma un molino (tres fichas alineadas), puede eliminar una ficha del oponente.
  
  -Final del juego: El juego termina cuando un jugador reduce al oponente a dos fichas o lo bloquea completamente, impidiendo que realice movimientos.

Evaluación del Tablero
  -La evaluación del tablero es una parte crucial del algoritmo Minimax utilizado para la IA. La función evaluar_tablero() analiza el estado actual del tablero y asigna una puntuación para ayudar a la IA a decidir qué movimiento realizar. Los factores evaluados son:
  
  -Diferencia de fichas: Se cuenta cuántas fichas tiene cada jugador en el tablero y se otorgan puntos positivos para el jugador actual y puntos negativos para el oponente.
  
  -Molinos formados: Se da una gran recompensa por formar un molino (tres fichas alineadas), y se penaliza al oponente si forma un molino.
  
  -Amenaza de molino: Si el jugador o el oponente está a punto de formar un molino, se incentiva o penaliza según corresponda.
  
  -Posibilidad futura de molino: Se valora la presión ofensiva de un jugador que podría formar un molino en el futuro.
  
  -Movilidad: Se cuenta cuántos movimientos posibles tiene cada jugador. Se premia a los jugadores con más opciones de movimiento.
  
  -Control de posiciones centrales: Se otorgan puntos por ocupar las posiciones centrales del tablero, que son estratégicamente ventajosas.
  
  -Fichas bloqueadas: Se penaliza al jugador si tiene fichas bloqueadas que no pueden moverse.
  
  -Eliminación de fichas: Se dan puntos por cada ficha eliminada del oponente.
  
  -Vuelo (modo con 3 fichas): Cuando un jugador tiene solo 3 fichas en el tablero, puede "volar" a cualquier casilla vacía. Se premia el uso de esta ventaja.
  
  -Victoria técnica: Si un jugador reduce al oponente a 2 fichas o no puede realizar movimientos, se considera una victoria.
