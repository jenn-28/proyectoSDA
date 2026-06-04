# pylint: disable=no-member
import pygame
import collections
import heapq

terrenos = {}
mensaje_estado = ""

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
ANCHO_MAPA = 600
ANCHO_PANEL = 300
ANCHO = ANCHO_MAPA + ANCHO_PANEL
ALTO = 655
COLUMNAS, FILAS = 30, 40
TAMANO_CELDA = ANCHO_MAPA // COLUMNAS


#PRIMERA ETAPA: BFS, DFS, DLS, IDDFS

def bfs(inicio, fin, muros, ventana):
    global mensaje_estado
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
            mensaje_estado = (f"BFS: Refugio encontrado. "
                            f"Nodos visitados: {conteo}")
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
    mensaje_estado = ("BFS Finalizado: Fuiste devorado por los infectados")
    return esperar_reinicio(muros, terrenos)

def dfs(inicio, fin, muros, ventana):
    global mensaje_estado
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
            mensaje_estado = (f"DFS: Refugio encontrado. "
                f"Nodos visitados: {conteo}")
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
    mensaje_estado = "DFS: No se encontro camino"
    return esperar_reinicio(muros, terrenos)

def dls(inicio, fin, muros, ventana, limite, iterativa=False):
    global mensaje_estado
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
                mensaje_estado = (f"DLS: Refugio encontrado. "
                    f"Nodos visitados: {conteo}")
                return esperar_reinicio(muros, terrenos)
            elif iterativa:
                mensaje_estado = (f"IDDFS: Refugio encontrado. " f"Nodos visitados: {conteo}")
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
        mensaje_estado = ("DLS Finalizado: Fuiste devorado por los inefctados")
        return esperar_reinicio(muros, terrenos)
    return False

def iddfs(inicio, fin, muros, ventana):
    global mensaje_estado
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
    mensaje_estado =("IDDFS Finalizado: Fuiste devorado por los infectados")    
    return esperar_reinicio(muros, terrenos)

#SEGUNDA ETAPA: A*
def algoritmo_a(inicio, fin, muros, terrenos, ventana):
    global mensaje_estado
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

            mensaje_estado = (f"A*: Camino={nodos_camino} "
            f"Costo={costos[fin]}")
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

def bfs_etapa2(inicio, fin, muros, terrenos, ventana):
    global mensaje_estado
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
                
            mensaje_estado = (f"BFS: Camino={nodos_camino} "
            f"Costo={costo_total}")
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

#TERCERA ETAPA KRUSKAL Y PRIM
def kruskal(puntos, ventana, muros, terrenos):
    global mensaje_estado

    aristas = []

    # Generar todas las conexiones posibles
    for i in range(len(puntos)):
        for j in range(i + 1, len(puntos)):
            costo = distancia(puntos[i], puntos[j])
            aristas.append((costo, i, j))

    # Ordenar por costo
    aristas.sort()

    ds = DisjointSet(len(puntos))

    costo_total = 0
    aristas_usadas = 0

    for costo, origen, destino in aristas:

        if ds.union(origen, destino):

            dibujar_arista(
                ventana,
                puntos[origen],
                puntos[destino]
            )

            pygame.display.update()
            pygame.time.delay(500)

            costo_total += costo
            aristas_usadas += 1

            if aristas_usadas == len(puntos) - 1:
                break

    mensaje_estado = f"Kruskal costo total: {costo_total}"

    return esperar_reinicio(muros, terrenos)

def prim(puntos, nodo_raiz, ventana, muros, terrenos):
    global mensaje_estado

    visitados = set()
    visitados.add(nodo_raiz)

    costo_total = 0

    while len(visitados) < len(puntos):

        mejor_costo = float("inf")
        mejor_origen = None
        mejor_destino = None

        for origen in visitados:

            for destino in range(len(puntos)):

                if destino not in visitados:

                    costo = distancia(
                        puntos[origen],
                        puntos[destino]
                    )

                    if costo < mejor_costo:
                        mejor_costo = costo
                        mejor_origen = origen
                        mejor_destino = destino

        dibujar_arista(
            ventana,
            puntos[mejor_origen],
            puntos[mejor_destino]
        )

        pygame.display.update()
        pygame.time.delay(500)

        visitados.add(mejor_destino)

        costo_total += mejor_costo

    mensaje_estado = (
        f"Prim costo total: {costo_total}"
    )

    return esperar_reinicio(muros, terrenos)

def dibujar_celda(win, pos, color):
    pygame.draw.rect(win, color, (pos[1]*TAMANO_CELDA, pos[0]*TAMANO_CELDA, TAMANO_CELDA-1, TAMANO_CELDA-1))

def dibujar_arista(ventana, nodo_a, nodo_b, color=NEGRO):
    pos_a = (nodo_a[1] * TAMANO_CELDA + TAMANO_CELDA // 2, nodo_a[0] * TAMANO_CELDA + TAMANO_CELDA // 2)
    pos_b = (nodo_b[1] * TAMANO_CELDA + TAMANO_CELDA // 2, nodo_b[0] * TAMANO_CELDA + TAMANO_CELDA // 2)
    pygame.draw.line(ventana, color, pos_a, pos_b, 3)
    pygame.display.update()

def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class DisjointSet:
    def __init__(self, n):
        self.padre = list(range(n))

    def find(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.find(self.padre[x])
        return self.padre[x]

    def union(self, a, b):
        raizA = self.find(a)
        raizB = self.find(b)

        if raizA != raizB:
            self.padre[raizB] = raizA
            return True

        return False

def escribir(win, texto, x, y, fuente, color=BLANCO):
    superficie = fuente.render(texto, True, color)
    win.blit(superficie, (x, y))

def dibujar_panel(win, fuente, etapa, algoritmo,
        capturando_entrada, texto_entrada, tipo_entrada):

    pygame.draw.rect(
        win,
        (40, 40, 40),
        (ANCHO_MAPA, 0, ANCHO_PANEL, ALTO)
    )
    pygame.draw.line(win,BLANCO,(ANCHO_MAPA, 0),
    (ANCHO_MAPA, ALTO),3)

    y = 20
    escribir(win, "SIMULADOR DE GRAFOS", ANCHO_MAPA + 15, y, fuente)

    y += 40
    escribir(win, f"Etapa: {etapa}", ANCHO_MAPA + 15, y, fuente)

    y += 30
    escribir(win, f"Algoritmo:", ANCHO_MAPA + 15, y, fuente)

    y += 25
    escribir(win, algoritmo if algoritmo else "Ninguno",ANCHO_MAPA + 15, y, fuente)

    y += 50
    if etapa == 0:

        escribir(win, "1 = Busquedas", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "2 = A* y Costos", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "3 = MST", ANCHO_MAPA + 15, y, fuente)

    elif etapa == 1:
        escribir(win, "PASOS:", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "Click Inicio Y Fin. Dibuja muros y ENTER", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "B = BFS", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "D = DFS", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "L = DLS", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "I = IDDFS", ANCHO_MAPA + 15, y, fuente)

    elif etapa == 2:
        escribir(win, "Click Izq = Muro", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "Click Der = Lodo", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "A = A*", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "B = BFS", ANCHO_MAPA + 15, y, fuente)

    elif etapa == 3:
        escribir(win, "Coloca nodos", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "K = Kruskal", ANCHO_MAPA + 15, y, fuente)
        y += 25
        escribir(win, "P = Prim", ANCHO_MAPA + 15, y, fuente)
    y += 60
    escribir(win, "COLORES", ANCHO_MAPA + 15, y, fuente)
    y += 30
    pygame.draw.rect(win, VERDE,(ANCHO_MAPA + 15, y, 20, 20))
    escribir(win, "Inicio", ANCHO_MAPA + 45, y, fuente)
    y += 30
    pygame.draw.rect(win, ROJO,(ANCHO_MAPA + 15, y, 20, 20))
    escribir(win, "Fin", ANCHO_MAPA + 45, y, fuente)
    y += 30
    pygame.draw.rect(win, NEGRO,(ANCHO_MAPA + 15, y, 20, 20))
    escribir(win, "Muro", ANCHO_MAPA + 45, y, fuente)

    y += 30
    pygame.draw.rect(win, CAFE,(ANCHO_MAPA + 15, y, 20, 20))
    escribir(win, "Lodo", ANCHO_MAPA + 45, y, fuente)

    if capturando_entrada:
        y += 40

    if tipo_entrada == "DLS":
        escribir(win,"Limite de saltos:", ANCHO_MAPA + 15,y+10,fuente)

    elif tipo_entrada == "PRIM":
        escribir(win,"Nodo raiz:",ANCHO_MAPA + 15,y+10, fuente)
    pygame.draw.rect(win,BLANCO,(ANCHO_MAPA + 15, y + 30, 120, 35))

    escribir(win,texto_entrada,ANCHO_MAPA + 20,y + 35,fuente,NEGRO)

    global mensaje_estado
    y += 60

    escribir(win,"RESULTADO:",ANCHO_MAPA + 15,y+10,fuente)
    y += 35
    lineas = []
    texto = mensaje_estado

    import textwrap
    lineas = textwrap.wrap(mensaje_estado, width=25)
    for linea in lineas:
        escribir(win,linea,ANCHO_MAPA + 15, y, fuente)
        y += 25

    lineas.append(texto)

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
    fuente = pygame.font.SysFont("Arial", 18)
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Simulador de Supervivencia")
    
    inicio = None
    fin = None
    muros = set()
    puntos_interes = []
    corriendo = True
    global mensaje_estado

    etapa = 0
    algoritmo = ""
    texto_entrada = ""
    capturando_entrada = False
    tipo_entrada = ""
    while corriendo:
        ventana.fill(GRIS)
        for r in range(FILAS):
            for c in range(COLUMNAS):
                    dibujar_celda(ventana, (r, c), BLANCO)

        for m in muros: dibujar_celda(ventana, m, NEGRO)
        for t in terrenos: dibujar_celda(ventana, t, CAFE)
        if etapa in [1, 2]:
            if inicio: dibujar_celda(ventana, inicio, VERDE)
            if fin: dibujar_celda(ventana, fin, ROJO)
        elif etapa == 3:
            for p in puntos_interes:
                dibujar_celda(ventana, p, MORADO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            if etapa != 0:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Ignorar clics en el panel lateral
                    if pos[0] >= ANCHO_MAPA:
                        continue
                    fila = pos[1]//TAMANO_CELDA
                    col = pos[0]//TAMANO_CELDA
                    posicion = (fila, col)

                    #Primer Click INICIO
                    if etapa in [1,2]:
                        if inicio is None:
                            inicio = posicion
               
                        #Segundo click FIN
                        elif fin is None and posicion != inicio:
                            fin = posicion
                            if etapa == 1:
                                pygame.display.set_caption("Etapa 1: Dibuja Muros (Clic Izq.) - Elige: B, D, L o I")
                            elif etapa == 2:
                                pygame.display.set_caption("Etapa 2: Clic Izq = Muros | Clic Der = Lodo. Elige: A o B")
                    elif etapa == 3:
                        if posicion not in puntos_interes:
                            puntos_interes.append(posicion)
                            id_nodo  = len(puntos_interes) - 1
                            print(f"Nodo {id_nodo} colocado en las coordenadas: {posicion}")
                            pygame.display.set_caption(f"Etapa 3: {len(puntos_interes)} nodos. Selecciona algoritmo (K o P)")

            if evento.type == pygame.KEYDOWN:
                if capturando_entrada:
                    if evento.key == pygame.K_BACKSPACE:
                        texto_entrada = texto_entrada[:-1]
                    elif evento.key == pygame.K_RETURN:
                        capturando_entrada = False
                    elif evento.unicode.isdigit():
                        texto_entrada += evento.unicode
                    continue
                if etapa == 0:
                    if evento.key == pygame.K_1:
                        etapa = 1
                        pygame.display.set_caption("Simulador de Grafos: Etapa 1 - Coloca INICIO y FIN")
                    if evento.key == pygame.K_2:
                        etapa = 2
                        pygame.display.set_caption("Simulador de Grafos: Etapa 2 - Coloca INICIO y FIN")
                    if evento.key == pygame.K_3:
                        etapa = 3
                        puntos_interes.clear()
                        pygame.display.set_caption("Simulador de Grafos: Etapa 3 - Haz clic para colocar nodos dispersos")
                elif evento.key == pygame.K_x:
                    etapa = 0
                    muros.clear() 
                    terrenos.clear()
                    puntos_interes.clear()
                    inicio = None
                    fin = None
                    mensaje_estado = ""     
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
                        capturando_entrada = True
                        tipo_entrada = "DLS"
                        texto_entrada = ""

                        pygame.display.set_caption("DLS - Escribe limite y presiona ENTER")
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
                                if texto_entrada == "":
                                    print("Debes escribir un limite")
                                    continue
                                limite = int(texto_entrada)
                                accion = dls(inicio,fin,muros,ventana,limite,
                                             iterativa=False)
                            elif algoritmo == "ITERATIVA":
                                accion = iddfs(inicio, fin, muros, ventana)
                            if accion == "LIMPIAR":
                                inicio = None
                                fin = None
                                algoritmo = ""
                                texto_entrada = ""
                                capturando_entrada = False
                                tipo_entrada = ""
                                mensaje_estado = ""
                                pygame.display.set_caption("Simulador de Grafos: Etapa 1 - Coloca INICIO y FIN")
                            elif accion == "REINICIAR":
                                algoritmo = ""
                                texto_entrada = ""
                                capturando_entrada = False
                                tipo_entrada = ""
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
                                mensaje_estado = ""
                                pygame.display.set_caption("Simulador de Grafos: Etapa 2 - Coloca INICIO y FIN")
                            elif accion == "REINICIAR":
                                algoritmo = ""
                                pygame.display.set_caption("Simulador de Grafos: Etapa 2 - Elige: A o B")
                        else:
                            print("Debes colocar el INICIO y el FIN en el mapa antes de iniciar.")

#ETAPA 3
                elif etapa == 3 and algoritmo == "":
                    if evento.key == pygame.K_k:
                        algoritmo = "Kruskal"
                        pygame.display.set_caption("Simulador de Grafos: Etapa 3 - Kruskal [Presiona ESPACIO]")
                    elif evento.key == pygame.K_p:
                        algoritmo = "Prim"
                        capturando_entrada = True
                        tipo_entrada = "PRIM"
                        texto_entrada = ""
                        pygame.display.set_caption("Prim -Escribe nodo raiz y ENTER")

                elif etapa == 3 and algoritmo != "":
                    if evento.key == pygame.K_SPACE:
                        accion = ""
                        if len(puntos_interes) < 2:
                            print("Debes colocar al menos 2 nodos de interés para ejecutar el algoritmo.")
                            continue
                        if algoritmo == "Kruskal":
                            print("\n--- Ejecutando Kruskal ---")
                            accion = kruskal(puntos_interes, ventana, muros, terrenos)
                        elif algoritmo == "Prim":
                            print("\n--- Ejecutando Prim ---")
                            print(f"Nodos disponibles en el mapa (0 a {len(puntos_interes)-1}):")
                            for i, p in enumerate(puntos_interes):
                                print(f"  Nodo {i} -> {p}")

                            if texto_entrada == "":
                                print("Debes escribir un nodo raiz")
                                continue

                            raiz = int(texto_entrada)

                            if raiz < 0 or raiz >= len(puntos_interes):
                                print("Nodo fuera de rango")
                                continue

                            accion = prim(puntos_interes,raiz,ventana,muros,terrenos)
                        if accion == "LIMPIAR":
                            algoritmo = ""
                            mensaje_estado = ""
                            texto_entrada = ""
                            capturando_entrada = False
                            tipo_entrada = ""
                            puntos_interes.clear()
                            pygame.display.set_caption("Simulador de Grafos: Etapa 3 - Haz clic para colocar nodos dispersos")
                        elif accion == "REINICIAR":
                            algoritmo = ""
                            texto_entrada = ""
                            capturando_entrada = False
                            tipo_entrada = ""
                            pygame.display.set_caption(f"Simulador de Grafos: Etapa 3 - {len(puntos_interes)} nodos. Selecciona algoritmo (K o P)")

            if etapa in [1,2] and inicio is not None and fin is not None:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if pos[0] >= ANCHO_MAPA:
                        continue
                    fila = pos[1]//TAMANO_CELDA
                    col = pos[0]//TAMANO_CELDA
                    posicion = (fila, col)

                    if posicion != inicio and posicion != fin:
                        muros.add(posicion)

                if etapa == 2 and pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    if pos[0] >= ANCHO_MAPA:
                        continue
                    fila = pos[1]//TAMANO_CELDA
                    col = pos[0]//TAMANO_CELDA
                    posicion = (fila, col)

                    if posicion != inicio and posicion != fin  and posicion not in muros:
                        terrenos[posicion] = 5
        dibujar_panel(ventana,fuente,etapa,algoritmo,capturando_entrada,
        texto_entrada,tipo_entrada
        )
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()