import imp
import multiprocessing
import pygame
import keyboard
import random
import math
import time

#Initializing pygame

pygame.init()

#Creating the visual screen

screen = pygame.display.set_mode((900,700))

#Theme

background = pygame.image.load('space.jpg')

#Title, Logo

pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

#Enemy


numEnemy = 3

listImage = []
for i in range(numEnemy):
    listImage.append(pygame.image.load('ufo.png'))

listenemyX = []
for i in range(numEnemy):
    listenemyX.append(random.randint(0,836))

listenemyY = []
for i in range(numEnemy):
    listenemyY.append(random.randint(0,150))

listenemyChange = []
for i in range(numEnemy):
    listenemyChange.append(0.5)

def enemy(x,y,i):

    #Enemy Boundaries

    global listenemyX
    global listenemyY
    global listenemyChange

    listenemyX[i]+= listenemyChange[i]

    if x >= 836:
        listenemyX[i] = 835
        listenemyY[i] += 40
        listenemyChange[i] = -0.5

    if x <= 0:
        listenemyX[i] = 1
        listenemyY[i] += 40
        listenemyChange[i] = 0.5
    
    screen.blit(listImage[i],(x,y))

#Player

playerImg = pygame.image.load('spaceship.png')
playerX = 420
playerY = 600
playerChange = 0

def player(x,y):

    #Player Boundaries

    global playerX

    if x >= 836:
        playerX = 836

    if x <= 0:
        playerX = 0

    screen.blit(playerImg,(x,y))

#Player movement

def playerMove():

    global playerChange
    global playerX

    if keyboard.is_pressed('right') or keyboard.is_pressed('d'):
        playerChange = 0.6
        playerX += playerChange

    if keyboard.is_pressed('left') or keyboard.is_pressed('a'):
        playerChange = -0.6
        playerX += playerChange

#Bullet

bulletImg = pygame.image.load('bullet_32.png')
bulletX = playerX
bulletY = 600
bulletChange = 1
state = ''
flag = 1

def bullet(x,y):
    
    global bulletY
    global bulletChange
    global state

    if keyboard.is_pressed('space') or keyboard.is_pressed('up') :
        state = 'fire'
    
    if state == 'fire':
        
        screen.blit(bulletImg,(x,y))

        bulletY -= bulletChange
            
        if bulletY <= 0:
            state = 'ready'
            bulletY = 600

#Collisions

col_count = 0

def sleep_cd():

    global level_st
    global col_count

    if col_count == numEnemy:
        level_st +=1
        col_count=0
        time.sleep(0.5)
        for i in range(numEnemy):
            listenemyX[i] = random.randint(0,836)
            listenemyY[i] = random.randint(0,150)
            
def collision(xE,yE,xB,yB,i):

    global listenemyY
    global bulletY
    global score_value
    global gold_value
    global level_st
    global col_count

    distance = math.sqrt(math.pow(xE-xB,2)+math.pow(yE-yB,2))

    if distance<=30:
        listenemyY[i]=-2000
        bulletY=0
        score_value += 1
        gold_value += 150
        col_count += 1
    
p1 = multiprocessing.Process(collision,(listenemyX[i],listenemyY[i],bulletX,bulletY,i))
p2 = multiprocessing.Process(sleep_cd)
    


#GAME OVER
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over():
    over_text = over_font.render('GAME OVER',True,(255,255,255))
    screen.blit(over_text,(260,250))

#Score 

score_value = 0
font_score = pygame.font.Font('freesansbold.ttf',32)

def show_score():
    score = font_score.render('Score : '+str(score_value),True,(255,255,255))
    screen.blit(score,(10,0))

#Gold 

gold_value = 0
font_gold = pygame.font.Font('freesansbold.ttf',32)

def show_gold():
    gold = font_gold.render('Gold : '+str(gold_value),True,(255,255,255))
    screen.blit(gold,(10,35))

#Level 

level_st = 1
font_level = pygame.font.Font('freesansbold.ttf',32)

def show_level():
    level = font_level.render('Level '+str(level_st),True,(255,255,255))
    screen.blit(level,(770,0))


#Activating the screen to stay always 

running = True

def main1():
    while running:
        
        #Screen Filling 
        screen.fill((0,0,0))
        #Background
        screen.blit(background,(0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False


        playerMove()
        
        player(playerX,playerY)

        for i in range(numEnemy):
            enemy(listenemyX[i],listenemyY[i],i)

        
        if state == 'fire' and flag == 1:
            bulletX = playerX+15
            flag += 1
        
        elif state == 'ready':
            flag = 1
            

        bullet(bulletX,bulletY)

        for i in range(numEnemy):

            if listenemyY[i]>=520:

                game_over()

                for k in range(numEnemy):
                    listenemyY[k]=2000

                break

        show_score()
        show_gold()
        show_level()

        pygame.display.update()

p3 = multiprocessing.Process(main1)

p1.start()
p2.start()
p3.start()