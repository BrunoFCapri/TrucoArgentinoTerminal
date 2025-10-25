import os

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print("\033[2J\033[H", end='')

def cargar_cartas(path):
    with open(path, encoding='utf-8') as f:
        contenido = f.read()
    palos = {}
    secciones = contenido.split('Palo de ')
    for sec in secciones[1:]:
        palo, cartas = sec.split('(', 1)
        palo = palo.strip()
        cartas = cartas.split(')', 1)[1]
        cartas_graficas = cartas.split('+--------+')
        cartas_graficas = [c for c in cartas_graficas if c.strip()]
        palos[palo] = {}
        for carta in cartas_graficas:
            lineas = carta.strip().splitlines()
            if lineas:
                num = lineas[0].replace('|','').strip()
                palos[palo][num] = '+--------+\n' + carta.strip() + '\n+--------+'
    return palos

def mostrar_carta(palos, palo, num):
    carta = palos.get(palo, {}).get(num)
    if carta:
        print(carta)
    else:
        print(f"No se encontró la carta {num} de {palo}")
