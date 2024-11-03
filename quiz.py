import pygame
import sys
import os
import random


def main():
    pygame.init()

    window_size = (640, 640)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Quiz")

    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    VERDE = (0, 255, 0)

    ruta_imagen_quiz = os.path.join(os.getcwd(), "academia.png")
    img_quiz = pygame.image.load(ruta_imagen_quiz)
    img_quiz = pygame.transform.scale(img_quiz, window_size)

    fuente = pygame.font.Font(None, 23)

    PREGUNTAS = [
        "¿Por morder qué fruta no se le permitió a Perséfone abandonar el Hades?",
        "¿Quién ejerció como juez en la disputa entre Hera, Atenea y Afrodita?",
        "¿Qué nombre pusieron los romanos al dios griego Hefesto?",
        "¿Qué hizo Aquiles para evitar acudir a la guerra de Troya?",
        "¿Cuál de estos montes no pertenece a la mitología griega?",
        "¿Cómo se llamaba a las sacerdotisas de Dionisio?",
        "¿Cuál de estas divinidades no era hermana de las otras tres?",
        "¿De quién se protegía Odiseo atándose al mástil de su barco?",
        "¿Qué mito representa «Las hilanderas» de Velázquez?",
        "¿Cuál de estos dioses no tiene un planeta a su nombre en el sistema solar?",
        "¿Qué nombre recibía el cetro de Hermes?",
        "¿Quién compitió y perdió contra Atenea por el patronazgo de Atenas?",
        "¿Cuál de estos enfrentamientos ocurrió antes?",
        "¿Cómo se llamaba el abuelo de Zeus?",
    ]

    OPCIONES = [
        ("A. Una manzana", "B. Un pomelo", "C. Una Granada", "D. Un arándano"),
        ("A. Héctor", "B. Agamenón", "C. Paris", "D. Aquiles"),
        ("A. Baco", "B. Febo", "C. Vulcano", "D. Plutón"),
        ("A. Se hizo pasar por mujer", "B. Se escondió en la cueva del centauro Quirón", "C. Le pidió a su madre que lo convirtiera en una constelación", "D. Se embarcó con los Argonautas"),
        ("A. El monte Parnaso", "B. El Monte Olimpo", "C. El monte Ida", "D. El monte Ararat"),
        ("A. Pitonisas, por la serpiente Pitón", "B. Ménades y bacantes", "C. Amazonas", "D. Hespérides e Hiperbóreas"),
        ("A. Atenea", "B. Hermes", "C. Poseidón", "D. Artemisa"),
        ("A. De las esfinges", "B. De las sirenas", "C. De las hidras", "D. De las quimeras"),
        ("A. El de Medea", "B. El de Ío", "C. El de Aracne", "D. El de Europa"),
        ("A. Apolo", "B. Cronos", "C. Afrodita", "D. Areas"),
        ("A. Caduceo", "B. Vellocino", "C. Pétaso", "D. Cornucopia"),
        ("A. Poseidón", "B. Ares", "C. Apolo", "D. Hera"),
        ("A. La Titanomaquia", "B. La Centauromaquia", "C. La Gigantomaquia", "D. La Guerra de Troya"),
        ("A. Cronos", "B. Urano", "C. Gea", "D. Caos"),
    ]

    RESPUESTAS = ["C", "C", "C", "A", "D", "B", "C", "B", "C", "A", "A", "A", "A", "B"]

    # Seleccionar cuatro preguntas al azar
    indices_preguntas = random.sample(range(len(PREGUNTAS)), 4)
    preguntas_seleccionadas = [PREGUNTAS[i] for i in indices_preguntas]
    opciones_seleccionadas = [OPCIONES[i] for i in indices_preguntas]
    respuestas_correctas = [RESPUESTAS[i] for i in indices_preguntas]

    # Variables de control
    indice_pregunta = 0
    indice_opcion = 0
    puntaje = 0
    intentos = 2
    mostrar_insuficiente = False  

    def mostrar_texto(texto, x, y, color=BLANCO):
        renderizado = fuente.render(texto, True, color)
        screen.blit(renderizado, (x, y))

    # Bucle principal
    while True:
        screen.fill(BLANCO)
        screen.blit(img_quiz, (0, 0))

        if mostrar_insuficiente:
            mostrar_texto("PUNTOS INSUFICIENTES", 80, 100)
            mostrar_texto(f"Intentos restantes: {intentos}", 90, 150)
            pygame.display.flip()
            pygame.time.delay(2000)  
            mostrar_insuficiente = False
            continue

        if indice_pregunta < len(preguntas_seleccionadas):
            mostrar_texto(f"Puntaje: {puntaje}", 80, 100)
            mostrar_texto(f"{preguntas_seleccionadas[indice_pregunta]}", 80, 200)
            for i, opcion in enumerate(opciones_seleccionadas[indice_pregunta]):
                color = VERDE if i == indice_opcion else BLANCO
                mostrar_texto(opcion, 90, 290 + i * 40, color)
        else:
            if puntaje >= 2:
                mostrar_texto("GANASTE", 80, 100)
            else:
                intentos -= 1
                if intentos > 0:
                    mostrar_insuficiente = True 
                    indice_pregunta = 0
                    puntaje = 0
                else:
                    mostrar_texto("GAME OVER", 80, 100)
                    mostrar_texto("Presiona Enter para salir", 80, 150)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if indice_pregunta >= len(preguntas_seleccionadas) and intentos <= 0 and event.key == pygame.K_RETURN:
                    return('LOSE')
                elif indice_pregunta >= len(preguntas_seleccionadas) and puntaje >= 2 and event.key == pygame.K_RETURN:
                    return('WIN')
                elif event.key == pygame.K_DOWN:
                    indice_opcion = (indice_opcion + 1) % 4
                elif event.key == pygame.K_UP:
                    indice_opcion = (indice_opcion - 1) % 4
                elif event.key == pygame.K_RETURN and indice_pregunta < len(preguntas_seleccionadas):
                    respuesta_seleccionada = opciones_seleccionadas[indice_pregunta][indice_opcion][0]
                    if respuesta_seleccionada == respuestas_correctas[indice_pregunta]:
                        puntaje += 1
                    indice_pregunta += 1
                    indice_opcion = 0


if __name__ == "__main__":
    main()