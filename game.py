import random
from utils import clear_console, cargar_cartas, mostrar_carta

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
        eleccion = input("Elige la carta a tirar (1-3), 'truco', 'puntos' o 'mazo': ").strip().lower()
        if eleccion == "puntos":
            clear_console()
            print(f"Puntos actuales:\nJugador: {puntos_jugador} - Máquina: {puntos_maquina}")
            input("Presiona 'q' para volver al juego...")
            clear_console()
            # Volver a mostrar la mesa y la mano antes de pedir carta
            # Mostrar la mesa y la mano con el mismo formato que el resto del juego
            print("\n--- Mesa ---")
            if mazo_descartado:
                print("Tus cartas jugadas:")
                # Mostrar primero las cartas del jugador
                jugadas_jugador = mazo_descartado[::2] if len(mazo_descartado) > 0 else []
                mostrar_cartas_horizontal(palos, jugadas_jugador)
                print("Cartas jugadas por la máquina:")
                jugadas_maquina = mazo_descartado[1::2] if len(mazo_descartado) > 1 else []
                mostrar_cartas_horizontal(palos, jugadas_maquina)
                print("--------------\n")
            mostrar_mano(palos, mano, "Jugador")
            continue
        if eleccion == "mazo":
            clear_console()
            print("Te fuiste al mazo. La máquina gana la ronda y suma 1 punto.")
            input("Presiona 'q' para continuar...")
            clear_console()
            # Señal especial para terminar la ronda
            return None
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
    # Prompt de canto antes de tirar carta
    carta_directa = None
    while True:
        canto = input("¿Querés cantar algo? (envido/real envido/falta envido/flor/truco/nada/puntos/mazo): ").strip().lower()
        # Si el usuario ingresa un número, lo toma como 'nada' y juega la carta directamente
        try:
            eleccion_num = int(canto)
            if 1 <= eleccion_num <= len(mano_jugador):
                carta_directa = mano_jugador.pop(eleccion_num-1)
                break
        except Exception:
            pass
        if canto == "puntos":
            clear_console()
            print(f"Puntos actuales:\nJugador: {puntos_jugador} - Máquina: {puntos_maquina}")
            input("Presiona 'q' para volver al juego...")
            clear_console()
            # Volver al prompt de canto, no avanzar turno
            continue
        if canto == "mazo":
            clear_console()
            print("Te fuiste al mazo. La máquina gana la ronda y suma 1 punto.")
            print("\n=== MESA FINAL DE LA RONDA ===")
            if mesa:
                jugadas_jugador = [cj for cj, cm in mesa]
                jugadas_maquina = [cm for cj, cm in mesa]
                print("Tus cartas jugadas:")
                mostrar_cartas_horizontal(palos, jugadas_jugador)
                print("Cartas jugadas por la máquina:")
                mostrar_cartas_horizontal(palos, jugadas_maquina)
                print("--------------\n")
            else:
                print("(No se jugó ninguna carta en esta ronda)")
            print(f"Puntaje actual: Jugador {puntos_jugador} - Máquina {puntos_maquina + 1}")
            input("Presiona 'q' para continuar...")
            clear_console()
            return puntos_jugador, puntos_maquina + 1
        if canto == "truco":
            if not truco_cantado_global:
                truco_cantado_global = True
                print("¡Truco cantado!")
            else:
                print("Ya cantaste Truco en esta ronda.")
            continue
        if canto == "envido":
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
        if canto == "real envido":
            envido_jugador = valor_envido(mano_jugador)
            envido_maquina = valor_envido(mano_maquina)
            print(f"Tu real envido: {envido_jugador}")
            print(f"Real envido de la máquina: {envido_maquina}")
            if envido_jugador > envido_maquina:
                print("¡Ganaste el real envido! +3 puntos")
                puntos_jugador += 3
            elif envido_jugador < envido_maquina:
                print("La máquina gana el real envido. +3 puntos")
                puntos_maquina += 3
            else:
                print("Empate en real envido. Nadie suma puntos.")
            break
        if canto == "falta envido":
            envido_jugador = valor_envido(mano_jugador)
            envido_maquina = valor_envido(mano_maquina)
            falta = 15 - max(puntos_jugador, puntos_maquina)
            print(f"Tu falta envido: {envido_jugador}")
            print(f"Falta envido de la máquina: {envido_maquina}")
            if envido_jugador > envido_maquina:
                print(f"¡Ganaste la falta envido! +{falta} puntos")
                puntos_jugador += falta
            elif envido_jugador < envido_maquina:
                print(f"La máquina gana la falta envido. +{falta} puntos")
                puntos_maquina += falta
            else:
                print("Empate en falta envido. Nadie suma puntos.")
            break
        if canto == "flor":
            palos_mano = [p for p, n in mano_jugador]
            if palos_mano.count(palos_mano[0]) == 3:
                print("¡Flor! +3 puntos")
                puntos_jugador += 3
            else:
                print("No tienes flor (tres cartas del mismo palo)")
            break
        if canto == "nada":
            break
        print("Opción inválida.")
    # Ronda de juego
    for turno in range(3):
        print(f"\nTurno {turno+1}:")
        # Mostrar la mesa antes de jugar
        print("\n--- Mesa ---")
        if mesa:
            jugadas_jugador = [cj for cj, cm in mesa]
            jugadas_maquina = [cm for cj, cm in mesa]
            print("Tus cartas jugadas:")
            mostrar_cartas_horizontal(palos, jugadas_jugador)
            print("Cartas jugadas por la máquina:")
            mostrar_cartas_horizontal(palos, jugadas_maquina)
            print("--------------\n")
        else:
            print("(La mesa está vacía)")
        # Mostrar la mano antes de elegir carta
        mostrar_mano(palos, mano_jugador, "Jugador")
        if carta_directa:
            carta_jugador = carta_directa
            carta_directa = None
        else:
            carta_jugador = elegir_carta(palos, mano_jugador, puntos_jugador, puntos_maquina, mazo_descartado)
            if carta_jugador is None:
                # El jugador se fue al mazo, terminar la ronda
                return puntos_jugador, puntos_maquina + 1
        mazo_descartado.append(carta_jugador)
        carta_maquina = turno_maquina(mano_maquina)
        mazo_descartado.append(carta_maquina)
        mesa.append((carta_jugador, carta_maquina))
        if valor_truco(carta_jugador) < valor_truco(carta_maquina):
            ganadas_maquina += 1
        elif valor_truco(carta_jugador) > valor_truco(carta_maquina):
            ganadas_jugador += 1
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
