import os
import os
def elegir_carta(palos, mano, puntos_jugador, puntos_maquina, mazo_descartado):
    global truco_cantado_global
    while True:
        eleccion = input("Elige la carta a tirar (1-3), 'truco', 'puntos' o 'mazo': ").strip().lower()
        if eleccion == "puntos":
            clear_console()
            print(f"Puntos actuales:\nJugador: {puntos_jugador} - Máquina: {puntos_maquina}")
            input("Presiona 'q' para volver al juego...")
            clear_console()
            continue
        if eleccion == "mazo":
            clear_console()
            print("Cartas que ya salieron del mazo:")
            if mazo_descartado:
                mostrar_cartas_horizontal(palos, mazo_descartado)
            else:
                print("No hay cartas descartadas todavía.")
            input("Presiona 'q' para volver al juego...")
            clear_console()
            continue
        if eleccion == "truco":
            if not truco_cantado_global:
                truco_cantado_global = True
                print("¡Truco cantado!")
            else:
                print("Ya cantaste Truco en esta ronda.")
            continue
        try:
            eleccion_num = int(eleccion)
            if 1 <= eleccion_num <= len(mano):
                return mano.pop(eleccion_num-1)
        except Exception:
            pass
        print("Opción inválida.")
def mostrar_carta(palos, palo, num):
    carta = palos.get(palo, {}).get(num)
    if carta:
        print(carta)
    else:
        print(f"No se encontró la carta {num} de {palo}")

# Mostrar varias cartas en horizontal
def mostrar_cartas_horizontal(palos, mano):
    if not mano:
        print("(Sin cartas)")
        return
    graficas = []
    for palo, num in mano:
        carta = palos.get(palo, {}).get(num)
        if carta:
            graficas.append(carta.splitlines())
        else:
            graficas.append([f"No se encontró la carta {num} de {palo}"])
    max_altura = max(len(g) for g in graficas)
    for i in range(len(graficas)):
        if len(graficas[i]) < max_altura:
            graficas[i] += [' ' * len(graficas[i][0])] * (max_altura - len(graficas[i]))
    for fila in range(max_altura):
        print('   '.join(graficas[c][fila] for c in range(len(graficas))))

PALOS_TRUCO = ["Espadas", "Bastos", "Oros", "Copas"]
VALORES_TRUCO = ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]
JERARQUIA = [
    ("Espadas", "1"), ("Bastos", "1"), ("Espadas", "7"), ("Oros", "7"),
    ("Copas", "3"), ("Oros", "3"), ("Bastos", "3"), ("Espadas", "3"),
    ("Copas", "2"), ("Oros", "2"), ("Bastos", "2"), ("Espadas", "2"),
    ("Copas", "1"), ("Oros", "1"), ("Copas", "12"), ("Oros", "12"), ("Bastos", "12"), ("Espadas", "12"),
    ("Copas", "11"), ("Oros", "11"), ("Bastos", "11"), ("Espadas", "11"),
    ("Copas", "10"), ("Oros", "10"), ("Bastos", "10"), ("Espadas", "10"),
    ("Copas", "7"), ("Bastos", "7"), ("Copas", "6"), ("Oros", "6"), ("Bastos", "6"), ("Espadas", "6"),
    ("Copas", "5"), ("Oros", "5"), ("Bastos", "5"), ("Espadas", "5"),
    ("Copas", "4"), ("Oros", "4"), ("Bastos", "4"), ("Espadas", "4"),
]

def valor_truco(carta):
    try:
        return JERARQUIA.index(carta)
    except ValueError:
        return 100

def valor_envido(mano):
    valores = []
    for palo in PALOS_TRUCO:
        nums = [int(c[1]) if c[1] in ["10","11","12"] else int(c[1]) for c in mano if c[0]==palo]
        nums = [n if n<10 else 0 for n in nums]
        if len(nums)>=2:
            valores.append(sum(sorted(nums)[-2:]))
        elif len(nums)==1:
            valores.append(nums[0])
    return max(valores) if valores else 0

def repartir():
    mazo = [(palo, valor) for palo in PALOS_TRUCO for valor in VALORES_TRUCO]
    random.shuffle(mazo)
    return mazo[:3], mazo[3:6]

def mostrar_mano(palos, mano, jugador):
    print(f"\nMano de {jugador}:")
    etiquetas = [f"[{i+1}] {num} de {palo}" for i, (palo, num) in enumerate(mano)]
    print('   '.join(etiquetas))
    mostrar_cartas_horizontal(palos, mano)

def elegir_carta(palos, mano, puntos_jugador, puntos_maquina, mazo_descartado):
    global truco_cantado_global
    while True:
        eleccion = input("Elige la carta a tirar (1-3), 'truco' o 'puntos': ").strip().lower()
        if eleccion == "puntos":
            clear_console()
            print(f"Puntos actuales:\nJugador: {puntos_jugador} - Máquina: {puntos_maquina}")
            input("Presiona 'q' para volver al juego...")
            clear_console()
            continue
        if eleccion == "truco":
            if not truco_cantado_global:
                truco_cantado_global = True
                print("¡Truco cantado!")
            else:
                print("Ya cantaste Truco en esta ronda.")
            continue
        try:
            eleccion_num = int(eleccion)
            if 1 <= eleccion_num <= len(mano):
                return mano.pop(eleccion_num-1)
        except Exception:
            pass
        print("Opción inválida.")

def turno_maquina(mano):
    idx = min(range(len(mano)), key=lambda i: valor_truco(mano[i]))
    return mano.pop(idx)

def jugar_ronda(palos, puntos_jugador, puntos_maquina):
    mano_jugador, mano_maquina = repartir()
    mostrar_mano(palos, mano_jugador, "Jugador")
    puntos_truco = 1
    global truco_cantado_global
    truco_cantado_global = False
    mesa = []
    mazo_descartado = []
    ganadas_jugador = ganadas_maquina = 0
    for turno in range(3):
        print(f"\nTurno {turno+1}:")
        carta_jugador = elegir_carta(palos, mano_jugador, puntos_jugador, puntos_maquina, mazo_descartado)
        mazo_descartado.append(carta_jugador)
        carta_maquina = turno_maquina(mano_maquina)
        mazo_descartado.append(carta_maquina)
        mesa.append((carta_jugador, carta_maquina))
        print("\n--- Mesa ---")
        jugadas_jugador = [cj for cj, cm in mesa]
        jugadas_maquina = [cm for cj, cm in mesa]
        print("Tus cartas jugadas:")
        mostrar_cartas_horizontal(palos, jugadas_jugador)
        print("Cartas jugadas por la máquina:")
        mostrar_cartas_horizontal(palos, jugadas_maquina)
        print("--------------\n")
        if valor_truco(carta_jugador) < valor_truco(carta_maquina):
            ganadas_maquina += 1
        elif valor_truco(carta_jugador) > valor_truco(carta_maquina):
            ganadas_jugador += 1
        # Si alguien gana 2 manos, termina la ronda
        if ganadas_jugador == 2 or ganadas_maquina == 2:
            break
    print("\n=== MESA FINAL DE LA RONDA ===")
    jugadas_jugador = [cj for cj, cm in mesa]
    jugadas_maquina = [cm for cj, cm in mesa]
    print("Tus cartas jugadas:")
    mostrar_cartas_horizontal(palos, jugadas_jugador)
    print("Cartas jugadas por la máquina:")
    mostrar_cartas_horizontal(palos, jugadas_maquina)
    print("--------------\n")
    # Mostrar resultado y puntaje
    if truco_cantado_global:
        puntos_truco = 2
        print("Truco cantado! La mano vale 2 puntos.")
    if ganadas_jugador > ganadas_maquina:
        print(f"¡Ganaste la ronda! +{puntos_truco} puntos")
        puntos_jugador += puntos_truco
    elif ganadas_jugador < ganadas_maquina:
        print(f"La máquina gana la ronda. +{puntos_truco} puntos")
        puntos_maquina += puntos_truco
    else:
        print("Empate en Truco. Nadie suma puntos.")
    print(f"Puntaje actual: Jugador {puntos_jugador} - Máquina {puntos_maquina}")
    input("\nPresiona 'q' para continuar...")
    clear_console()
    return puntos_jugador, puntos_maquina

# --- main y ejecución ---
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

    # Mostrar varias cartas en horizontal
    def mostrar_cartas_horizontal(palos, mano):
        graficas = []
        for palo, num in mano:
            carta = palos.get(palo, {}).get(num)
            if carta:
                graficas.append(carta.splitlines())
            else:
                graficas.append([f"No se encontró la carta {num} de {palo}"])
        max_altura = max(len(g) for g in graficas)
        for i in range(len(graficas)):
            if len(graficas[i]) < max_altura:
                graficas[i] += [' ' * len(graficas[i][0])] * (max_altura - len(graficas[i]))
        for fila in range(max_altura):
            print('   '.join(graficas[c][fila] for c in range(len(graficas))))

    PALOS_TRUCO = ["Espadas", "Bastos", "Oros", "Copas"]
    VALORES_TRUCO = ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]
    JERARQUIA = [
        ("Espadas", "1"), ("Bastos", "1"), ("Espadas", "7"), ("Oros", "7"),
        ("Copas", "3"), ("Oros", "3"), ("Bastos", "3"), ("Espadas", "3"),
        ("Copas", "2"), ("Oros", "2"), ("Bastos", "2"), ("Espadas", "2"),
        ("Copas", "1"), ("Oros", "1"), ("Copas", "12"), ("Oros", "12"), ("Bastos", "12"), ("Espadas", "12"),
        ("Copas", "11"), ("Oros", "11"), ("Bastos", "11"), ("Espadas", "11"),
        ("Copas", "10"), ("Oros", "10"), ("Bastos", "10"), ("Espadas", "10"),
        ("Copas", "7"), ("Bastos", "7"), ("Copas", "6"), ("Oros", "6"), ("Bastos", "6"), ("Espadas", "6"),
        ("Copas", "5"), ("Oros", "5"), ("Bastos", "5"), ("Espadas", "5"),
        ("Copas", "4"), ("Oros", "4"), ("Bastos", "4"), ("Espadas", "4"),
    ]

    def valor_truco(carta):
        try:
            return JERARQUIA.index(carta)
        except ValueError:
            return 100

    def valor_envido(mano):
        valores = []
        for palo in PALOS_TRUCO:
            nums = [int(c[1]) if c[1] in ["10","11","12"] else int(c[1]) for c in mano if c[0]==palo]
            nums = [n if n<10 else 0 for n in nums]
            if len(nums)>=2:
                valores.append(sum(sorted(nums)[-2:]))
            elif len(nums)==1:
                valores.append(nums[0])
        return max(valores) if valores else 0

    def repartir():
        mazo = [(palo, valor) for palo in PALOS_TRUCO for valor in VALORES_TRUCO]
        random.shuffle(mazo)
        return mazo[:3], mazo[3:6]

    def mostrar_mano(palos, mano, jugador):
        print(f"\nMano de {jugador}:")
        etiquetas = [f"[{i+1}] {num} de {palo}" for i, (palo, num) in enumerate(mano)]
        print('   '.join(etiquetas))
        mostrar_cartas_horizontal(palos, mano)

    def elegir_carta(mano, puntos_jugador, puntos_maquina):
        global truco_cantado_global
        while True:
            eleccion = input("Elige la carta a tirar (1-3), 'truco' o 'puntos': ").strip().lower()
            if eleccion == "puntos":
                clear_console()
                print(f"Puntos actuales:\nJugador: {puntos_jugador} - Máquina: {puntos_maquina}")
                input("Presiona 'q' para volver al juego...")
                clear_console()
                continue
            if eleccion == "truco":
                if not truco_cantado_global:
                    truco_cantado_global = True
                    print("¡Truco cantado!")
                else:
                    print("Ya cantaste Truco en esta ronda.")
                continue
            try:
                eleccion_num = int(eleccion)
                if 1 <= eleccion_num <= len(mano):
                    return mano.pop(eleccion_num-1)
            except Exception:
                pass
            print("Opción inválida.")

    def turno_maquina(mano):
        idx = min(range(len(mano)), key=lambda i: valor_truco(mano[i]))
        return mano.pop(idx)

    def jugar_ronda(palos, puntos_jugador, puntos_maquina):
        mano_jugador, mano_maquina = repartir()
        mostrar_mano(palos, mano_jugador, "Jugador")
        puntos_truco = 1
        global truco_cantado_global
        truco_cantado_global = False
        mesa = []
        while True:
            r = input("¿Querés cantar algo? (truco/envido/nada/puntos): ").strip().lower()
            if r == "puntos":
                clear_console()
                print(f"Puntos actuales:\nJugador: {puntos_jugador} - Máquina: {puntos_maquina}")
                input("Presiona 'q' para volver al juego...")
                clear_console()
                continue
            if r == "envido":
                envido_jugador = valor_envido(mano_jugador)
                envido_maquina = valor_envido(mano_maquina)
                print(f"Tu envido: {envido_jugador}")
                print(f"Envido de la máquina: {envido_maquina}")
                if envido_jugador > envido_maquina:
                    print("¡Ganaste el envido! +2 puntos")
                    puntos_jugador += 2
                elif envido_jugador < envido_maquina:
                    print("La máquina gana el envido. +2 puntos")
                    puntos_maquina += 2
                else:
                    print("Empate en envido. Nadie suma puntos.")
                break
            if r == "truco":
                truco_cantado_global = True
                print("¡Truco cantado!")
                break
            if r == "nada" or r == "":
                break
        ganadas_jugador = ganadas_maquina = 0
        for turno in range(3):
            print(f"\nTurno {turno+1}:")
            mostrar_mano(palos, mano_jugador, "Jugador")
            carta_jugador = elegir_carta(mano_jugador, puntos_jugador, puntos_maquina)
            carta_maquina = turno_maquina(mano_maquina)
            mesa.append((carta_jugador, carta_maquina))
            print("\n--- Mesa ---")
            for i, (cj, cm) in enumerate(mesa):
                print(f"Turno {i+1}:")
                print("Jugador:")
                mostrar_cartas_horizontal(palos, [cj])
                print("Máquina:")
                mostrar_cartas_horizontal(palos, [cm])
                print("-")
            print("--------------\n")
            print(f"Tiraste: {carta_jugador[1]} de {carta_jugador[0]}")
            mostrar_cartas_horizontal(palos, [carta_jugador])
            print(f"La máquina tira: {carta_maquina[1]} de {carta_maquina[0]}")
            mostrar_cartas_horizontal(palos, [carta_maquina])
            if valor_truco(carta_jugador) < valor_truco(carta_maquina):
                print("¡Ganaste la mano!")
                ganadas_jugador += 1
            elif valor_truco(carta_jugador) > valor_truco(carta_maquina):
                print("La máquina gana la mano.")
                ganadas_maquina += 1

        if truco_cantado_global:
            puntos_truco = 2
            print("Truco cantado! La mano vale 2 puntos.")
        if ganadas_jugador > ganadas_maquina:
            print(f"¡Ganaste el Truco! +{puntos_truco} puntos")
            puntos_jugador += puntos_truco
        elif ganadas_jugador < ganadas_maquina:
            print(f"La máquina gana el Truco. +{puntos_truco} puntos")
            puntos_maquina += puntos_truco
        else:
            print("Empate en Truco. Nadie suma puntos.")
        return puntos_jugador, puntos_maquina

    # --- main y ejecución ---
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


# --- Lógica del Truco Argentino ---
import random

PALOS_TRUCO = ["Espadas", "Bastos", "Oros", "Copas"]
VALORES_TRUCO = ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]

# Jerarquía de Truco (mayor a menor)
JERARQUIA = [
    ("Espadas", "1"), ("Bastos", "1"), ("Espadas", "7"), ("Oros", "7"),
    ("Copas", "3"), ("Oros", "3"), ("Bastos", "3"), ("Espadas", "3"),
    ("Copas", "2"), ("Oros", "2"), ("Bastos", "2"), ("Espadas", "2"),
    ("Copas", "1"), ("Oros", "1"), ("Copas", "12"), ("Oros", "12"), ("Bastos", "12"), ("Espadas", "12"),
    ("Copas", "11"), ("Oros", "11"), ("Bastos", "11"), ("Espadas", "11"),
    ("Copas", "10"), ("Oros", "10"), ("Bastos", "10"), ("Espadas", "10"),
    ("Copas", "7"), ("Bastos", "7"), ("Copas", "6"), ("Oros", "6"), ("Bastos", "6"), ("Espadas", "6"),
    ("Copas", "5"), ("Oros", "5"), ("Bastos", "5"), ("Espadas", "5"),
    ("Copas", "4"), ("Oros", "4"), ("Bastos", "4"), ("Espadas", "4"),
]

def valor_truco(carta):
    try:
        return JERARQUIA.index(carta)
    except ValueError:
        return 100  # Menor valor si no está

def valor_envido(mano):
    # Suma de dos cartas del mismo palo, 10-12 valen 0
    valores = []
    for palo in PALOS_TRUCO:
        nums = [int(c[1]) if c[1] in ["10","11","12"] else int(c[1]) for c in mano if c[0]==palo]
        nums = [n if n<10 else 0 for n in nums]
        if len(nums)>=2:
            valores.append(sum(sorted(nums)[-2:]))
        elif len(nums)==1:
            valores.append(nums[0])
    return max(valores) if valores else 0

def repartir():
    mazo = [(palo, valor) for palo in PALOS_TRUCO for valor in VALORES_TRUCO]
    random.shuffle(mazo)
    return mazo[:3], mazo[3:6]

def mostrar_mano(palos, mano, jugador):
    print(f"\nMano de {jugador}:")
    etiquetas = [f"[{i+1}] {num} de {palo}" for i, (palo, num) in enumerate(mano)]
    print('   '.join(etiquetas))
    mostrar_cartas_horizontal(palos, mano)

def elegir_carta(mano, puntos_jugador, puntos_maquina):
    global truco_cantado_global
    while True:
        eleccion = input("Elige la carta a tirar (1-3), 'truco' o 'puntos': ").strip().lower()
        if eleccion == "puntos":
            clear_console()
            print(f"Puntos actuales:\nJugador: {puntos_jugador} - Máquina: {puntos_maquina}")
            input("Presiona 'q' para volver al juego...")
            clear_console()
            continue
        if eleccion == "truco":
            if not truco_cantado_global:
                truco_cantado_global = True
                print("¡Truco cantado!")
            else:
                print("Ya cantaste Truco en esta ronda.")
            continue
        try:
            eleccion_num = int(eleccion)
            if 1 <= eleccion_num <= len(mano):
                return mano.pop(eleccion_num-1)
        except Exception:
            pass
        print("Opción inválida.")

def turno_maquina(mano):
    # Máquina tira la carta más baja
    idx = min(range(len(mano)), key=lambda i: valor_truco(mano[i]))
    return mano.pop(idx)

def cantar_envido():
    while True:
        r = input("¿Querés cantar Envido? (s/n): ").lower()
        if r in ["s", "n"]:
            return r == "s"

def cantar_truco():
    while True:
        r = input("¿Querés cantar Truco? (s/n): ").lower()
        if r in ["s", "n"]:
            return r == "s"

def jugar_ronda(palos, puntos_jugador, puntos_maquina):
    mano_jugador, mano_maquina = repartir()
    mostrar_mano(palos, mano_jugador, "Jugador")
    # Limpiar consola antes del prompt de canto
    def clear_console():
        import os
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print("\033[2J\033[H", end='')

    puntos_truco = 1
    global truco_cantado_global
    truco_cantado_global = False
    mesa = []  # [(carta_jugador, carta_maquina)]
    # Envido y Truco: prompt unificado
    while True:
        r = input("¿Querés cantar algo? (truco/envido/nada/puntos): ").strip().lower()
        if r == "puntos":
            clear_console()
            print(f"Puntos actuales:\nJugador: {puntos_jugador} - Máquina: {puntos_maquina}")
            input("Presiona 'q' para volver al juego...")
            clear_console()
            continue
        if r == "envido":
            envido_jugador = valor_envido(mano_jugador)
            envido_maquina = valor_envido(mano_maquina)
            print(f"Tu envido: {envido_jugador}")
            print(f"Envido de la máquina: {envido_maquina}")
            if envido_jugador > envido_maquina:
                print("¡Ganaste el envido! +2 puntos")
                puntos_jugador += 2
            elif envido_jugador < envido_maquina:
                print("La máquina gana el envido. +2 puntos")

                puntos_maquina += 2
            else:
                print("Empate en envido. Nadie suma puntos.")
            break
        if r == "truco":
            truco_cantado_global = True
            print("¡Truco cantado!")
            break
        if r == "nada" or r == "":
            break
    # Truco ahora se puede cantar en elegir_carta
    # Si se cantó truco, la mano vale 2 puntos
    # Juego de cartas
    ganadas_jugador = ganadas_maquina = 0
    for turno in range(3):
        print(f"\nTurno {turno+1}:")
        mostrar_mano(palos, mano_jugador, "Jugador")
        carta_jugador = elegir_carta(mano_jugador, puntos_jugador, puntos_maquina)
        carta_maquina = turno_maquina(mano_maquina)
        mesa.append((carta_jugador, carta_maquina))
        # Mostrar mesa con cartas dibujadas
        print("\n--- Mesa ---")
        for i, (cj, cm) in enumerate(mesa):
            print(f"Turno {i+1}:")
            print("Jugador:")
            mostrar_cartas_horizontal(palos, [cj])
            print("Máquina:")
            mostrar_cartas_horizontal(palos, [cm])
            print("-")
        print("--------------\n")
        print(f"Tiraste: {carta_jugador[1]} de {carta_jugador[0]}")
        mostrar_cartas_horizontal(palos, [carta_jugador])
        print(f"La máquina tira: {carta_maquina[1]} de {carta_maquina[0]}")
        mostrar_cartas_horizontal(palos, [carta_maquina])
        if valor_truco(carta_jugador) < valor_truco(carta_maquina):
            print("¡Ganaste la mano!")
            ganadas_jugador += 1
        elif valor_truco(carta_jugador) > valor_truco(carta_maquina):
            print("La máquina gana la mano.")
            ganadas_maquina += 1

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
