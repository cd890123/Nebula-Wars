# -*- coding: utf-8 -*-
# By Daniel Petri 2012-2014. Graphics by Paulo Ditzel and Peter Pluecker.
# Special thanks to Michail (michailgames.com)
# Check out the 'Encyclopedia' README file to discover how this code works
# -*- CC BY-NC 4.0 -*-

#中文翻譯--戴君儒

import pygame, sys, math, random
from pygame.locals import *

if not pygame.font:
    print('Warning, fonts disabled!')
if not pygame.mixer:
    print('Warning, sound disabled!')

背景 = 'data/background/bg.jpg'
船 = 'data/living/ship.png'
流星 = 'data/rocks/meteor.png'
流星碎片 = 'data/rocks/meteor_debris.png'
地球 = 'data/rocks/earth.png'
火星 = 'data/rocks/mars.png'
木星 = 'data/rocks/jupiter.png'
敵艦_1 ='data/living/enemyship1.png'
敵艦_2 = 'data/living/enemyship2.png'
敵艦_3 = 'data/living/enemyship3.png'
玩家飛彈_1 = 'data/effects/playermissile1.png'

pygame.init()

#sound setup below (for future use)

class Player(object):
    def __init__(自己, x, y, 圖片, 生命值, 防護, 流星碰撞, 船碰撞, 射擊):
        自己.x = x
        自己.y = y
        自己.圖片 = 圖片
        自己.生命值 = 生命值
        自己.防護 = 防護
        自己.流星碰撞 = 流星碰撞
        自己.船碰撞 = 船碰撞
        自己.射擊 = 射擊
        
class Background(object):
    def __init__(自己, x, y, 圖片, 速度):
        自己.x = x
        自己.y = y
        自己.圖片 = 圖片
        自己.速度 = 速度

class Meteor(object):
    def __init__(自己, x, y, 圖片, 分數, 方向, 預設圖片):
        自己.x = x
        自己.y = y
        自己.圖片 = 圖片
        自己.分數 = 分數
        自己.方向 = 方向
        自己.旋轉 = 圖片
        自己.預設圖片 = 預設圖片

class Planet(object):
    def __init__(自己, x, y, 圖片, 大小):
        自己.x = x
        自己.y = y
        自己.圖片 = 圖片
        自己.大小 = 大小

class Ship(object):
    def __init__(自己, x, y, 圖片, 速度, 快速, 分數):
        自己.x = x
        自己.y = y
        自己.圖片 = 圖片
        自己.速度 = 速度
        自己.快速 = 快速
        自己.分數 = 分數

class Bullet(object):
    def __init__(自己, x, y, 圖片, 速度):
        自己.x = x
        自己.y = y
        自己.圖片 = 圖片
        自己.速度 = 速度

寬 = 960 # x coord
高 = 720 # y coord

#Colors
白 = (255, 255, 255)
黑 = (0,0,0)
紅 = (192,0,0)
黃 = (238,201,0)
綠 = (50, 205, 50)

太空字體 = pygame.font.Font('data/font/astro.ttf',20)

畫面 = pygame.display.set_mode((寬,高), 0, 32)
pygame.display.set_caption("Nebula Wars 0.3")

#Sprites
背景 = pygame.image.load(背景).convert()
船 = pygame.image.load(船).convert_alpha()
流星 = pygame.image.load(流星).convert_alpha()
流星碎片 = pygame.image.load(流星碎片).convert_alpha()
地球 = pygame.image.load(地球).convert_alpha()
火星 = pygame.image.load(火星).convert_alpha()
木星 = pygame.image.load(木星).convert_alpha()
敵艦_1 = pygame.image.load(敵艦_1).convert_alpha()
敵艦_2 = pygame.image.load(敵艦_2).convert_alpha()
敵艦_3 = pygame.image.load(敵艦_3).convert_alpha()
玩家飛彈_1 = pygame.image.load(玩家飛彈_1).convert_alpha()

顯示張數 = pygame.time.Clock()

#Classes
玩家=Player(0, 0, 船, 100, 100, False, False, False) # x, y, img, health, shield, meteor_collision, ship_collision, shooting
畫面背景=Background(0, 0, 背景, 1)
流星=Meteor(960, 180, 流星, 0, -1, 流星)
行星=Planet(960, 360, 地球, 3)
飛行船=Ship(960, 360, 敵艦_1, 3, 0, 0)
子彈=Bullet(寬, 0, 玩家飛彈_1, 13)

def addRocks():
    畫面.blit(行星.圖片, (行星.x, 行星.y)) #Draws
    畫面.blit(流星.圖片, (流星.x, 流星.y))
    
    #=======================Planet=====================#
    if 行星.大小 == 1:
        行星.圖片 = pygame.transform.scale(行星.圖片, (70, 72))
        行星.x -= 2
    elif 行星.大小 == 2:
        行星.圖片 = pygame.transform.scale(行星.圖片, (140, 144))
        行星.x -= 3
    else:
        行星.圖片 = pygame.transform.scale(行星.圖片, (280, 288))
        行星.x -= 4
        
    if 行星.x < -300:
       行星.圖片 = random.randint(1,3)
       if 行星.圖片 == 3:
           行星.圖片 = 地球
       if 行星.圖片 == 2:
           行星.圖片 = 火星
       if 行星.圖片 == 1:
          行星.圖片 = 木星
       行星.大小 = random.randint(1,3)
       行星.x = 980
       行星.y = random.randint(100, 500)
       
    #=======================Meteor=====================#
    流星.x -= 8 #Speed
    流星.y += 流星.方向  #Direction
    
    流星.圖片 = pygame.transform.rotate(流星.旋轉, 流星.分數)
    流星.分數 += 1

    if 玩家.流星碰撞 == True:
        流星.旋轉 = 流星碎片

    else:
        流星.旋轉 = 流星.預設圖片
        
    if 流星.x <= -120 or 流星.y > 高+120 or 流星.y < -120: #Makes meteor go back if it leaves the window or crashes into the player's ship
       流星.x = random.randint(960, 1000)
       流星.y = random.randint(50, 720)
       流星.方向 *= -1
       玩家.流星碰撞 = False
       流星.圖片 = 流星.預設圖片

def addShips():
    if not 玩家.船碰撞:
        畫面.blit(飛行船.圖片, (飛行船.x, 飛行船.y)) #Draws enemy ship
    畫面.blit(玩家.圖片, (玩家.x, 玩家.y)) #Draws player ship

    飛行船.x -= 飛行船.速度 #Moves ship sideways
    
    if 飛行船.x > 780: #Moves ship a little bit up
        飛行船.y += 飛行船.快速

    if 飛行船.圖片 == 敵艦_1: #Speed variation
        飛行船.速度 = 3
        if 飛行船.x < 640:
            飛行船.速度 = 15
            
    if 飛行船.圖片 == 敵艦_2:
        飛行船.速度 = 7
        
    if 飛行船.圖片 == 敵艦_3:
        飛行船.速度 = 5
        
    if 飛行船.x <= -120 or 飛行船.y > 高+120 or 飛行船.y < -120: #Checks if ship is offscreen. If so, adds a new one
       玩家.船碰撞 = False # Ship collision is always set to False when it spawns
       飛行船.分數 = 0 #Same applies to it's rotation
       
       飛行船.圖片 = random.randint(1,3) #Change the type of a random ship
       if 飛行船.圖片 == 3:
           飛行船.圖片 = 敵艦_3
       if 飛行船.圖片 == 2:
           飛行船.圖片 = 敵艦_2
       if 飛行船.圖片 == 1:
           飛行船.圖片 = 敵艦_1
           
       飛行船.x = random.randint(960, 1000)
       飛行船.y = random.randint(50, 650)

       if 飛行船.快速 >= 0: #Controls ship AI direction
           飛行船.快速 *= -1
       
       if 飛行船.y > 360: #Selects random Y direction
           飛行船.快速 += 0.5

       else:
           飛行船.快速 -= 0.5
           
def animateBackground():
    畫面.blit(畫面背景.圖片, (畫面背景.x, 畫面背景.y)) #BG 1
    畫面.blit(畫面背景.圖片, (畫面背景.x+寬, 畫面背景.y)) #BG 2

    畫面背景.x -= 畫面背景.速度

    if 畫面背景.x <= -960:
        畫面背景.x = 0

def drawText(文字, 字體, x, y, 顏色):
        textobj = 字體.render(文字, 1, 顏色)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        畫面.blit(textobj, textrect)

def shoot():    
    if 玩家.射擊 == True:
        畫面.blit(子彈.圖片, (子彈.x, 子彈.y)) #Blits bullet's image
        if 子彈.x < 寬:
            子彈.x += 子彈.速度

def collisionBoxes(): #Draws collision boxes and checks for them. Note to 自己: screen, color, (x, y, width, height), thickness
    ##Player##
    playerRect = [pygame.Rect(玩家.x+35, 玩家.y+28, 60, 5), #Creates multiple collision rectangles
                  pygame.Rect(玩家.x+40, 玩家.y+35, 50, 5),
                  pygame.Rect(玩家.x, 玩家.y+16, 40, 10),
                  pygame.Rect(玩家.x+16, 玩家.y+10, 10, 5),
                  pygame.Rect(玩家.x+85, 玩家.y+5, 52, 13)]

    playerBox = list(playerRect)

    #for rect in playerBox: pygame.draw.rect(screen, GREEN, rect, 1) #Allows you to see collision boxes
    #pygame.draw.rect(screen, WHITE, (player.x, player.y, 148, 43), 1)

    ##Meteor##
    meteorBox = pygame.Rect((流星.x+10), (流星.y+10), 56, 43)
    #pygame.draw.rect(screen, WHITE, meteorBox, 1)

    ##Enemy Ship##
    if 飛行船.圖片 == 敵艦_1:
        if 飛行船.x > 640:                                       ###
            shipBox = pygame.Rect(飛行船.x, 飛行船.y, 43, 11)      ###
            #pygame.draw.rect(screen, WHITE, shipBox, 1)       ###
                                                               ### Prevents a lag in enemyship1's collision box when he boosts
        else:                                                  ###
            shipBox = pygame.Rect((飛行船.x+13), 飛行船.y, 43, 11) ###
            #pygame.draw.rect(screen, WHITE, shipBox, 1)       ###

    elif 飛行船.圖片 == 敵艦_2:
        shipBox = pygame.Rect((飛行船.x+5), 飛行船.y, 70, 20)
        #pygame.draw.rect(screen, WHITE, shipBox, 1)

    elif 飛行船.圖片 == 敵艦_3:
        shipBox = pygame.Rect(飛行船.x+6, 飛行船.y, 72, 46)
        #pygame.draw.rect(screen, WHITE, shipBox, 1)

    ##Bullet##
    bulletBox = pygame.Rect(子彈.x, 子彈.y, 95, 17)
    #pygame.draw.rect(screen, YELLOW, bulletBox, 1)
    
    ############# Actual collision #############

    #If a player crashes into a meteor
    if 玩家.流星碰撞 == False:
        if 玩家.生命值 >= 0 and 流星.旋轉 != 流星碎片:
            for r1 in playerBox:
                if r1.colliderect(meteorBox):    
                    玩家.流星碰撞 = True
                    玩家.生命值 -= ((1-(玩家.防護/100))*random.randint(30,50)) # The higher your shield, the less damage you take.
                    玩家.防護 -= random.randint(15, 30)

    #If a player crashes into a ship
    def dropShip(): #Controls ship's death animation
        飛行船.y += 15
        飛行船.x -= 3
        船掉落 = pygame.transform.rotate(飛行船.圖片, 飛行船.分數)
        畫面.blit(船掉落, (飛行船.x, 飛行船.y))
        飛行船.分數 -= 3 #Similar code to how the meteor's rotation works
    
    if 玩家.船碰撞 == False:
        for r1 in playerBox:
            if r1.colliderect(shipBox):
                玩家.船碰撞 = True
                if 飛行船.圖片 == 敵艦_1:
                    if 飛行船.x < 640: # Tiny enemy ship is moving fast... lots of damage shall be taken
                        玩家.生命值 -= ((1-(玩家.防護/100))*random.randint(20,40))
                        玩家.防護 -= random.randint(10, 20)

                    else: # Tiny enemy is moving slowly
                        玩家.生命值 -= ((1-(玩家.防護/100))*random.randint(5,12))
                        玩家.防護 -= random.randint(2, 7)

                elif 飛行船.圖片 == 敵艦_2:
                    玩家.生命值 -= ((1-(玩家.防護/100))*random.randint(15,25))
                    玩家.防護 -= random.randint(19, 26)

                else:
                    玩家.生命值 -= ((1-(玩家.防護/100))*random.randint(27,37))
                    玩家.防護 -= random.randint(28, 44)
                                       
    if 玩家.船碰撞: #Starts ship's death animation
        dropShip()

    #If a bullet crashes into a ship
    if bulletBox.colliderect(shipBox):
        玩家.船碰撞 = True

    #If a bullet crashes into a meteor
    if bulletBox.colliderect(meteorBox):
        玩家.流星碰撞 = True
        
    ############# Dying and making sure your stats don't reach negative numbers #############
    if 玩家.生命值 <= 0:
        drawText('Game over', 太空字體, 400, 300, 白)
        玩家.生命值 = 0

    if 玩家.防護 < 0:
        玩家.防護 = 0
    
def draw():
    animateBackground()
    shoot()
    addRocks()
    addShips()
    collisionBoxes()
    
    #Different display colors
    if 玩家.生命值 >= 90:
        drawText('healTh: %a shielD: %a'% (round(玩家.生命值), 玩家.防護), 太空字體, 5, 5, 白)
    elif 玩家.生命值 >= 60 and 玩家.生命值 < 90:
        drawText('healTh: %a shielD: %a'% (round(玩家.生命值), 玩家.防護), 太空字體, 5, 5, 綠)
    elif 玩家.生命值 >= 40 and 玩家.生命值 < 60:
        drawText('healTh: %a shielD: %a'% (round(玩家.生命值), 玩家.防護), 太空字體, 5, 5, 黃)
    else: # player.health >= 0 and player.health < 40:
        drawText('healTh: %a shielD: %a'% (round(玩家.生命值), 玩家.防護), 太空字體, 5, 5, 紅)
    ##########################
    
def getEvents():
    FULLSCREENMODE = False
    
    for event in pygame.event.get():
        if event.type == QUIT:
            end()

        if event.type == MOUSEBUTTONDOWN:
            if 子彈.x >= 寬: # Makes sure you can't shoot more than one bullet if one has already been shot
                子彈.x = 玩家.x + 70 #Sets bullets coords for new shot
                子彈.y = 玩家.y + 5

                玩家.射擊 = True
            
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                end()
            
            elif event.key == K_F11:
                FULLSCREENMODE = not FULLSCREENMODE
                if FULLSCREENMODE:
                    畫面 = pygame.display.set_mode((寬,高), FULLSCREEN) #Fullscreen
                else:
                    畫面 = pygame.display.set_mode((寬,高), 0, 32) #Windowed

    玩家.x, 玩家.y = pygame.mouse.get_pos() #
    玩家.x -= 玩家.圖片.get_width()/2 # mouse control
    玩家.y -= 玩家.圖片.get_height()/2 #

def end():
    pygame.quit()
    sys.exit()

def main():
    while True:
        getEvents()
        draw()
        顯示張數.tick(30)
        pygame.display.update()

if __name__ == '__main__':
    main()
