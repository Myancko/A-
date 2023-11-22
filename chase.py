import pygame
import math
from queue import PriorityQueue
import time


WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)

# Node class to keep track of each spot on the grid
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        
        self.g = float('inf')
        self.h = float('inf') 
        self.f = float('inf') 
        
        self.x = row * width
        self.y = col * width
        self.color = BLACK
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def update_g(self, g):
        self.g = g
        
    def update_h(self, h):
        self.h = h

    #pra evitar ter q ficar alterando os valores dps
    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == WHITE

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = BLACK

    def make_closed(self):
        self.color = GREEN

    def make_open(self):
        self.color = RED

    def make_barrier(self):
        self.color = WHITE

    def start(self):
        self.color = ORANGE

    def end(self):
        self.color = TURQUOISE

    def make_path(self):
       
        self.color = BLUE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        """
        altera os vizinho e verifica aonde pode ou não ser vizinho, para evitar que o algoritimo ande por cima de colunas.
        
        """
        self.neighbors = []
        
        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier():  
            # down-right
            self.neighbors.append(grid[self.row + 1][self.col + 1])
        if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier():  
            # down-left
            self.neighbors.append(grid[self.row + 1][self.col - 1])
        if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier():  
            # up-right
            self.neighbors.append(grid[self.row - 1][self.col + 1])
        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier():  
            # up-left
            self.neighbors.append(grid[self.row - 1][self.col - 1])
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  
            # down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  
            # up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # 
            #right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  
            # left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __str__  (self):
        
        if self.color == ORANGE:
            
            return f'Start: x = {self.row}, y = {self.col}, ghf = ({self.g} {self.h} {self.f})'
        
        elif self.color == TURQUOISE:
            
            return f'End: x = {self.row}, y = {self.col}, ghf = ({self.g} {self.h} {self.f})'
        
        else:
        
            return f'x = {self.row}, y = {self.col}, ghf = ({self.g} {self.h} {self.f})'
    
    def __lt__(self, other):
        return False


def h(p1, p2):
    """ funcao heuristica """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


def reconstruct_path(percorrido, atual, draw):
    """Reconstroi o caminho percorrdo"""
    
    #print('Caminho ficiente encontrado pelo A*')
    x = atual
    caminho = []

    while atual in percorrido:
        atual = percorrido[atual]
        #print(f"[{atual.row}, {atual.col}]")
        caminho.append([atual.row, atual.col])
        #atual.make_path()
        
    draw()
    atual.start()
    return caminho

def algorithm(draw, grid, start, end):
    """
    A* algorithm implementation
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            caminho_percorrido = reconstruct_path(came_from, end, draw)
            end.end()
            return came_from, caminho_percorrido

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                neighbor.update_g(temp_g_score)
                neighbor.update_h(h(neighbor.get_pos(), end.get_pos()))
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    #neighbor.make_open()

        #draw()

        #if current != start:
            #current.make_closed()

    return False

def escape_algorithm(draw, grid, start, end):
    """
    A* algorithm implementation
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            caminho_percorrido = reconstruct_path(came_from, end, draw)
            end.start()
            start.end()
            return came_from, caminho_percorrido

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                neighbor.update_g(temp_g_score)
                neighbor.update_h(h(neighbor.get_pos(), end.get_pos()))
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    #neighbor.make_open()

        #draw()

        #if current != start:
        #    current.make_closed()

    return False

def test(draw, grid, start, end, way, way_end):
    
    #print(grid, ' <<<')
    try:
        way.pop(-1)
    except:
        pass
    
    format_grid = []
    row_fix = []
    formated_matrix = str('[')
    
    st_fix = start
    end_fix  = end
    
    start = None
    end = None
    next = None
    
    for row in grid: #preparar a matrix para iniciar a caçada
        for node in row:  
            
            x = str(node.row)
            y = str(node.col)
            
            row_fix.append([node.row, node.col])
            #print(node, '<<')
            
            if node.color == ORANGE:
                
                formated_matrix = formated_matrix + f'[S],'
                start = node
                continue
                
            elif node.color == TURQUOISE:
                
                formated_matrix = formated_matrix + f'[E],'
                end = node
                continue
                
            elif node.color == BLUE:
                
                node.reset()
                formated_matrix = formated_matrix + f'[-],'
                continue
                
            elif node.color == WHITE:
                
                formated_matrix = formated_matrix + f'[|],'
                continue
            
            else:
                formated_matrix = formated_matrix + f'[0],'
                continue
                
        formated_matrix = formated_matrix + f'\n'  
        format_grid.append(row)
        row = []
        
    print(formated_matrix)
    print(way)

    nei = []
    
    #print(way_end)
    next = []
    try:
        end.reset()
    except:
        pass
    end = grid[way_end[-1][0]][way_end[-1][1]]
    print(end, end.neighbors)
    
    for nei in end.neighbors:
        n = nei.g + nei.h
        next.append([n,nei])
        print(nei)
    
    worst_max = max(next)
    print(worst_max[1], 'aq')
    #input('<<<')
    

    count = 0
    while True:
        
        if len(way) == 0:
            break
        
        for row in grid: 
            
            for node in row:      
                
                if way:
                    if node.row == way[-1][0] and node.col == way[-1][1]:

                        start.color = BLACK
                        node.color = ORANGE
                        start = node
                        try:
                            grid[worst_max[1].row][worst_max[1].col].end()
                            ne = grid[worst_max[1].row][worst_max[1].col]
                            #print(ne, '<<<<<<<<<')
                        except:
                            input('erro aq')
                        
                        
                        #draw()
                        #input('wait')
                        #print(way, worst_max[1], '<<<')
                        

                        #print(way, '<<<<<<')
                        try:
                            way.pop(-1)

                        except:

                            start.reset()
                            grid[worst_max[1].row][worst_max[1].col].start()
                                
                        
                        return 0, start, ne
                        
                    else:
                        count+= 1
                        print('test while', count)

                        continue
                    
                else:
                    
                    print('tes')
 
    start.reset()
    grid[worst_max[1].row][worst_max[1].col].start()
    draw()

def make_grid(rows, width):
    """
    faz o mapa
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    """
    desenha as linhas entre os quadrados
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, WHITE, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, WHITE, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    """
    desenha os quadrados
    """
    win.fill(BLACK)

    for row in grid:
        for spot in row:
            spot.draw(win)
            if spot.g != math.inf or spot.h != math.inf:
                font = pygame.font.SysFont("comicsans", 8)
                g_value = font.render(f'g: {spot.g}', True, BLACK)
                h_value = font.render(f'h: {spot.h}', True, BLACK)
                f_value = font.render(f'f: {spot.g + spot.h}', True, BLACK)
                win.blit(g_value, (spot.x + 1, spot.y + 1))
                win.blit(h_value, (spot.x + 1, spot.y + 10))
                win.blit(f_value, (spot.x + 1, spot.y + 19))

    draw_grid(win, rows, width)
    pygame.display.update()
    
def get_clicked_pos(pos, rows, width):
    """
    obtem a posição aonde ocorreu o click do mouse
    """
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def read_from_file(file_path, grid):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()
            for j in range(len(line)):
                if line[j] == '1':
                    grid[j][i].make_barrier()
                elif line[j] == 'S':
                    s = grid[j][i]
                    grid[j][i].start()
                    
                elif line[j] == 'E':
                    e = grid[j][i]
                    grid[j][i].end()
                    
        return s, e
def main(win, width):
    pygame.font.init()
    ROWS = 8
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.start()
                elif not end and spot != start:
                    end = spot
                    end.end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    started = True
                    while started:
                        
                        alg, perco = algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                        alg_end, perco_end = escape_algorithm(lambda: draw(win, grid, ROWS, width), grid, end, start)
                        count = 0
                        if alg:
                            
                            x = alg
                            for obj in x:
                                #print(obj, type(obj))
                                count += 1
                            #print(count, perco, len(perco))
                            draw(win, grid, ROWS, width)

                            re, new_s, new_e = test(lambda: draw(win, grid, ROWS, width), grid, start, end, perco, perco_end)
                            #print('s>',start, 'e>',end , '\n>', new_s, new_e)
                            #input('><><>')
                            while re == 0:
                                clock = pygame.time.Clock()
                                clock.tick(5)
                                
                                alg, perco = algorithm(lambda: draw(win, grid, ROWS, width), grid, new_s, new_e)
                                alg_end, perco_end = escape_algorithm(lambda: draw(win, grid, ROWS, width), grid, new_e, new_s)
                                
                                #print(perco, perco_end)
                                    
                                try:re, new_s, new_e = test(lambda: draw(win, grid, ROWS, width), grid, start, end, perco, perco_end)
                                except:re = test(lambda: draw(win, grid, ROWS, width), grid, start, end, perco, perco_end)
                                

                            #print('xx')
                            

                        started = False

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_r:
                    file_path = input("Enter the path of the file: ")
                    start, end = read_from_file(file_path, grid)
                    #print(start, end)
                    draw(win, grid, ROWS, width)

    pygame.quit()

if __name__ == '__main__':
    main(WIN, WIDTH)