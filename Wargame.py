
import random

# Datos base de perfiles
PERFILES = {
    "Asalto":      {"ataque": 8, "defensa": 4, "hp": 18, "costo": 10},
    "Táctico":     {"ataque": 6, "defensa": 6, "hp": 20, "costo": 10},
    "Devastador":  {"ataque": 9, "defensa": 3, "hp": 16, "costo": 12},
    "Explorador":  {"ataque": 4, "defensa": 8, "hp": 18, "costo": 8}
}

NOMBRES_MARINES = [
    "Hermano Baltar", "Sargento Vortan", "Lexicanum Kain", "Capitán Rhael",
    "Hermano Lucien", "Hermano Kael", "Apotecario Tyros", "Veterano Drevan",
    "Sargento Morth", "Explorador Fenix"
]

class Marine:
    def __init__(self, tipo):
        stats = PERFILES[tipo]
        self.nombre = random.choice(NOMBRES_MARINES)
        self.tipo = tipo
        self.ataque_base = stats["ataque"]
        self.defensa_base = stats["defensa"]
        self.hp = stats["hp"]
        self.vivo = True

    def recibir_daño(self, daño):
        self.hp -= daño
        if self.hp <= 0:
            self.vivo = False
            self.hp = 0

    def lanzar_ataque(self):
        return random.randint(1, 6) + self.ataque_base

    def lanzar_defensa(self):
        return random.randint(1, 6) + self.defensa_base

def elegir_escuadra(nombre, puntos_maximos=30):
    print(f"\n{nombre}, construye tu escuadra (máximo {puntos_maximos} puntos):")
    escuadra = []
    total_puntos = 0

    opciones = {
        "1": "Asalto",
        "2": "Táctico",
        "3": "Devastador",
        "4": "Explorador"
    }
    while len(escuadra) < 3:
        print("Opciones:")
        for n, perfil in PERFILES.items():
            print(f"- {n} (Ataque {perfil['ataque']}, Defensa {perfil['defensa']}, HP {perfil['hp']}, Costo {perfil['costo']})")
        eleccion_num = input(f"Elige al marine #{len(escuadra) + 1} (1-4): ")

        if eleccion_num not in opciones:
            print("Opción inválida.")
            continue

        eleccion = opciones[eleccion_num]
        costo = PERFILES[eleccion]["costo"]
        if total_puntos + costo > puntos_maximos:
            print(f"¡Esa elección supera el límite de {puntos_maximos} puntos! Te quedan {puntos_maximos - total_puntos}.")
            continue

        nuevo_marine = Marine(eleccion)
        escuadra.append(nuevo_marine)
        total_puntos += costo
        print(f"{nuevo_marine.nombre} ({eleccion}) agregado. Puntos usados: {total_puntos}/{puntos_maximos}")

    return escuadra

def jugar_round(j1_nombre, j1_escuadra, j2_nombre, j2_escuadra, ronda):
    print(f"\n--- RONDA {ronda} ---")

    vivos1 = [m for m in j1_escuadra if m.vivo]
    vivos2 = [m for m in j2_escuadra if m.vivo]

    atk1 = sum(m.lanzar_ataque() for m in vivos1)
    def1 = sum(m.lanzar_defensa() for m in vivos1)

    atk2 = sum(m.lanzar_ataque() for m in vivos2)
    def2 = sum(m.lanzar_defensa() for m in vivos2)

    daño_a_j1 = max(0, atk2 - def1)
    daño_a_j2 = max(0, atk1 - def2)

    print(f"{j1_nombre} ataque total: {atk1} | defensa: {def1}")
    print(f"{j2_nombre} ataque total: {atk2} | defensa: {def2}")
    print(f"{j1_nombre} recibe {daño_a_j1} de daño.")
    print(f"{j2_nombre} recibe {daño_a_j2} de daño.")

    distribuir_daño(vivos1, daño_a_j1)
    distribuir_daño(vivos2, daño_a_j2)

def distribuir_daño(escuadra, daño):
    if not escuadra or daño == 0:
        return
    daño_por_marine = daño // len(escuadra)
    for marine in escuadra:
        marine.recibir_daño(daño_por_marine)

def estado_escuadra(nombre, escuadra):
    print(f"\n{nombre} - Estado de la escuadra:")
    for i, m in enumerate(escuadra, 1):
        estado = "💀 Muerto" if not m.vivo else f"❤️ {m.hp} HP"
        print(f"  {i}. {m.nombre} ({m.tipo}) - {estado}")

def contar_victorias(escuadra):
    return sum(1 for m in escuadra if m.vivo)

def main():
    print("🔥 Batalla de Space Marines por escuadras 🔥")
    j1 = input("Jugador 1, ingresa tu nombre: ")
    j2 = input("Jugador 2, ingresa tu nombre: ")

    esc1 = elegir_escuadra(j1)
    esc2 = elegir_escuadra(j2)

    for ronda in range(1, 4):
        jugar_round(j1, esc1, j2, esc2, ronda)
        estado_escuadra(j1, esc1)
        estado_escuadra(j2, esc2)

    vivos_j1 = contar_victorias(esc1)
    vivos_j2 = contar_victorias(esc2)

    print("\n=== RESULTADO FINAL ===")
    print(f"{j1} tiene {vivos_j1} marines vivos.")
    print(f"{j2} tiene {vivos_j2} marines vivos.")
    if vivos_j1 > vivos_j2:
        print(f"🏆 ¡{j1} gana!")
        ganador = j1
    elif vivos_j2 > vivos_j1:
        print(f"🏆 ¡{j2} gana!")
        ganador = j2
    else:
        print("🤝 ¡Empate!")
        ganador = "Empate"

    with open("estadisticas_victoria.txt", "a") as f:
        f.write(f"Ganador: {ganador}\n")

if __name__ == "__main__":
    main()


print("Gracias por jugar. ¡Hasta la próxima batalla!")  
 
