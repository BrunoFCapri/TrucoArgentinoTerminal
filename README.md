# Truco Argentino Terminal

Juego de Truco Argentino para la terminal, con gráficos ASCII para las cartas y lógica completa de partida contra la máquina.

## Características
- Juego clásico de Truco Argentino (primer a 15 puntos).
- Gráficos de cartas en ASCII.
- Envido, Truco, Flor y puntajes automáticos.
- IA básica para la máquina.
- Interfaz interactiva por consola.

## Estructura del proyecto
- `main.py`: Entrada principal del juego. Controla el flujo de la partida.
- `game.py`: Lógica de la ronda, reparto de cartas, jugadas y reglas.
- `truco.py`: (Puede contener lógica alternativa o funciones auxiliares del juego).
- `utils.py`: Funciones utilitarias, carga de cartas y gráficos, limpieza de consola.
- `cartas.txt`: Gráficos ASCII de todas las cartas por palo.

## Instalación
1. Clona el repositorio:
   ```sh
   git clone https://github.com/BrunoFCapri/TrucoArgentinoTerminal.git
   ```
2. Entra a la carpeta del proyecto:
   ```sh
   cd TrucoArgentinoTerminal/Truco
   ```
3. (Opcional) Crea un entorno virtual:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```

## Ejecución
Ejecuta el juego desde la terminal:
```sh
python main.py
```

## Cómo jugar
- El juego muestra tu mano y la de la máquina.
- Puedes elegir cartas, cantar Truco, Envido, Flor o irte al mazo.
- El primero en llegar a 15 puntos gana la partida.
- Los gráficos de las cartas se muestran en la consola.

## Ejemplo de uso
```
--- Truco Argentino ---
Primer a 15 puntos gana.

Puntos: Jugador 0 - Máquina 0
Mano de Jugador:
[1] 3 de Espadas   [2] 7 de Oros   [3] 1 de Bastos
+--------+   +--------+   +--------+
| 3      |   | 7      |   | 1      |
...      ...           ...
Elige la carta a tirar (1-3), 'truco', 'puntos' o 'mazo':
```

## Créditos
Desarrollado por BrunoFCapri para usarlo como comando especial para mi powershell modificada

## Licencia
Este proyecto se distribuye bajo la licencia MIT.
