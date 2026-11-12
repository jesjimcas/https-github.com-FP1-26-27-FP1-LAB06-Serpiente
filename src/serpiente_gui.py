import tkinter as tk
from collections import deque
import serpiente_utiles as serpiente_utiles
import math
import random

FILAS = 30
COLUMNAS = 40
PASOS_ANIMACION = 6
PAREDES = [
    [(15,15), (16,15), (17,15), (18,15)],
    [(25,10), (25,11), (25,12), (25,13), (25,14), (25,15)],
    [(10,25), (11,25), (12,25), (13,25), (14,25)],
    [(30,20), (31,20), (32,20), (33,20), (34,20), (35,20)],
    [(20,5), (20,6), (20,7), (20,8)],
    [(8,5), (8,6), (8,7), (8,8)]
]

class SerpienteGUI(tk.Canvas):
    def __init__(self, filas=FILAS, columnas=COLUMNAS, tam_bloque=20):
        self.filas = filas
        self.columnas = columnas
        self.tam_bloque = tam_bloque
        self.ancho = columnas * tam_bloque
        self.alto = filas * tam_bloque  
        self.retraso_ms = 120  # Retraso inicial en milisegundos      
        self.retrasos_dificultad = {"facil": 170, "normal": 120, "dificil": 75}
        self.dificultad = "normal"
        self.juego_iniciado = False
        self.partida_finalizada = False

        super().__init__(width=self.ancho, height=self.alto, background="#08111f", highlightthickness=0)
        self.master.resizable(False, False)
        self.master.configure(background="#08111f")

        self.serpiente = [(5, 2), (4, 2), (3, 2)]              
        self.paredes = PAREDES

        self.comida = serpiente_utiles.genera_comida_aleatoria(self.serpiente, self.paredes, self.filas, self.columnas)
        self.puntuacion = 0
        self.direccion = "Right"
        self.ultima_direccion = self.direccion  
        self.cola_direcciones = deque()  # Lo usaremos para guardar pulsaciones más rápidas que el retardo

        self.bind_all("<Key>", self.al_pulsar_tecla)
        self.bind_all("<Button-1>", self.al_pulsar_raton)
        self.fase_animacion = 0
        self.dibuja_fondo()
        self.muestra_pantalla_inicial()

    def dibuja_fondo(self):
        self.create_rectangle(0, 0, self.ancho, self.alto, fill="#08111f", outline="", tag="background")
        # El margen evita que la cuadrícula parezca un límite físico del mundo.
        for x in range(self.tam_bloque, self.ancho, self.tam_bloque):
            self.create_line(x, 0, x, self.alto, fill="#102238", tag="background")
        for y in range(self.tam_bloque, self.alto, self.tam_bloque):
            self.create_line(0, y, self.ancho, y, fill="#102238", tag="background")

    def muestra_pantalla_inicial(self):
        self.create_text(
            self.ancho / 2,
            self.alto / 2 - 40,
            text="JUEGO DE LA SERPIENTE",
            fill="#e8f1ff",
            font=('TkDefaultFont', 26, 'bold'),
            tag="inicio"
        )
        self.create_text(
            self.ancho / 2,
            self.alto / 2 + 20,
            text="Controles: ← ↑ → ↓",
            fill="#65d6c2",
            font=('TkDefaultFont', 16),
            tag="inicio"
        )
        self.create_text(
            self.ancho / 2,
            self.alto / 2 + 60,
            text="Pulsa cualquier tecla para comenzar",
            fill="#8da5bd",
            font=('TkDefaultFont', 12),
            tag="inicio"
        )
        self.create_text(self.ancho / 2, self.alto / 2 + 115,
                         text="DIFICULTAD", fill="#8da5bd",
                         font=('TkDefaultFont', 10, 'bold'), tag="inicio")

        opciones = [("facil", "Fácil"), ("normal", "Normal"), ("dificil", "Difícil")]
        ancho_opcion = 110
        separacion = 14
        inicio_x = self.ancho / 2 - (3 * ancho_opcion + 2 * separacion) / 2
        for indice, (nivel, texto) in enumerate(opciones):
            x1 = inicio_x + indice * (ancho_opcion + separacion)
            x2 = x1 + ancho_opcion
            seleccionado = nivel == self.dificultad
            self.create_rectangle(
                x1, self.alto / 2 + 135, x2, self.alto / 2 + 175,
                fill="#194c55" if seleccionado else "#102238",
                outline="#65d6c2" if seleccionado else "#29435a",
                width=2 if seleccionado else 1,
                    tags=("inicio", "difficulty_button", f"difficulty_{nivel}",
                        f"difficulty_style_{nivel}")
            )
            self.create_text(
                (x1 + x2) / 2, self.alto / 2 + 155, text=texto,
                fill="#e8f1ff", font=('TkDefaultFont', 10, 'bold'),
                tags=("inicio", "difficulty_label", f"difficulty_{nivel}")
            )
            self.tag_bind(f"difficulty_{nivel}", "<Button-1>",
                          lambda event, opcion=nivel: self.selecciona_dificultad(opcion))

    def selecciona_dificultad(self, dificultad):
        if self.juego_iniciado or self.partida_finalizada:
            return
        self.dificultad = dificultad
        self.retraso_ms = self.retrasos_dificultad[dificultad]
        for nivel in self.retrasos_dificultad:
            seleccionado = nivel == dificultad
            self.itemconfigure(f"difficulty_style_{nivel}",
                               fill="#194c55" if seleccionado else "#102238",
                               outline="#65d6c2" if seleccionado else "#29435a",
                               width=2 if seleccionado else 1)

    def iniciar_juego(self):
        self.delete("inicio")
        self.delete("gameover")
        self.crea_objetos()
        self.juego_iniciado = True
        self.anima_comida()
        self.after(self.retraso_ms, self.bucle_juego)

    def convierte_a_pixeles(self, posicion):
        return posicion[0] * self.tam_bloque + self.tam_bloque/2, posicion[1] * self.tam_bloque + self.tam_bloque/2

    def crea_objetos(self):
        self.create_text(
            24, 24, text=f"PUNTOS  {self.puntuacion:02d}", anchor="w",
            tag="score", fill="#e8f1ff", font=('TkDefaultFont', 12, 'bold')
        )
        self.create_text(self.ancho - 24, 24, text="Usa las flechas del cursor",
                         anchor="e", tag="status", fill="#6d899f",
                         font=('TkDefaultFont', 9, 'bold'))
        for i, posicion in enumerate(self.serpiente):
            self.dibuja_segmento(posicion, i)
        self.dibuja_comida()
        self.crea_objetos_paredes()

    def dibuja_segmento(self, posicion, indice):
        x, y = self.convierte_a_pixeles(posicion)
        margen = 2 if indice else 1
        radio = self.tam_bloque / 2 - margen
        color = "#28b99f" if indice else "#65e0c2"
        borde = "#167d79" if indice else "#b0ffdf"
        self.create_oval(x - radio, y - radio, x + radio, y + radio,
                         fill=color, outline=borde, width=1, tag="snake")
        if indice == 0:
            self.create_oval(x - 6, y - 6, x - 1, y - 1, fill="#07131f", outline="", tag="snake_eye")
            self.create_oval(x + 1, y - 6, x + 6, y - 1, fill="#07131f", outline="", tag="snake_eye")

    def dibuja_comida(self):
        x, y = self.convierte_a_pixeles(self.comida)
        self.create_oval(x - 9, y - 9, x + 9, y + 9, fill="#3b2738",
                         outline="#ef668a", width=1, tag="food_glow")
        self.create_oval(x - 6, y - 6, x + 6, y + 6, fill="#ff6689",
                         outline="#ffd0a8", width=2, tag="food")
        self.create_oval(x - 2, y - 4, x + 1, y - 1, fill="#fff0d0", outline="", tag="food")
    
    def crea_objetos_paredes(self):
        for pared in self.paredes:
            for posicion in pared:
                x, y = self.convierte_a_pixeles(posicion)
                half = self.tam_bloque / 2 - 2
                self.create_rectangle(x - half + 2, y - half + 3, x + half + 2, y + half + 3,
                                      fill="#050b14", outline="", tag="wall_shadow")
                self.create_rectangle(x - half, y - half, x + half, y + half,
                                      fill="#314b67", outline="#7190a9", width=1, tag="wall")
                self.create_line(x - half + 2, y - half + 2, x + half - 2, y - half + 2,
                                 fill="#a2bed1", tag="wall_highlight")

    def anima_comida(self):
        if not self.juego_iniciado:
            return
        self.fase_animacion += 0.18
        escala = 1 + math.sin(self.fase_animacion) * 0.12
        x, y = self.convierte_a_pixeles(self.comida)
        radio = 9 * escala
        self.coords(self.find_withtag("food_glow"), x - radio, y - radio, x + radio, y + radio)
        self.after(35, self.anima_comida)

    def crea_particulas(self, posicion):
        x, y = self.convierte_a_pixeles(posicion)
        for _ in range(12):
            angulo = random.random() * math.tau
            distancia = random.randint(5, 12)
            px, py = x + math.cos(angulo) * distancia, y + math.sin(angulo) * distancia
            particula = self.create_oval(px - 2, py - 2, px + 2, py + 2,
                                         fill="#ffd166", outline="", tag="particle")
            self.anima_particula(particula, px, py, math.cos(angulo) * 1.5, math.sin(angulo) * 1.5, 7)

    def anima_particula(self, item, x, y, dx, dy, vida):
        if vida <= 0:
            self.delete(item)
            return
        self.move(item, dx, dy)
        self.itemconfigure(item, state="normal" if vida % 2 else "hidden")
        self.after(35, self.anima_particula, item, x + dx, y + dy, dx, dy, vida - 1)

    def coloca_segmentos(self, posiciones, progreso):
        for indice, (segmento, posicion) in enumerate(zip(self.find_withtag("snake"), self.serpiente)):
            origen = posiciones[indice] if indice < len(posiciones) else posicion
            x_origen, y_origen = self.convierte_a_pixeles(origen)
            x_destino, y_destino = self.convierte_a_pixeles(posicion)

            if abs(x_destino - x_origen) > self.ancho / 2:
                x = x_destino
            else:
                x = x_origen + (x_destino - x_origen) * progreso
            if abs(y_destino - y_origen) > self.alto / 2:
                y = y_destino
            else:
                y = y_origen + (y_destino - y_origen) * progreso

            radio = self.tam_bloque / 2 - (1 if indice == 0 else 2)
            self.coords(segmento, x - radio, y - radio, x + radio, y + radio)

        cabeza_x, cabeza_y = self.convierte_a_pixeles(self.serpiente[0])
        if posiciones:
            origen_x, origen_y = self.convierte_a_pixeles(posiciones[0])
            if abs(cabeza_x - origen_x) <= self.ancho / 2:
                cabeza_x = origen_x + (cabeza_x - origen_x) * progreso
            if abs(cabeza_y - origen_y) <= self.alto / 2:
                cabeza_y = origen_y + (cabeza_y - origen_y) * progreso
        ojos = self.find_withtag("snake_eye")
        if len(ojos) == 2:
            self.coords(ojos[0], cabeza_x - 6, cabeza_y - 6, cabeza_x - 1, cabeza_y - 1)
            self.coords(ojos[1], cabeza_x + 1, cabeza_y - 6, cabeza_x + 6, cabeza_y - 1)

    def anima_movimiento(self, posiciones, paso=1):
        if not self.juego_iniciado:
            return
        progreso = min(paso / PASOS_ANIMACION, 1)
        self.coloca_segmentos(posiciones, progreso)
        if paso < PASOS_ANIMACION:
            intervalo = max(1, self.retraso_ms // (PASOS_ANIMACION - 1))
            self.after(intervalo, self.anima_movimiento, posiciones, paso + 1)
        else:
            self.after(1, self.bucle_juego)
        
    def mueve_serpiente(self):
        posiciones_anteriores = self.serpiente.copy()
        while self.cola_direcciones:
            siguiente_direccion = self.cola_direcciones.popleft()
            if (self.ultima_direccion == "Left" and siguiente_direccion != "Right") or \
               (self.ultima_direccion == "Right" and siguiente_direccion != "Left") or \
               (self.ultima_direccion == "Up" and siguiente_direccion != "Down") or \
               (self.ultima_direccion == "Down" and siguiente_direccion != "Up"):
                self.direccion = siguiente_direccion
                break

        serpiente_utiles.mueve_serpiente(self.serpiente, self.direccion, self.filas, self.columnas)
        self.anima_movimiento(posiciones_anteriores)
            
        self.ultima_direccion = self.direccion

    def bucle_juego(self):
        self.mueve_serpiente()

        if serpiente_utiles.comprueba_choque(self.serpiente, self.paredes):
            self.game_over()
            return

        self.comprueba_serpiente_come_crece()

    def anima_explosion(self, segmentos, indice=0):
        if indice >= len(segmentos):
            self.muestra_game_over()
            return

        segmento = segmentos[indice]
        posicion = self.serpiente[indice] if indice < len(self.serpiente) else self.serpiente[-1]
        x, y = self.convierte_a_pixeles(posicion)
        radio = self.tam_bloque / 2
        destello = self.create_oval(x - radio, y - radio, x + radio, y + radio,
                                    fill="#ffe08a", outline="#ff6689", width=2,
                                    tag="explosion")
        self.crea_particulas((posicion[0], posicion[1]))
        self.delete(segmento)
        self.after(70, self.delete, destello)
        self.after(95, self.anima_explosion, segmentos, indice + 1)

    def muestra_game_over(self):
        self.delete("snake", "snake_eye", "food", "food_glow", "particle", "explosion", "score", "status")
        self.create_rectangle(150, 210, self.ancho - 150, 390, fill="#0e2034",
                              outline="#e35d7d", width=2, tag="gameover")
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2 - 24,
            text="FIN DE LA PARTIDA", fill="#ff8299", font=('TkDefaultFont', 24, 'bold'), tag="gameover"
        )
        self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2 + 25,
            text=f"Puntuación  {self.puntuacion:02d}", fill="#e8f1ff",
            font=('TkDefaultFont', 15), tag="gameover"
        )
        self.create_text(
            self.winfo_width() / 2, self.winfo_height() / 2 + 60,
            text="Pulsa el ratón para salir", fill="#8da5bd",
            font=('TkDefaultFont', 11), tag="gameover"
        )

    def game_over(self):
        self.juego_iniciado = False
        self.partida_finalizada = True
        segmentos = self.find_withtag("snake")
        self.delete("snake_eye", "food", "food_glow", "score", "status")
        self.anima_explosion(segmentos)

    def al_pulsar_tecla(self, e):
        if self.partida_finalizada:
            return

        if not self.juego_iniciado:
            self.iniciar_juego()
            return
            
        if e.keysym in {"Left", "Right", "Up", "Down"}:
            self.cola_direcciones.append(e.keysym)

    def al_pulsar_raton(self, e):
        if self.partida_finalizada:
            self.master.destroy()


    def comprueba_serpiente_come_crece(self):
        if serpiente_utiles.ha_comido_serpiente(self.serpiente, self.comida):
            self.puntuacion += 1
            self.crea_particulas(self.comida)
            serpiente_utiles.crece_serpiente(self.serpiente)
            if self.retraso_ms > 50:
                self.retraso_ms -= 1 # Cuanto más come, más rápido se moverá

            self.dibuja_segmento(self.serpiente[-1], len(self.serpiente) - 1)
            
            self.comida = serpiente_utiles.genera_comida_aleatoria(self.serpiente, self.paredes, self.filas, self.columnas)
            self.delete("food", "food_glow")
            self.dibuja_comida()
            
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"PUNTOS  {self.puntuacion:02d}")

               

root = tk.Tk()
root.title("Juego Serpiente")

board = SerpienteGUI()
board.pack()

root.mainloop()
