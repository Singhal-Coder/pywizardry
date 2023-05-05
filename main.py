import pygame as p
import random
from math import sqrt,pow
from pygame import mixer
p.init()

#screen

screen=p.display.set_mode((600,600))
p.display.set_caption("Wrong Side")
icon=p.image.load("D:\Python\Game\CAR GAME\gameicon.png")
p.display.set_icon(icon)

#PLayer
player=p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\player.png"),(50,90))
player_velocity=0
player_y=475
player_x=275
playerx_change=0
#Enemy
enemyimg=[p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\enemy1.png"),(50,80)),p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\enemy2.png"),(50,80)),p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\enemy3.png"),(50,80))]
enemy_x=[121,195,275,353,430]
enemy_velocity=2
List=[]
counter=0
def enemy(no_of_enemies):
    global counter

    for i in range(no_of_enemies):
        if counter<=no_of_enemies:
            dic={}
            dic["x"]=random.choice(enemy_x)
            dic["y"]=random.randrange(-100,-1000,-150)
            dic["img"]=random.choice(enemyimg)
            List.append(dic)
            counter+=1
        
        screen.blit(List[i]['img'],(List[i]['x'],List[i]['y']))
        
        if List[i]['y']>650:
            List[i]['y']=random.randrange(-100,-1000,-150)
            List[i]['x']=random.choice(enemy_x)
        for j in range(len(List)):
            if abs(List[i]['y']-List[j]['y'])<=80 and List[i]['x']==List[j]['x'] and i!=j:
                List[i]['y']=random.randrange(-100,-1000,-150)
        List[i]['y']+=enemy_velocity

# Score
score_value=0
font=p.font.Font('freesansbold.ttf',32)
over_font = p.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    global score_value,sc
    if sc%250==0:
        score_value+=1

    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))   #s o the blit copies the pixels of one image onto the other image
                                #(x,y)  is the positional coordinates passed onto the blit for displaying the score at the speciifed poistion

def game_over_text():
    global running
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))  #True so that the text appears in a smooth or jagged way.

    player_velocity=0
    while running:
        screen.blit(over_text, (100, 250))
        show_score(350,50)
        p.display.update()
        for event in p.event.get():
            if event.type==p.QUIT:
                running=False

                break
                
    # del List

#road
roadimg=p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\\road.png"),(400,100))
L=[500,400,300,200,100,0,-100]
def road():
    for i in range(len(L)):
        screen.blit(roadimg,(100,L[i]))
        if L[i]>600:
            L[i]=-90
        L[i]+=player_velocity


#tree
treeimg=[p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\\tree1.png"),(50,50)),
        p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\\tree2.png"),(50,50)),
        p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\\tree3.png"),(50,50)),
        p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\\tree4.png"),(50,50))]
Tr=[]
count=0
def tree():
    global player_velocity,count,Tr
    for i in range(len(L)):
        if count<=len(L):
            dic={}
            dic["img"]=random.choice(treeimg)
            dic['y']=random.choice(L)

            count+=1
            Tr.append(dic)
        screen.blit(Tr[i]['img'],(540,L[i]))
        screen.blit(Tr[i]["img"],(35,L[i]))
        if Tr[i]['y']>600:
            Tr[i]['y']=-90
        Tr[i]['y']+=player_velocity





fuel=[]
def Fuelfun():
    fuelcar={"x":random.choice(enemy_x),"y":random.randrange(-100,-1000,-150),"img":p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\\fuelcar.png"),(50,80))}
    if sc%(250*4)==0:
        fuel.append(fuelcar)
    elif fuel!=[]:
        screen.blit(fuel[0]["img"],(fuel[0]['x'],fuel[0]['y']))
        fuel[0]['y']+=enemy_velocity
        for j in range(len(List)):
            if abs(fuel[0]['y']-List[j]['y'])<=80 and fuel[0]['x']==List[j]['x']:
                List[j]['y']=random.randrange(-100,-1000,-150)
        if fuel[0]['y']>650:
            fuel.pop()

            
coin=[]
def coinfun():
    coins={"x":random.choice(enemy_x),"y":random.randrange(-100,-1000,-150),"img":p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\\coin.png"),(50,80))}
    if sc%(250*3.4)==0:
        coin.append(coins)
    elif coin!=[]:
        screen.blit(coin[0]["img"],(coin[0]['x'],coin[0]['y']))
        coin[0]['y']+=enemy_velocity
        for j in range(len(List)):
            if abs(coin[0]['y']-List[j]['y'])<=80 and coin[0]['x']==List[j]['x']:
                List[j]['y']=random.randrange(-100,-1000,-150)
        if coin[0]['y']>650:
            coin.pop()




#collision
def iscollision(enemy_x,enemy_y,player_x,player_y,ene):
    global fuel,k,coin,score_value
    distance=sqrt(pow(enemy_x-player_x,2)+pow(enemy_y-player_y,2))
    req=[player.get_width(),player.get_height(),ene.get_width(),ene.get_height()]
    if (abs(enemy_x-player_x)<=req[0] or abs(enemy_x-player_x)<=req[2]) and (abs(enemy_y-player_y)<=req[1]-15 or abs(enemy_y-player_y)<=req[3]-15) and distance<=73:
        game_over_text()
    elif fuel!=[]:
        distance=sqrt(pow(fuel[0]['x']-player_x,2)+pow(fuel[0]['y']-player_y,2))
        req=[player.get_width(),player.get_height(),fuel[0]['img'].get_width(),fuel[0]['img'].get_height()]
        if (abs(fuel[0]['x']-player_x)<=req[0] or abs(fuel[0]['x']-player_x)<=req[2]) and (abs(fuel[0]['y']-player_y)<=req[1]-15 or abs(fuel[0]['y']-player_y)<=req[3]-15) and distance<=73:
            k=1
            fuel.pop()
    if coin!=[]:
        distance=sqrt(pow(coin[0]['x']-player_x,2)+pow(coin[0]['y']-player_y,2))
        req=[player.get_width(),player.get_height(),coin[0]['img'].get_width(),coin[0]['img'].get_height()]
        if (abs(coin[0]['x']-player_x)<=req[0] or abs(coin[0]['x']-player_x)<=req[2]) and (abs(coin[0]['y']-player_y)<=req[1]-15 or abs(coin[0]['y']-player_y)<=req[3]-15) and distance<=73:
            score_value+=3
            coin.pop()

    




Fuel=p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\Fuel.png"),(50,90))

sc=1
running=True
k=0
while running:
    screen.fill((0,200,0))
    road()
    tree()
    screen.blit(Fuel,(20,20))
    while k<74:
        p.draw.rect(screen,(0,0,0),[25,34,42,k])
        k+=0.03
        break
    else:
        game_over_text()


    for event in p.event.get():
        if event.type == p.QUIT:
            running=False
        elif event.type == p.KEYDOWN:
            if event.key==p.K_LEFT:
                playerx_change=-2
            if event.key==p.K_RIGHT:
                playerx_change=2
        elif event.type == p.KEYUP:
            if event.key==p.K_LEFT:
                playerx_change=0
            if event.key==p.K_RIGHT:
                playerx_change=0
            
    player_x+=playerx_change
    if player_x <=120:
        player_x = 120
    if player_x >=430:
        player_x = 430

    enemy(7)
    Fuelfun()
    coinfun()
    player_velocity=1.5
    screen.blit(player,(player_x,player_y))
    if sc%(250*5)==0 and enemy_velocity<5 and score_value>0:
        enemy_velocity+=0.7
    for i in List:
        
        iscollision(i['x'],i['y'],player_x,player_y,i['img'])
    show_score(350,50)
    p.display.update()
    sc+=1
p.quit()
quit()