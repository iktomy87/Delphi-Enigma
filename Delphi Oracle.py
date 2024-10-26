import pygame
import sys
import os

pygame.init()

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
CREMA = (219, 203, 158)

TEMAS = ["Historia", "Ciencia", "Arte", "Deporte", "Geografía", "Matemática", "Literatura", "Tecnología", "Entretenimiento"]



ANCHO, ALTO = 640, 640
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Delphi Enigma")

# Cargar la imagen de fondo desde el directorio actual
ruta_imagen = os.path.join(os.getcwd(), "MainMenuWT.png")
fondo = pygame.image.load(ruta_imagen)
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))


fuente = pygame.font.Font(None, 50)


opciones = ["Jugar", "Salir"]
opcion_seleccionada = 0
en_menu = True  

def dibujar_menu():
    pantalla.blit(fondo, (0, 0))
    for i, opcion in enumerate(opciones):
        color = BLANCO if i == opcion_seleccionada else (100, 100, 100)
        texto = fuente.render(opcion, True, color)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 200 + i * 60))

def manejar_eventos_menu():
    global opcion_seleccionada, en_menu
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
            elif evento.key == pygame.K_DOWN:
                opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
            elif evento.key == pygame.K_RETURN:
                if opciones[opcion_seleccionada] == "Jugar":
                    en_menu = False  
                elif opciones[opcion_seleccionada] == "Salir":
                    pygame.quit()
                    sys.exit()

# Función para dibujar el tablero de 8x8
def pantalla_juego():
    pantalla.fill(CREMA)
    filas, columnas = 8, 8
    tam_celda = ANCHO // columnas
    
    for fila in range(filas):
        for col in range(columnas):
            rect = pygame.Rect(col * tam_celda, fila * tam_celda, tam_celda, tam_celda)
            pygame.draw.rect(pantalla, NEGRO, rect, 1)

def manejar_eventos_juego():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:  
                global en_menu
                en_menu = True


while True:
    if en_menu:
        manejar_eventos_menu()
        dibujar_menu()
    else:
        manejar_eventos_juego()
        pantalla_juego()
        
    pygame.display.flip()
