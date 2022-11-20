import pygame
import math
import numpy as np
import random

pygame.init()
pygame.font.init()

height = 800
width = 600
fps = 30

hive_height = 3*height / 4

hive_n = 20
hive_size = 25
origin_pos = (width/2, 7*height/8)
war_n = 10
work_n = 20

###COLORS###
black = (27,27,27)
hive_yellow = (120,90,30)
brown = (68,44,13)
skin = (255, 216, 142)

war_image = pygame.image.load("images/kbee.png")
work_image = pygame.image.load("images/bee.png")
work_image_f = pygame.transform.flip(work_image,True,True)
hand_image = pygame.image.load("images/finger.png")

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hive-Five!')
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
        self.v = (1,1)

    def move(self):
        if self.typ == "warrior":
            if grabbing == True:
                self.speed = 5
                self.v = (player.x - self.pos[0], player.y - self.pos[1])
            else:
                #self.orig = ((width - self.orig[0])*math.cos(0.01) - (height -self.orig[1])*math.sin(0.01),(height - self.orig[1])*math.cos(0.01) + (width - self.orig[0])*math.sin(0.01))
                self.speed = 3 
                self.v = (self.orig[0] - self.pos[0], self.orig[1] - self.pos[1])
        
            if self.v != (0,0):
                self.dir = self.v/np.linalg.norm(self.v)
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
        if(self.typ == "worker"):
            if(self.di == 1):
                display.blit(work_image,(self.pos[0]-20,self.pos[1]-20))
            else:
                display.blit(work_image_f,(self.pos[0]-20,self.pos[1]-20))
        elif(self.typ == "warrior"):
            if self.v != (0,0):
                rot = pygame.transform.rotate(war_image,math.degrees(math.tan(-1*self.v[1]/self.v[0])))
                display.blit(rot,(self.pos[0]-20,self.pos[1]-20))
        #pygame.draw.rect(display,self.col,pygame.Rect(self.pos[0] - self.size/2,self.pos[1]-self.size/2,self.size,self.size))
        #pygame.draw.rect(display,(10,255,20),pygame.Rect(self.orig[0],self.orig[1],self.size,self.size))
class hand:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.d_x = origin_pos[0]
        self.d_y = origin_pos[1]
        self.de_x = origin_pos[0]
        self.de_y = -200
        self.eks = self.de_x
        self.way = self.de_y
        self.size = 50
        self.col1 = (20,20,10)
        self.col2 = brown
        self.col_dest = self.col2
        self.col_cur = self.col2

    def move(self):
        self.x += (self.d_x - self.x)*0.4
        self.y += (self.d_y - self.y)*0.2
        self.eks += (self.de_x - self.eks)*0.4
        self.way += (self.de_y - self.way)*0.2 
        self.col_cur = (self.col_cur[0] + (self.col_dest[0] - self.col_cur[0])*0.4,self.col_cur[1] + (self.col_dest[1] - self.col_cur[1])*0.4,self.col_cur[2] + (self.col_dest[2] - self.col_cur[2])*0.4)

    def draw(self):
        pygame.draw.circle(display,self.col_cur,(self.x-self.size/2 + 25,self.y-self.size/2 + 25),25)
        display.blit(hand_image,(self.eks - 30,self.way - 975))

class hive:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def draw(self):
        pygame.draw.rect(display,hive_yellow,pygame.Rect(self.x,self.y, hive_size,hive_size))

for i in range(hive_n):
    for j in range(hive_n):
        if j % 2 == 0:
            hives.append(hive(i*(width/hive_n) + 0.5*hive_size,j*(hive_height/hive_n)))
        else:
            hives.append(hive((i-0.5)*(width/hive_n) + 0.5*hive_size,j*(hive_height/hive_n)))
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
    global inhand, points
    for bee in bees:
        if bee.pos[0] > player.d_x - player.size/2 and bee.pos[0] < player.d_x + player.size/2 and bee.pos[1] > player.d_y - player.size/2 and bee.pos[1] < player.d_y + player.size/2:
            print("Collision!!!")
            points -= math.floor(inhand/2)
            inhand = 0
            return True
    return False

def end_grab():
    global points, grabbing
    randomize_bees("warrior")
    player.d_x = origin_pos[0]
    player.d_y = origin_pos[1]
    player.de_x = origin_pos[0]
    player.de_y = -200
    player.col_dest = player.col2
    points += math.floor(inhand)
    grabbing = False
    print("Points: " + str(points))

def begin_grab(): 
    global grabbing, g_since
    player.d_x = pygame.mouse.get_pos()[0]
    player.d_y = min(hive_height,pygame.mouse.get_pos()[1])
    player.de_x = player.d_x
    player.de_y = player.d_y
    player.col_dest = player.col1
    grabbing = True
    g_since = pygame.time.get_ticks()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

def main_loop():
    exitProgram = False

    global grabbing, g_since,inhand, points

    while not exitProgram:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitProgram = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                begin_grab()
                pass
            if event.type == pygame.MOUSEBUTTONUP:
                end_grab()
            if event.type == pygame.KEYDOWN:
                pass
        
        if grabbing == True:
            seconds = (pygame.time.get_ticks() - g_since)/1000
            inhand = 0.5 * 3**seconds
            
            inhand_sur = my_font.render("Collecting... " + str(math.floor(inhand)),False, (100,255,100))
            print(inhand)

        display.fill(brown)
        
        score_sur = my_font.render("SCORE: " + str(points),False,(255,255,200))


        draw_hives()
        update_bees()
        #draw_hives()
        player.draw()
        player.move()
        if (collision()):
            end_grab()
        display.blit(score_sur, (30,30))
        if grabbing == True:
            display.blit(inhand_sur,(30,60))
        pygame.display.update()
        clock.tick(fps)

player = hand(width/2,3*height/4)

main_loop()
pygame.quit()
quit()

