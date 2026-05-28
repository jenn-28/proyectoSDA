# pylint: disable=no-member
import pygame
import collections
import heapq

terrenos = {}

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
CAFE = (139, 69, 19) # Lodo (costo 5)
CELESTE = (0, 255, 255)  # Exploración A*

# Dimensiones del mapa
ANCHO, ALTO = 600, 600
COLUMNAS, FILAS = 30, 30
TAMANO_CELDA = ANCHO // COLUMNAS

#PRIMERA ETAPA: BFS, DFS, DLS, IDDFS

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
            return esperar_reinicio(muros, terrenos)

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
    return esperar_reinicio(muros, terrenos)

def bfs_etapa2(inicio, fin, muros, terrenos, ventana):
    cola = collections.deque([inicio])
    visitados = {inicio: None}

    while cola:
        actual = cola.popleft()

        if actual == fin:
            costo_total = 0
            nodos_camino = 0
            
            while actual is not None:
                dibujar_celda(ventana, actual, AMARILLO)
                dibujar_celda(ventana, inicio, VERDE)
                dibujar_celda(ventana, fin, ROJO)
                
                nodos_camino += 1
                if actual != inicio:
                    costo_total = costo_total + terrenos.get(actual, 1)
                    
                actual = visitados[actual]
                pygame.display.update()
                
            print("BFS (Etapa 2) Finalizado")
            print("Nodos en el camino a la meta:", nodos_camino)
            print("Costo total del camino:", costo_total)
            return esperar_reinicio(muros, terrenos)

        r, c = actual
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            vecino = (r + dr, c + dc)
            if 0 <= vecino[0] < FILAS and 0 <= vecino[1] < COLUMNAS:
                if vecino not in muros and vecino not in visitados:
                    visitados[vecino] = actual
                    cola.append(vecino)
                    if vecino != fin:
                        dibujar_celda(ventana, vecino, AZUL)
        
        pygame.display.update()
        pygame.time.delay(20)
    print("BFS (Etapa 2) Finalizado. No se encontró camino.")
    return esperar_reinicio(muros, terrenos)

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
            return esperar_reinicio(muros, terrenos)

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
    return esperar_reinicio(muros, terrenos)

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
                return esperar_reinicio(muros, terrenos)
            elif iterativa:
                print("IDDFS Finalizado. ENCONTRASTRE EL REFUGIO -> Cantidad de nodos visitados: ", conteo)
                return True # Devuelve True para romper el ciclo en IDDFS

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
        return esperar_reinicio(muros, terrenos)
    return False

def iddfs(inicio, fin, muros, ventana):
    limite = 0
    MAX = FILAS * COLUMNAS
    while limite <= MAX:
        band = dls(inicio, fin, muros, ventana, limite, iterativa=True)

        if band is True: # Encontró el camino
            return esperar_reinicio(muros, terrenos)
        
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
    return esperar_reinicio(muros, terrenos)

#SEGUNDA ETAPA: A*
def algoritmo_a(inicio, fin, muros, terrenos, ventana):
    cola = []
    heapq.heappush(cola, (0, inicio))

    padres = {inicio: None}
    # g(n)
    costos = {inicio: 0}

    while cola:
        prioridad_actual, actual = heapq.heappop(cola)

        # Llegó al final
        if actual == fin:
            nodos_camino = 0
            
            while actual is not None:
                dibujar_celda(ventana, actual, AMARILLO)
                dibujar_celda(ventana, inicio, VERDE)
                dibujar_celda(ventana, fin, ROJO)
                
                nodos_camino += 1
                actual = padres[actual]
                pygame.display.update()

            print("A* Finalizado")
            print("Nodos en el camino a la meta:", nodos_camino)
            print("Costo total:", costos[fin])
            return esperar_reinicio(muros, terrenos)

        r, c = actual

        # vecinos
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            vecino = (r + dr, c + dc)
            if 0 <= vecino[0] < FILAS and 0 <= vecino[1] < COLUMNAS:

                # ignorar muros
                if vecino in muros:
                    continue

                # costo del terreno
                costo_terreno = terrenos.get(vecino, 1)

                # g(n)
                nuevo_costo = costos[actual] + costo_terreno

                # si encontramos camino más barato
                if vecino not in costos or nuevo_costo < costos[vecino]:

                    costos[vecino] = nuevo_costo

                    # h(n)
                    heuristica = abs(fin[0] - vecino[0]) + abs(fin[1] - vecino[1])

                    # f(n)
                    prioridad = nuevo_costo + heuristica

                    heapq.heappush(cola, (prioridad, vecino))
                    padres[vecino] = actual

                    if vecino != fin:
                        dibujar_celda(ventana, vecino, CELESTE)
        
        pygame.display.update()
        pygame.time.delay(25)

    print("A* Finalizado. No hay camino.")
    return esperar_reinicio(muros, terrenos)


def dibujar_celda(win, pos, color):
    pygame.draw.rect(win, color, (pos[1]*TAMANO_CELDA, pos[0]*TAMANO_CELDA, TAMANO_CELDA-1, TAMANO_CELDA-1))

def esperar_reinicio(muros, terrenos):
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return "REINICIAR"
                elif evento.key == pygame.K_l:
                    muros.clear()
                    terrenos.clear()
                    return "LIMPIAR"

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
        for t in terrenos: dibujar_celda(ventana, t, CAFE)
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
                        if etapa == 1:
                            pygame.display.set_caption("Etapa 1: Dibuja Muros (Clic Izq.) - Elige: B, D, L o I")
                        elif etapa == 2:
                            pygame.display.set_caption("Etapa 2: Clic Izq = Muros | Clic Der = Lodo. Elige: A o B")

            if evento.type == pygame.KEYDOWN:
                if etapa == 0:
                    if evento.key == pygame.K_1:
                        etapa = 1
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1 - Coloca INICIO y FIN")
                    if evento.key == pygame.K_2:
                        etapa = 2
                        pygame.display.set_caption("Simulador de Grafos: Etapa 2 - Coloca INICIO y FIN")
                    if evento.key == pygame.K_3:
                        etapa = 3
                        pygame.display.set_caption("Simulador de Grafos: Etapa 3")
                elif evento.key == pygame.K_x:
                    etapa = 0
                    muros.clear() 
                    terrenos.clear()
                    inicio = None
                    fin = None     
                    pygame.display.set_caption("Simulador de Grafos")

#ETAPA 1: BFS, DFS, DLS, IDDFS
                elif etapa == 1 and algoritmo == "":
                    if evento.key == pygame.K_b: 
                        algoritmo = "BFS"
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1 - BFS [Presiona ESPACIO]")
                    elif evento.key == pygame.K_d: 
                        algoritmo = "DFS"
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1 - DFS [Presiona ESPACIO]")
                    elif evento.key == pygame.K_l: 
                        algoritmo = "LIMITADA"
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1 - LIMITADA [Presiona ESPACIO]")
                    elif evento.key == pygame.K_i: 
                        algoritmo = "ITERATIVA"
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1 - ITERATIVA [Presiona ESPACIO]")

                elif etapa == 1 and algoritmo != "":
                    if evento.key == pygame.K_SPACE:
                        if inicio is not None and fin is not None:
                            accion = ""
                            if algoritmo == "BFS":
                                accion = bfs(inicio, fin, muros, ventana)
                            elif algoritmo == "DFS":
                                accion = dfs(inicio, fin, muros, ventana)
                            elif algoritmo == "LIMITADA":
                                limite = int(input("Introduce el limite de saltos: "))
                                accion = dls(inicio, fin, muros, ventana, limite, iterativa = False)
                            elif algoritmo == "ITERATIVA":
                                accion = iddfs(inicio, fin, muros, ventana)
                            
                            if accion == "LIMPIAR":
                                inicio = None
                                fin = None
                                algoritmo = ""
                                pygame.display.set_caption("Simulador de Grafos: Etapa 1 - Coloca INICIO y FIN")
                            elif accion == "REINICIAR":
                                algoritmo = ""
                                pygame.display.set_caption("Simulador de Grafos: Etapa 1 - Elige: B, D, L o I")
                        else:
                            print("Debes colocar el INICIO y el FIN en el mapa antes de iniciar.")

 #ETAPA 2: A*, BFS              
                elif etapa == 2 and algoritmo == "":
                    if evento.key == pygame.K_a:
                        algoritmo = "A*"
                        pygame.display.set_caption("Simulador de Grafos: Etapa 2 - A* [Presiona ESPACIO]")
                    elif evento.key == pygame.K_b:
                        algoritmo = "BFS"
                        pygame.display.set_caption("Simulador de Grafos: Etapa 2 - BFS [Presiona ESPACIO]") 

                elif etapa == 2 and algoritmo != "":
                    if evento.key == pygame.K_SPACE:
                        if inicio is not None and fin is not None:
                            accion = ""
                            if algoritmo == "BFS":
                                accion = bfs_etapa2(inicio, fin, muros, terrenos, ventana)
                            elif algoritmo == "A*":
                                accion = algoritmo_a(inicio, fin, muros, terrenos, ventana)
                            
                            if accion == "LIMPIAR":
                                inicio = None
                                fin = None
                                algoritmo = ""
                                pygame.display.set_caption("Simulador de Grafos: Etapa 2 - Coloca INICIO y FIN")
                            elif accion == "REINICIAR":
                                algoritmo = ""
                                pygame.display.set_caption("Simulador de Grafos: Etapa 2 - Elige: A o B")
                        else:
                            print("Debes colocar el INICIO y el FIN en el mapa antes de iniciar.")

#ETAPA 3
                elif etapa == 3 and algoritmo == "":
                    print("En construccion...")
                    etapa = 0

            if etapa != 0 and inicio is not None and fin is not None:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    fila = pos[1]//TAMANO_CELDA
                    col = pos[0]//TAMANO_CELDA
                    posicion = (fila, col)

                    if posicion != inicio and posicion != fin:
                        muros.add(posicion)

                if etapa == 2 and pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    fila = pos[1]//TAMANO_CELDA
                    col = pos[0]//TAMANO_CELDA
                    posicion = (fila, col)

                    if posicion != inicio and posicion != fin  and posicion not in muros:
                        terrenos[posicion] = 5

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()