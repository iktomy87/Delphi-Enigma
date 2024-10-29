import pygame
import sys
import os
import random

pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
CREMA = (219, 203, 158)
AZUL = (0, 0, 255) 
ROJO = (255, 0, 0) 
VERDE = (0, 255, 0)  

ANCHO, ALTO = 640, 640
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Delphi Enigma")

ruta_imagen = os.path.join(os.getcwd(), "MainMenuWT.png")
fondo = pygame.image.load(ruta_imagen)
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

fuente = pygame.font.Font(None, 30)


filas, columnas = 8, 8
tam_celda = ANCHO // columnas


class Tema:
    def __init__(self, nombre, preguntas_respuestas):
        self.nombre = nombre
        self.preguntas_respuestas = preguntas_respuestas

    def obtener_pregunta_aleatoria(self):
        return random.choice(self.preguntas_respuestas)


TEMAS = {
    "Historia": Tema("Historia", [
        {"pregunta": "¿Quién fue el primer presidente?", "respuesta": "George Washington", "opciones": ["Abraham Lincoln", "George Washington", "Thomas Jefferson"]},
        {"pregunta": "¿En qué año fue la Revolución Francesa?", "respuesta": "1789", "opciones": ["1789", "1776", "1804"]}
    ]),
    "Ciencia": Tema("Ciencia", [
        {"pregunta": "¿Cuál es la fórmula del agua?", "respuesta": "H2O", "opciones": ["H2O", "O2", "CO2"]},
        {"pregunta": "¿Qué planeta es el más grande del sistema solar?", "respuesta": "Júpiter", "opciones": ["Tierra", "Júpiter", "Marte"]}
    ])
}


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.casilla = (0, 0)

    def asignarCasillaRandom(self):
        self.casilla = (random.randint(0, filas - 1), random.randint(0, columnas - 1))

class Enemigo:
    def __init__(self, casilla, tema):
        self.casilla = casilla
        self.tema = tema
        pregunta_y_respuesta = tema.obtener_pregunta_aleatoria()
        self.pregunta = pregunta_y_respuesta["pregunta"]
        self.respuesta = pregunta_y_respuesta["respuesta"]
        self.opciones = pregunta_y_respuesta["opciones"]


jugador = Jugador("Jugador 1")
jugador.asignarCasillaRandom()


enemigos = []
for fila in range(filas):
    for col in range(columnas):
        if (fila, col) != jugador.casilla:
            tema = random.choice(list(TEMAS.values()))
            enemigos.append(Enemigo((fila, col), tema))


def enemigos_adyacentes(jugador, enemigos):
    x, y = jugador.casilla
    posiciones_adyacentes = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return [enemigo for enemigo in enemigos if enemigo.casilla in posiciones_adyacentes]


def dibujar_menu():
    pantalla.blit(fondo, (0, 0))
    opciones = ["Jugar", "Salir"]
    for i, opcion in enumerate(opciones):
        color = BLANCO if i == 0 else (100, 100, 100)
        texto = fuente.render(opcion, True, color)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 200 + i * 60))

def manejar_eventos_menu():
    global en_menu
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            en_menu = False

def pantalla_juego():
    pantalla.fill(CREMA)
    for fila in range(filas):
        for col in range(columnas):
            rect = pygame.Rect(col * tam_celda, fila * tam_celda, tam_celda, tam_celda)
            pygame.draw.rect(pantalla, NEGRO, rect, 1)
         
            if (fila, col) == jugador.casilla:
                pygame.draw.circle(pantalla, AZUL, rect.center, tam_celda // 4)

            for enemigo in enemigos:
                if enemigo.casilla == (fila, col):
                    color = VERDE if enemigo == enemigo_seleccionado else ROJO
                    pygame.draw.circle(pantalla, color, rect.center, tam_celda // 4)

def manejar_eventos_juego():
    global enemigo_seleccionado, en_duelo
    adyacentes = enemigos_adyacentes(jugador, enemigos)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:  
                global en_menu
                en_menu = True
            elif evento.key == pygame.K_RETURN and enemigo_seleccionado:
                en_duelo = True
            elif evento.key == pygame.K_DOWN:
                indice = adyacentes.index(enemigo_seleccionado)
                enemigo_seleccionado = adyacentes[(indice + 1) % len(adyacentes)]
            elif evento.key == pygame.K_UP:
                indice = adyacentes.index(enemigo_seleccionado)
                enemigo_seleccionado = adyacentes[(indice - 1) % len(adyacentes)]


opcion_seleccionada = 0
def pantalla_duelo(enemigo):
    pantalla.fill(BLANCO)
    pregunta = fuente.render(enemigo.pregunta, True, NEGRO)
    pantalla.blit(pregunta, (20, 50))
    for i, opcion in enumerate(enemigo.opciones):
        color = VERDE if i == opcion_seleccionada else NEGRO
        opcion_texto = fuente.render(opcion, True, color)
        pantalla.blit(opcion_texto, (20, 150 + i * 40))

def manejar_eventos_duelo():
    global opcion_seleccionada, en_duelo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                opcion_seleccionada = (opcion_seleccionada - 1) % len(enemigo_seleccionado.opciones)
            elif evento.key == pygame.K_DOWN:
                opcion_seleccionada = (opcion_seleccionada + 1) % len(enemigo_seleccionado.opciones)
            elif evento.key == pygame.K_RETURN:
                en_duelo = False

en_menu = True
en_duelo = False
enemigo_seleccionado = None

while True:
    if en_menu:
        manejar_eventos_menu()
        dibujar_menu()
    elif en_duelo and enemigo_seleccionado:
        manejar_eventos_duelo()
        pantalla_duelo(enemigo_seleccionado)
    else:
        manejar_eventos_juego()
        pantalla_juego()
        
        adyacentes = enemigos_adyacentes(jugador, enemigos)
        if adyacentes and enemigo_seleccionado is None:
            enemigo_seleccionado = adyacentes[0]  

    pygame.display.flip()
