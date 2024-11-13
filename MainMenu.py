import pygame
import sys
import os
import random
import quiz
import subprocess


pygame.init()

window_size = (640, 640)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Delphi Enigma")

BLANCO = (255, 255, 255)
GRIS_CLARO = (200, 200, 200)
board_color = (245, 245, 220) 
AZUL = (0, 0, 255) 
ROJO = (255, 0, 0) 
VERDE = (0, 255, 0)  


ruta_imagen_menu = os.path.join(os.getcwd(), "MainMenuWT.png")
menu = pygame.image.load(ruta_imagen_menu)
menu = pygame.transform.scale(menu, window_size)

ruta_imagen_tablero = os.path.join(os.getcwd(), "tablero.png")
tablero = pygame.image.load(ruta_imagen_tablero)
tablero = pygame.transform.scale(tablero, window_size)


font = pygame.font.Font(None, 48)


grid_size = 4 
board_width = 493  
board_height = 493 
cell_width = board_width // grid_size
cell_height = board_height // grid_size


board_x = (window_size[0] - board_width) // 2
board_y = (window_size[1] - board_height) // 2

opciones = ["Jugar", "Salir"]
opcion_seleccionada = 0  

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.casilla = (0, 0)
        self.vidas = 1

    def asignarCasillaRandom(self):
        self.casilla = (random.randint(0, 3), random.randint(0, 3))

class Enemigo:
    def __init__(self, casilla, tema=None):
        self.casilla = casilla
        self.tema = tema


jugador = Jugador("Jugador 1")
jugador.asignarCasillaRandom()

enemigos = []
for fila in range(4):
    for col in range(4):
        if (fila, col) != jugador.casilla:
            enemigos.append(Enemigo((fila, col)))


enemigo_seleccionado = None

def enemigos_adyacentes(jugador, enemigos):
    x, y = jugador.casilla
    posiciones_adyacentes = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return [enemigo for enemigo in enemigos if enemigo.casilla in posiciones_adyacentes]

def dibujar_tablero():
    screen.blit(tablero, (0, 0))
    
 
    for row in range(grid_size):
        for col in range(grid_size):
            x = board_x + col * cell_width
            y = board_y + row * cell_height + 7
            rect = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, board_color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  

            if (row, col) == jugador.casilla:
                pygame.draw.circle(screen, AZUL, rect.center, cell_width // 4)

            for enemigo in enemigos:
                if enemigo.casilla == (row, col):
                    color = VERDE if enemigo == enemigo_seleccionado else ROJO
                    pygame.draw.circle(screen, color, rect.center, cell_width // 4)

def dibujar_menu():
    screen.blit(menu, (0, 0))
    
    for i, opcion in enumerate(opciones):
        color = BLANCO if i == opcion_seleccionada else GRIS_CLARO
        texto = font.render(opcion, True, color)
        text_rect = texto.get_rect(center=(window_size[0] // 2, 300 + i * 60))
        screen.blit(texto, text_rect)

def manejar_eventos_menu():
    global en_menu, opcion_seleccionada
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_DOWN:
                opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
            elif evento.key == pygame.K_UP:
                opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
            elif evento.key == pygame.K_RETURN:
                if opcion_seleccionada == 0:  # Jugar
                    en_menu = False
                elif opcion_seleccionada == 1:  # Salir
                    pygame.quit()
                    sys.exit()

enemigos_adyacentes_lista = enemigos_adyacentes(jugador, enemigos)
if enemigos_adyacentes_lista:
    enemigo_quiz = random.choice(enemigos_adyacentes_lista)
    enemigo_quiz.tema = "Quiz"

def manejar_eventos_juego():
    global enemigo_seleccionado
    adyacentes = enemigos_adyacentes(jugador, enemigos)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                global en_menu
                en_menu = True
            elif evento.key == pygame.K_DOWN:
                if adyacentes:
                    if enemigo_seleccionado in adyacentes:
                        indice = adyacentes.index(enemigo_seleccionado)
                        enemigo_seleccionado = adyacentes[(indice + 1) % len(adyacentes)]
                    else:
                        enemigo_seleccionado = adyacentes[0]
            elif evento.key == pygame.K_UP:
                if adyacentes:
                    if enemigo_seleccionado in adyacentes:
                        indice = adyacentes.index(enemigo_seleccionado)
                        enemigo_seleccionado = adyacentes[(indice - 1) % len(adyacentes)]
                    else:
                        enemigo_seleccionado = adyacentes[-1]
            elif evento.key == pygame.K_RETURN:
                if enemigo_seleccionado and enemigo_seleccionado.tema:
                    resultado_quiz = quiz.main()  # Llama a quiz y guarda el resultado
                    if resultado_quiz == 'WIN':
                        jugador.vidas += 1
                    elif resultado_quiz == 'LOSE':
                        pass
                   



en_menu = True


while True:
    if en_menu:
        manejar_eventos_menu()
        dibujar_menu()
    else:
        manejar_eventos_juego()
        dibujar_tablero()
        
    pygame.display.flip()
