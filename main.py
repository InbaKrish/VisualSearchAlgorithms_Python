import pygame
from queue import PriorityQueue
import sys
from pygame.locals import *

#setting up the window
WIDTH = 660
HEIGHT = 710
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.font.init()
FONT = pygame.font.SysFont('chalkduster.ttc', 25)

clock = pygame.time.Clock()
pygame.display.set_caption("A* PATH FINDER")

#declaring colors - tuple
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BUT_C = (40, 42, 44)

#creating class to work with nodes (particular cubes)
class Node:

    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row,self.col

    #methods to check the status of the node considered
    def is_closed(self):
        return self.color == RED
    def is_open(self):
        return self.color == GREEN
    def is_blocked(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == PURPLE
    def is_end(self):
        return self.color == ORANGE
    
    #method to set colors
    def reset(self):
        self.color = WHITE
    def set_start(self):
        self.color = TURQUOISE
    def set_end(self):
        self.color = ORANGE
    def set_blocked(self):
        self.color = BLACK
    def set_open(self):
        self.color = GREEN
    def set_closed(self):
        self.color = RED
    def set_path(self):
        self.color = PURPLE
    
    #method to draw cubes for the specified node
    def draw_node(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    
    def check_pos(self,pos,nodes):
        x,y = pos
        return 0<=x<=len(nodes)-1 and 0<=y<=len(nodes[0])-1 and not nodes[x][y].is_blocked()
    
    #method to update neighbours
    def update_neighbour(self,nodes):
        self.neighbors = []
        directions = {"down": (1, 0),"right": (0, 1),"up": (-1, 0),"left": (0, -1)}
        for d in directions:
            x,y = directions[d]
            neighbour = (self.row+x,self.col+y)
            if self.check_pos(neighbour,nodes):
                self.neighbors.append(nodes[neighbour[0]][neighbour[1]])
                 
    #method to check whether the passed node is less than the other
    def __lt__(self,other):
        return False

#heuristic function to get the manhatten distance between two points
def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2)+abs(y1-y2)

#MAIN ALGORITHM - A* PATH FINDER
def a_star_algorithm(draw,start,end):
    pq = PriorityQueue()
    pq.put((0,start))
    g_score = {start:0}
    predecessors = {start:None}

    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = pq.get()[1]
        if current == end:
            construct_path(start,predecessors,end,draw)
            return True
            
        for neighbour in current.neighbors:
            if neighbour not in g_score:
                g_score[neighbour]  = g_score[current]+1
                f_value = g_score[neighbour] + h(current.get_pos(),end.get_pos())
                pq.put((f_value,neighbour))
                if not neighbour.is_end():
                    neighbour.set_open()
                predecessors[neighbour] = current

        draw()

        if current!=start:
            current.set_closed()
    
    return False

#BFS
def bfs_algo(draw, start, end):
    queue =[]
    queue.append(start)
    predecessors = {start:None}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = queue.pop(0)
        if current == end:
            construct_path(start,predecessors,end,draw)
            return True
        for neighbour in current.neighbors:
            if neighbour not in predecessors:
                queue.append(neighbour)
                if not neighbour.is_end():
                    neighbour.set_open()
                predecessors[neighbour] = current
        
        draw()
        if current!=start:
            current.set_closed()
    
    return False

#DFS
def dfs_algo(draw, start, end):
    stack = []
    stack.append(start)
    predecessors = {start: None}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = stack.pop()
        if current == end:
            construct_path(start, predecessors, end, draw)
            return True
        for neighbour in current.neighbors:
            if neighbour not in predecessors:
                stack.append(neighbour)
                if not neighbour.is_end():
                    neighbour.set_open()
                predecessors[neighbour] = current

        draw()
        if current != start:
            current.set_closed()

    return False

#final path draw
def construct_path(start,predecessors,current,draw):
    while current!=start:
        if not current.is_end():
            current.set_path()
        current = predecessors[current]
        draw()

#method to create and hold node objects inside a 2d list
def create_grid(total_rows,total_width):
    nodes = []
    node_width = total_width//total_rows
    for i in range(total_rows):
        nodes.append([])  #creating a 2d list
        for j in range(total_rows):
            new_node = Node(i,j,node_width,total_rows)   #Node objects 
            nodes[i].append(new_node)
    return nodes

#drawing grid lines
def draw_grid_lines(win,rows,width):
    line_width = width//rows
    pygame.draw.line(win, GREY, (0,WIDTH), (WIDTH,WIDTH))

    for i  in range(rows):
        pygame.draw.line(win,GREY,(0,i*line_width),(width,i*line_width))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*line_width,0), (j*line_width,width))
    

#main draw function 
def draw(win,nodes,rows,width):
    win.fill(WHITE)

    for row in nodes: #traversing through the 2d node object list and drawing rects with its own draw function
        for node in row:
            node.draw_node(win)

    draw_grid_lines(win,rows,width) #drwaing grid lines above the drawn rects
    #button_switch(win,algo)
    pygame.display.update()

#button selector
def button_switch(win,index):
    
    #buttons
    if index == 1:
        pygame.draw.rect(win, BUT_C, (80, 670, 80, 22), border_radius=2)
        pygame.draw.rect(win, RED, (300, 670, 80, 22), border_radius=2)
        pygame.draw.rect(win, BUT_C, (540, 670, 80, 22), border_radius=2)
    
    elif index == 2:
        pygame.draw.rect(win, BUT_C, (80, 670, 80, 22), border_radius=2)
        pygame.draw.rect(win, BUT_C, (300, 670, 80, 22), border_radius=2)
        pygame.draw.rect(win, RED, (540, 670, 80, 22), border_radius=2)
    
    else:
        pygame.draw.rect(win, RED, (80, 670, 80, 22), border_radius=2)
        pygame.draw.rect(win, BUT_C, (300, 670, 80, 22), border_radius=2)
        pygame.draw.rect(win, BUT_C, (540, 670, 80, 22), border_radius=2)

    win.blit(FONT.render('A* Algo', True, WHITE), (85, 672))
    win.blit(FONT.render('BFS', True, WHITE), (322, 672))
    win.blit(FONT.render('DFS', True, WHITE), (562, 672))
    pygame.display.update()


#get mouse pos in the maze
def get_mpos(pos,rows,width):
    x,y = pos
    gap = width//rows

    posx = x//gap
    posy = y//gap

    return posx,posy

#main function
def main(win,width):
    ROWS = 30   
    nodes = create_grid(ROWS,width)
    algo = 0

    started = False
    run = True

    start = None
    end = None

    while run:
        draw(win,nodes,ROWS,width)
        button_switch(win,algo)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            #if started: #if algo starts we need to stop interrupts except exit
             #   continue

            if pygame.mouse.get_pressed()[0]: #left button
                pos = pygame.mouse.get_pos()
                x,y = get_mpos(pos,ROWS,width)

                if pos[0]<660 and pos[1]<660:
                    node = nodes[x][y]

                    if not start and node != end:
                        start = node
                        start.set_start()
                    elif not end and node != start:
                        end = node
                        end.set_end()
                    elif node != start and node != end:
                        node.set_blocked()

            if pygame.mouse.get_pressed()[0] and not started:
                    x,y = pygame.mouse.get_pos()

                    if 79<=x<=160 and 669<=y<=693:
                        algo = 0
                        button_switch(win, algo)    
                    elif 299 <= x <= 379 and 669 <= y <= 693:
                        algo = 1
                        button_switch(win, algo)
                    elif 539 <= x <= 619 and 669 <= y <= 693:
                        algo = 2
                        button_switch(win, algo)
    
            
            elif pygame.mouse.get_pressed()[2]:  # right button
                pos = pygame.mouse.get_pos()
                x, y = get_mpos(pos, ROWS, width)
                node = nodes[x][y]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    for row in nodes:
                        for node in row:
                            node.update_neighbour(nodes)
                    if algo == 0:  
                        a_star_algorithm(lambda: draw(win, nodes, ROWS, width),start,end)
                    elif algo == 1:  
                        bfs_algo(lambda: draw(win, nodes, ROWS, width),start,end)
                    elif algo == 2:
                        dfs_algo(lambda: draw(win, nodes, ROWS, width), start, end)

                if event.key == pygame.K_c:
                    started = False 
                    start = None
                    end = None
                    nodes = create_grid(ROWS, width)

            clock.tick(30)
    pygame.quit()

main(WIN,WIDTH)
