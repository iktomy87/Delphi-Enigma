
import random

class Movimiento:
    def __init__(self, nombre, poder):
        self.nombre = nombre
        self.poder = poder
    
    def usarMovimiento(self, atacante, defensor):
        danio = self.poder
        defensor.vida -= danio
        print(f"{atacante.nombre} usó {self.nombre} y causó {danio} de daño a {defensor.nombre}.")
        if defensor.vida <= 0:
            print(f"{defensor.nombre} ha sido derrotado!")


class Bestia:
    def __init__(self, nombre, vida, movimientos):
        self.nombre = nombre
        self.vida = vida
        self.movimientos = movimientos
    
    def seleccionarMov(self, esRobot):
        if esRobot:
            return self.movimientos[random.randint(0, 2)]
        else:
            print("Selecciona un movimiento:")
            #imprime los movimientos en forma enumerada
            for idx, mov in enumerate(self.movimientos):
                print(f"{idx + 1}. {mov.nombre} (Poder: {mov.poder})")
            #Selecciona un movimiento
            while True:
                try:
                    eleccion = int(input("Ingresa el número del movimiento: ")) - 1
                    if 0 <= eleccion < len(self.movimientos):
                        return self.movimientos[eleccion]
                    else:
                        print("Selección no válida. Inténtalo de nuevo.")
                except ValueError:
                    print("Por favor, ingresa un número válido.")

        
        
class Jugador:
    def __init__(self, nombre, bestia,esRobot):
        self.nombre = nombre
        self.bestia = bestia
        self.esRobot = esRobot


class Batalla:
    def __init__(self, jugador1, jugador2):
        self.jugador1 = jugador1
        self.jugador2 = jugador2
    
    def iniciar_batalla(self):
        print("¡La batalla ha comenzado!")
        while self.jugador1.bestia.vida > 0 and self.jugador2.bestia.vida > 0:
            
            self.turno(self.jugador1, self.jugador2)
            if self.jugador2.bestia.vida <= 0:
                print(f"¡{self.jugador1.nombre} gana la batalla!")
                break

            self.turno(self.jugador2, self.jugador1)
            if self.jugador1.bestia.vida <= 0:
                print(f"¡{self.jugador2.nombre} gana la batalla!")
                break

    def turno(self, jugador, oponente):
        print(f"Turno de {jugador.nombre} con {jugador.bestia.nombre} (Vida: {jugador.bestia.vida})")
        movimiento = jugador.bestia.seleccionarMov(jugador.esRobot)
        movimiento.usarMovimiento(jugador.bestia, oponente.bestia)

#Movimientos
#Pegaso
patada = Movimiento("Patada baja", 30)
viento = Movimiento("Viento de Eolo", 40)
rayo = Movimiento("Rayo Olímpico", 85)



#Quimera
alientoDr = Movimiento("Aliento de Dragon", 50)
cabezaso = Movimiento("Envestida de Cabra", 30)
rugido = Movimiento("Rugido del León", 20)


#Bestias
pegazo = Bestia("Pegazo", vida=100, movimientos=[patada, viento, rayo])
quimera = Bestia("Quimera", vida=100, movimientos=[alientoDr, cabezaso, rugido])

#Jugadores 
jugador1 = Jugador("Bellerofonte", pegazo, False)
cpu = Jugador("Equidna", quimera, True)

batalla = Batalla(jugador1, cpu)
batalla.iniciar_batalla()