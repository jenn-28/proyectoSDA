# pylint: disable=no-member
import pygame
import collections

# Configuración de colores
BLANCO = (255, 255, 255) #Mapa
NEGRO = (0, 0, 0) #Muros
GRIS = (200, 200, 200) #Lineas
VERDE = (0, 255, 0)  # Inicio
ROJO = (255, 0, 0)    # Fin
AZUL = (0, 0, 255)    # Explorando BFS
AMARILLO = (255, 255, 0) # Camino final
MORADO = (128, 0, 128) # Explorando DFS
NARANJA = (255, 165, 0) #explorando DLS

# Dimensiones del mapa
ANCHO, ALTO = 600, 600
COLUMNAS, FILAS = 30, 30
TAMANO_CELDA = ANCHO // COLUMNAS

def bfs(inicio, fin, muros, ventana):
    conteo = 0
    cola = collections.deque([inicio])
    visitados = {inicio: None} # Diccionario para rastrear el camino (nodo: padre)

    while cola:
        actual = cola.popleft()

        if actual == fin:
            # Reconstruir camino
            while actual in visitados and actual is not None:
                dibujar_celda(ventana, actual, AMARILLO)
                dibujar_celda(ventana, inicio, VERDE)
                dibujar_celda(ventana, fin, ROJO)
                actual = visitados[actual]
                pygame.display.update()
            print("BFS Finalizado. ENCONTRASTRE EL REFUGIO -> Cantidad de nodos visitados: ", conteo)
            esperar_reinicio(muros)
            return True

        # Obtener vecinos (Derecha, Izquierda, Abajo, Arriba)
        r, c = actual
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            vecino = (r + dr, c + dc)
            if 0 <= vecino[0] < FILAS and 0 <= vecino[1] < COLUMNAS:
                if vecino not in muros and vecino not in visitados:
                    visitados[vecino] = actual
                    cola.append(vecino)
                    conteo = conteo + 1
                    # Dibujar exploración
                    if vecino != fin:
                        dibujar_celda(ventana, vecino, AZUL)
        
        pygame.display.update()
        pygame.time.delay(20) # Control de velocidad para ver el proceso
    print("BFS Finalizado. Fuiste devorado por los infectados")
    esperar_reinicio(muros)
    return False

def dfs(inicio, fin, muros, ventana):
    conteo = 0
    pila = collections.deque([inicio])
    visitados = {inicio: None} # Diccionario para rastrear el camino (nodo: padre)

    while pila:
        actual = pila.pop()

        if actual == fin:
            # Reconstruir camino
            while actual in visitados and actual is not None:
                dibujar_celda(ventana, actual, AMARILLO)
                dibujar_celda(ventana, inicio, VERDE)
                dibujar_celda(ventana, fin, ROJO)
                actual = visitados[actual]
                pygame.display.update()
            print("DFS Finalizado. ENCONTRASTRE EL REFUGIO -> Cantidad de nodos visitados: ", conteo)
            esperar_reinicio(muros)
            return True

        # Obtener vecinos ((Derecha, Izquierda, Abajo, Arriba)
        r, c = actual
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            vecino = (r + dr, c + dc)
            if 0 <= vecino[0] < FILAS and 0 <= vecino[1] < COLUMNAS:
                if vecino not in muros and vecino not in visitados:
                    visitados[vecino] = actual
                    pila.append(vecino)
                    conteo = conteo + 1
                    # Dibujar exploración
                    if vecino != fin:
                        dibujar_celda(ventana, vecino, MORADO)
        
        pygame.display.update()
        pygame.time.delay(20) # Control de velocidad para ver el proceso
    print("DFS Finalizado. Fuiste devorado por los infectados")
    esperar_reinicio(muros)
    return False

def dls(inicio, fin, muros, ventana, limite, iterativa=False):
    conteo = 0
    pila = collections.deque([(inicio, 0)])
    visitados = {inicio: None} # Diccionario para rastrear el camino (nodo: padre)

    while pila:
        actual, profundidad = pila.pop()

        if actual == fin:
            # Reconstruir camino
            while actual in visitados and actual is not None:
                dibujar_celda(ventana, actual, AMARILLO)
                dibujar_celda(ventana, inicio, VERDE)
                dibujar_celda(ventana, fin, ROJO)
                actual = visitados[actual]
                pygame.display.update()
            if not iterativa:
                print("DLS Finalizado. ENCONTRASTRE EL REFUGIO -> Cantidad de nodos visitados: ", conteo)
            elif iterativa:
                print("IDDFS Finalizado. ENCONTRASTRE EL REFUGIO -> Cantidad de nodos visitados: ", conteo)
            esperar_reinicio(muros)
            return True

        # Obtener vecinos ((Derecha, Izquierda, Abajo, Arriba) SOLO SI NO HA LLEGADO AL LIMITE
        if(profundidad < limite):
            r, c = actual
            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                vecino = (r + dr, c + dc)
                if 0 <= vecino[0] < FILAS and 0 <= vecino[1] < COLUMNAS:
                    if vecino not in muros and vecino not in visitados:
                        visitados[vecino] = actual
                        pila.append((vecino, profundidad + 1))
                        conteo = conteo + 1
                        # Dibujar exploración
                        if vecino != fin:
                            dibujar_celda(ventana, vecino, NARANJA)
        
        pygame.display.update()
        pygame.time.delay(20) # Control de velocidad para ver el proceso
    if not iterativa:
        print("DLS Finalizado. Fuiste devorado por los infectados")
        esperar_reinicio(muros)
    return False

def iddfs(inicio, fin, muros, ventana):
    limite = 0
    MAX = FILAS * COLUMNAS
    while limite <= MAX:
        band = dls(inicio, fin, muros, ventana, limite, iterativa=True)

        if band:
            return True
        
        ventana.fill(GRIS)
        for r in range(FILAS):
            for c in range(COLUMNAS):
                dibujar_celda(ventana, (r, c), BLANCO)

        for m in muros: dibujar_celda(ventana, m, NEGRO)
        dibujar_celda(ventana, inicio, VERDE)
        dibujar_celda(ventana, fin, ROJO)

        pygame.time.delay(300)
        
        limite += 1
    print("IDDFS Finalizado. Fuiste devorado por los infectados")
    esperar_reinicio(muros)
    return False
    
def dibujar_celda(win, pos, color):
    pygame.draw.rect(win, color, (pos[1]*TAMANO_CELDA, pos[0]*TAMANO_CELDA, TAMANO_CELDA-1, TAMANO_CELDA-1))

def esperar_reinicio(muros):
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False
                elif evento.key == pygame.K_l:
                    muros.clear()
                    esperando = False

def main():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Simulador de Supervivencia")
    
    inicio = None
    fin = None
    muros = set()
    corriendo = True

    etapa = 0
    algoritmo = ""

    while corriendo:
        ventana.fill(GRIS)
        for r in range(FILAS):
            for c in range(COLUMNAS):
                dibujar_celda(ventana, (r, c), BLANCO)

        for m in muros: dibujar_celda(ventana, m, NEGRO)
        if inicio: dibujar_celda(ventana, inicio, VERDE)
        if fin: dibujar_celda(ventana, fin, ROJO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            if etapa != 0:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    fila = pos[1]//TAMANO_CELDA
                    col = pos[0]//TAMANO_CELDA

                    posicion = (fila, col)

                    #Primer Click INICIO
                    if inicio is None:
                        inicio = posicion
               
                    #Segundo click FIN
                    elif fin is None and posicion != inicio:
                        fin = posicion

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    fila = pos[1]//TAMANO_CELDA
                    col = pos[0]//TAMANO_CELDA
                    posicion = (fila, col)
                    muros.add(posicion)

                    if inicio is not None and fin is not None:
                        if posicion != inicio and posicion != fin:
                         muros.add(posicion)


            if evento.type == pygame.KEYDOWN:
                if etapa == 0:
                    if evento.key == pygame.K_1:
                        etapa = 1
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1")
                    if evento.key == pygame.K_2:
                        etapa = 2
                        pygame.display.set_caption("Simulador de Grafos: Etapa 2")
                    if evento.key == pygame.K_3:
                        etapa = 3
                        pygame.display.set_caption("Simulador de Grafos: Etapa 3")
                elif evento.key == pygame.K_x:
                    etapa = 0
                    muros.clear() 
                    inicio=None
                    fin=None     
                    pygame.display.set_caption("Simulador de Grafos")

                elif etapa == 1 and algoritmo == "":
                    if evento.key == pygame.K_b: 
                        algoritmo = "BFS"
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1 - BFS")
                    elif evento.key == pygame.K_d: 
                        algoritmo = "DFS"
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1 - DFS")
                    elif evento.key == pygame.K_l: 
                        algoritmo = "LIMITADA"
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1 - LIMITADA")
                    elif evento.key == pygame.K_i: 
                        algoritmo = "ITERATIVA"
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1 - ITERATIVA")
                    elif evento.key == pygame.K_c: 
                        etapa = 0
                        muros.clear() 
                        inicio=None
                        fin=None                       
                        pygame.display.set_caption("Simulador de Grafos")

                elif etapa == 1 and algoritmo != "":
                    if evento.key == pygame.K_SPACE:
                        if algoritmo == "BFS":
                            bfs(inicio, fin, muros, ventana)
                        if algoritmo == "DFS":
                            dfs(inicio, fin, muros, ventana)
                        if algoritmo == "LIMITADA":
                            limite = int(input("Introduce el limite de saltos: "))
                            dls(inicio, fin, muros, ventana, limite, iterativa = False)
                        if algoritmo == "ITERATIVA":
                            iddfs(inicio, fin, muros, ventana)
                        algoritmo = ""
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1")

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
