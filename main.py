import os
from utils import cargar_cartas, clear_console
from game import jugar_ronda

def main():
    path_cartas = os.path.join(os.path.dirname(__file__), "cartas.txt")
    palos = cargar_cartas(path_cartas)
    puntos_jugador = puntos_maquina = 0
    print("\n--- Truco Argentino ---\nPrimer a 15 puntos gana.\n")
    while puntos_jugador < 15 and puntos_maquina < 15:
        print(f"\nPuntos: Jugador {puntos_jugador} - Máquina {puntos_maquina}")
        puntos_jugador, puntos_maquina = jugar_ronda(palos, puntos_jugador, puntos_maquina)
        clear_console()
    if puntos_jugador >= 15:
        print("\n¡Felicidades! Ganaste la partida de Truco.")
    else:
        print("\nLa máquina ganó la partida de Truco.")

if __name__ == "__main__":
    main()