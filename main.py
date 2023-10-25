import pygame
import math
from queue import PriorityQueue


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

    def __lt__(self, other):
        return False


def h(p1, p2):
    """ funcao heuristica """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


def reconstruct_path(percorrido, atual, draw):
    """Reconstroi o caminho percorrdo"""
    
    print('Caminho ficiente encontrado pelo A*')
    
    while atual in percorrido:
        atual = percorrido[atual]
        print(f"[{atual.row}, {atual.col}]")
        atual.make_path()
        draw()

def algorithm(draw, grid, start, end):
    
    """
    a implementação do a*
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
            reconstruct_path(came_from, end, draw)
            end.end()
            return True

        for neighbor in current.neighbors:
            
            if neighbor.row != current.row and neighbor.col != current.col:
                temp_g_score = g_score[current] + 2  
                
            else:
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
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

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
                g_value = font.render(f'g: {spot.g}', True, (0, 0, 0))
                h_value = font.render(f'h: {spot.h}', True, (0, 0, 0))
                f_value = font.render(f'f: {spot.g + spot.h}', True, (0, 0, 0))
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
    ROWS = 20
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

            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
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

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    
                if event.key == pygame.K_r:
                    file_path = input("Enter the path of the file: ")
                    start, end = read_from_file(file_path, grid)
                    print(start, end)
                    draw(win, grid, ROWS, width)

    pygame.quit()
    


if __name__ == '__main__':
    main(WIN, WIDTH)