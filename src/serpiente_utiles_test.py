from serpiente_utiles import *

def test_comprueba_choque():
    # Caso de prueba donde la serpiente se choca consigo misma
    serpiente_choque = [(0,0), (1,0), (0,0)]
    assert comprueba_choque(serpiente_choque, [[]]), "Error: la serpiente debería haberse chocado consigo misma"

    # Caso de prueba donde la serpiente no se choca consigo misma
    serpiente_no_choque = [(0,0), (1,0), (2,0)]
    assert not comprueba_choque(serpiente_no_choque, [[]]), "Error: la serpiente no debería haberse chocado consigo misma"

    # Caso de prueba donde la serpiente se choca con una pared
    serpiente_choque_pared = [(0,0), (1,0), (2,0)]
    paredes = [[(0,0), (0,1)]]
    assert comprueba_choque(serpiente_choque_pared, paredes), "Error: la serpiente debería haberse chocado con la pared"

    # Caso de prueba donde la serpiente no se choca con una pared
    serpiente_no_choque_pared = [(0,0), (1,0), (2,0)]
    paredes = [[(3,0), (3,1)]]
    assert not comprueba_choque(serpiente_no_choque_pared, paredes), "Error: la serpiente no debería haberse chocado con la pared"

def test_ha_comido_serpiente():
    # Caso de prueba donde la cabeza de la serpiente está en la misma posición que la comida
    serpiente_con_comida = [(0,0), (1,0)]
    posicion_comida = (0,0)
    assert ha_comido_serpiente(serpiente_con_comida, posicion_comida), "Error: la cabeza de la serpiente debería estar en la misma posición que la comida"

    # Caso de prueba donde la cabeza de la serpiente no está en la misma posición que la comida
    serpiente_sin_comida = [(0,0), (1,0)]
    posicion_comida_diferente = (2,2)
    assert not ha_comido_serpiente(serpiente_sin_comida, posicion_comida_diferente), "Error: la cabeza de la serpiente no debería estar en la misma posición que la comida"

def test_crece_serpiente():
    serpiente = [(2,2), (2,1), (2,0)]
    serpiente_original = serpiente.copy()
    crece_serpiente(serpiente)

    # Verificar que la longitud de la serpiente ha aumentado en uno
    assert len(serpiente) == len(serpiente_original) + 1, "Error: la serpiente no creció en longitud como se esperaba."

    # Verificar que todas las posiciones, excepto la última, son iguales a las originales
    assert serpiente[:-1] == serpiente_original, "Error: las posiciones existentes de la serpiente han cambiado."

    # Verificar que la nueva posición es igual a la última posición original
    assert serpiente[-1] == serpiente_original[-1], "Error: la nueva posición de la serpiente no es una duplicación de la última posición."

def test_genera_comida_aleatoria():
    serpiente = [(0,0)]
    paredes = [[(1,0), (2,0)]]
    filas = 30
    columnas = 40

    posiciones_comida = set()
    for _ in range(100):  
        comida = genera_comida_aleatoria(serpiente, paredes, filas, columnas)
        posiciones_comida.add(comida)

        # La comida no debe estar en la misma posición que la serpiente o las paredes
        assert comida not in serpiente and all(comida not in pared for pared in paredes), "Error: la comida fue generada en una posición inválida."
        # La comida debe estar dentro de los límites del tablero
        assert 0 <= comida[0] < columnas and 0 <= comida[1] < filas, "Error: la comida fue generada fuera de los límites del tablero."
    # Verificar que se generaron posiciones variadas
    assert len(posiciones_comida) > 10, "Error: la función no generó suficiente variación en las posiciones de la comida."


def test_mueve_serpiente():
    filas = 5
    columnas = 4

    # Mover la serpiente hacia arriba y verificar su nueva posición
    serpiente = [(2,2), (2,1), (2,0)]
    mueve_serpiente(serpiente, "Up", filas, columnas)
    assert serpiente == [(2, 1), (2, 2), (2, 1)], "Error: movimiento hacia arriba incorrecto."

    # Mover la serpiente hacia la izquierda y verificar su nueva posición
    mueve_serpiente(serpiente, "Left", filas, columnas)
    assert serpiente == [(1, 1), (2, 1), (2, 2)], "Error: movimiento hacia la izquierda incorrecto."

    # Mover la serpiente hacia abajo y verificar su nueva posición
    mueve_serpiente(serpiente, "Down", filas, columnas)
    assert serpiente == [(1,2), (1, 1), (2, 1)], "Error: movimiento hacia abajo incorrecto en el borde del tablero."

    # Mover la serpiente hacia la derecha y verificar su nueva posición
    mueve_serpiente(serpiente, "Right", filas, columnas)
    assert serpiente == [(2,2), (1,2), (1, 1)], "Error: movimiento hacia la derecha incorrecto."

    # Mover la serpiente hacia la derecha en el borde y verificar si aparece por la izquierda
    serpiente = [(3,4)]
    mueve_serpiente(serpiente, "Right", filas, columnas)
    assert serpiente == [(0,4)], "Error: movimiento circular hacia la derecha en el borde del tablero no funcionó correctamente."

    # Mover la serpiente hacia arriba en el borde y verificar si aparece por abajo
    serpiente = [(0,0)]
    mueve_serpiente(serpiente, "Up", filas, columnas)
    assert serpiente == [(0,4)], "Error: movimiento circular hacia arriba en el borde del tablero no funcionó correctamente."

    # Mover la serpiente hacia la izquierda en el borde y verificar si aparece por la derecha
    serpiente = [(0,0)]
    mueve_serpiente(serpiente, "Left", filas, columnas)
    assert serpiente == [(3,0)], "Error: movimiento circular hacia la izquierda en el borde del tablero no funcionó correctamente."

    # Mover la serpiente hacia abajo en el borde y verificar si aparece por arriba
    serpiente = [(0,4)]
    mueve_serpiente(serpiente, "Down", filas, columnas)
    assert serpiente == [(0,0)], "Error: movimiento circular hacia abajo en el borde del tablero no funcionó correctamente."


# Descomenta las siguientes líneas para ejecutar los tests
test_comprueba_choque()
#test_ha_comido_serpiente()
#test_crece_serpiente()
#test_genera_comida_aleatoria()
#test_mueve_serpiente() 
print("Todos los tests superados.")