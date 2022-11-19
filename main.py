import pygame
import math
import numpy as np
import random

pygame.init()

height = 800
width = 1000
fps = 30

hive_height = 3*height / 4

hive_n = 10
hive_size = 20
origin_pos = (width/2, 7*height/8)
war_n = 10
work_n = 20

###COLORS###
black = (27,27,27)
hive_yellow = (208,162,64)
brown = (68,44,13)
skin = (255, 216, 142)

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('display caption')
clock = pygame.time.Clock()

hives = list()
bees = list()

grabbing = False
g_since = pygame.time.get_ticks()
points = 0
inhand = 0

class bee:
    def __init__(self,x,y,col,typ):
        self.pos = (x,y)
        self.orig = (x,y)
        self.col = col
        self.speed = 5
        self.size = 30
        self.typ = typ
        self.di = 1
        self.diy = 1

    def move(self):
        if self.typ == "warrior":
            if grabbing == True:
                self.speed = 5
                v = (player.x - self.pos[0], player.y - self.pos[1])
            else:
                #self.orig = ((width - self.orig[0])*math.cos(0.01) - (height -self.orig[1])*math.sin(0.01),(height - self.orig[1])*math.cos(0.01) + (width - self.orig[0])*math.sin(0.01))
                self.speed = 3 
                v = (self.orig[0] - self.pos[0], self.orig[1] - self.pos[1])
        
            if v != (0,0):
                self.dir = v/np.linalg.norm(v)
                self.pos = self.pos + self.dir * self.speed 
                
    #        if grabbing = False
    #            if self.orig[0] - (self.speed+1) < self.pos[0] and self.pos[0]< self.orig[0] + (self.speed + 1):
    #                self.pos = (self.orig[0],self.pos[1])
    #            if self.pos[0] > width:
    #                self.pos[0] = width
    #            if self.orig[1] - (self.speed+1) < self.pos[1] and self.pos[1] < self.orig[1] + (self.speed + 1):
    #                self.pos = (self.pos[0],self.orig[1])
    #            if self.pos[1] > height:
    #                self.pos[1] = height
        if self.typ == "worker":
            self.orig = (self.orig[0]+(self.di*self.speed), self.orig[1])
            if self.orig[0] >= width - 20:
                self.di = -1
            if self.orig[0] <= 0 + 20:
                self.di = 1
            if self.orig[1] >= hive_height:
                self.diy = -1
            if self.orig[1] <= 0:
                self.diy = 1
            self.orig = (self.orig[0], self.orig[1] + self.diy * math.sin(math.pi * self.orig[0] / 200))
            v = (self.orig[0] - self.pos[0], self.orig[1] - self.pos[1])
            if v != (0,0):
                self.dir = v/np.linalg.norm(v)
                self.pos = self.pos + self.dir * self.speed 
    def draw(self):
        pygame.draw.rect(display,self.col,pygame.Rect(self.pos[0] - self.size/2,self.pos[1]-self.size/2,self.size,self.size))
        #pygame.draw.rect(display,(10,255,20),pygame.Rect(self.orig[0],self.orig[1],self.size,self.size))
class hand:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.d_x = origin_pos[0]
        self.d_y = origin_pos[1]
        self.size = 50

    def move(self):
        self.x += (self.d_x - self.x)*0.4
        self.y += (self.d_y - self.y)*0.2

    def draw(self):
        pygame.draw.rect(display,skin,pygame.Rect(self.x-self.size/2,self.y-self.size/2,self.size,self.size ))

class hive:
    def __init__(self,i):
        self.x = i 
        self.y = i
    def draw(self):
        pygame.draw.rect(display,hive_yellow,pygame.Rect(self.x,self.y, hive_size,hive_size))

for i in range(hive_n):
    hives.append(hive((i)))
for b in range(war_n):
    bees.append(bee(random.randint(0,width),height/2,(200,50,50),"warrior"))
for b in range(work_n):
    bees.append(bee(random.randint(0,width),(hive_height)/work_n * b, (200,200,50), "worker"))

def draw_hives():
    for hive in hives:
        hive.draw()

def update_bees():
    for bee in bees:
        bee.move()
        bee.draw()

def randomize_bees(typ):
    for bee in bees:
        if bee.typ == typ:
            bee.orig = (random.randint(0,width),random.randint(0,hive_height))

def collision():
    for bee in bees:
        if bee.pos[0] > player.d_x - player.size/2 and bee.pos[0] < player.d_x + player.size/2 and bee.pos[1] > player.d_y - player.size/2 and bee.pos[1] < player.d_y + player.size/2:
            print("Collision!!!")
            return True
    return False

def main_loop():
    exitProgram = False

    global grabbing, g_since,inhand, points

    while not exitProgram:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitProgram = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.d_x = pygame.mouse.get_pos()[0]
                player.d_y = min(hive_height,pygame.mouse.get_pos()[1])
                grabbing = True
                g_since = pygame.time.get_ticks()
                pass
            if event.type == pygame.MOUSEBUTTONUP:
                randomize_bees("warrior")
                player.d_x = origin_pos[0]
                player.d_y = origin_pos[1]
                points += math.floor(inhand)
                grabbing = False
                print("Points: " + str(points))
            if event.type == pygame.KEYDOWN:
                pass
        
        if grabbing == True:
            seconds = (pygame.time.get_ticks() - g_since)/1000
            inhand = 0.5 * 3**seconds
            print(inhand)

        display.fill(brown)
        
        update_bees()
        draw_hives()
        player.draw()
        player.move()
        collision()

        pygame.display.update()
        clock.tick(fps)

player = hand(width/2,3*height/4)

main_loop()
pygame.quit()
quit()

