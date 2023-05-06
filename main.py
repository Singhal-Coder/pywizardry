import pygame as p
import random
from math import sqrt,pow
from pygame import mixer
p.init()

#screen

screen=p.display.set_mode((600,600))
p.display.set_caption("Wrong Side")
icon=p.image.load("D:\Python\Game\CAR GAME\sprites\gameicon.png")
p.display.set_icon(icon)
mixer.music.load("D:\Python\Game\CAR GAME\\audio\\background.mp3")
mixer.music.play(-1)
#PLayer
player=p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\player.png"),(50,90))
player_velocity=0
player_y=475
player_x=275
playerx_change=0
x_velocity=3
#Enemy
enemyimg=[p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\enemy1.png"),(50,80)),p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\enemy2.png"),(50,80)),p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\enemy3.png"),(50,80))]
enemy_x=[121,195,275,353,430]
enemy_velocity=2.4
List=[]
counter=0
clock=p.time.Clock()
pol_img=p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\police.png"),(50,80))
police=[pol_img]
occurance=[0.33,0.33,0.33,0.01]
x=0
police_sound=mixer.Sound("D:\Python\Game\CAR GAME\\audio\\police.wav")
def enemy(no_of_enemies):
    global counter,x
    clock.tick(60)
    for i in range(no_of_enemies):
        if counter<=no_of_enemies:
            dic={}
            dic["x"]=random.choice(enemy_x)
            dic["y"]=random.randrange(-100,-1000,-150)
            dic["img"]=random.choice(enemyimg)
            List.append(dic)
            counter+=1
        
        screen.blit(List[i]['img'],(List[i]['x'],List[i]['y']))
        if List[i]["img"]==pol_img:
            List[i]['y']+=3

        if List[i]['y']>650:
            if List[i]["img"]==pol_img:
                police_sound.stop()
                police.append(pol_img)
                enemy_x.append(x)
                occurance.append(0.01)
            List[i]['y']=random.randrange(-100,-1000,-150)
            List[i]['x']=random.choice(enemy_x)
            List[i]["img"]=random.choices(enemyimg+police,occurance,k=1)[0]
            if List[i]["img"]==pol_img:
                List[i]["y"]=-50
                police.pop()
                x=enemy_x.pop(enemy_x.index(List[i]['x']))
                occurance.pop()
        if List[i]['y']==-50 and List[i]["img"]==pol_img :
            police_sound.play(-1)

        for j in range(len(List)):
            if List[i]["img"]==pol_img:
                if i!=j and List[i]['y']<List[j]['y']<550 and List[i]['x']==List[j]['x']:
                    List[i]['y']-=3
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
    screen.blit(score, (x, y))   

def game_over_text():
    global running
    over_text = over_font.render("GAME OVER", True, (255, 255, 255)) 
    mixer.music.stop()
    player_velocity=0
    while running:
        screen.blit(over_text, (100, 250))
        show_score(350,50)
        p.display.update()
        for event in p.event.get():
            if event.type==p.QUIT:
                running=False

                break
                

#road
roadimg=p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\\road.png"),(400,100))
L=[500,400,300,200,100,0,-100]
def road():
    for i in range(len(L)):
        screen.blit(roadimg,(100,L[i]))
        if L[i]>600:
            L[i]=-90
        L[i]+=player_velocity


#tree
treeimg=[p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\\tree1.png"),(50,50)),
        p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\\tree2.png"),(50,50)),
        p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\\tree3.png"),(50,50)),
        p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\\tree4.png"),(50,50))]
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
    fuelcar={"x":random.choice(enemy_x),"y":random.randrange(-100,-1000,-150),"img":p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\\fuelcar.png"),(50,80))}
    if sc%(250*random.randint(3,6))==0:
        fuel.append(fuelcar)
    elif fuel!=[]:
        screen.blit(fuel[0]["img"],(fuel[0]['x'],fuel[0]['y']))
        fuel[0]['y']+=enemy_velocity
        for j in range(len(List)):
            if abs(fuel[0]['y']-List[j]['y'])<=80 and fuel[0]['x']==List[j]['x']:
                fuel[0]['y']=random.randrange(-100,-1000,-150)
        if fuel[0]['y']>650:
            fuel.pop()

            





#collision
def iscollision(enemy_x,enemy_y,player_x,player_y,ene):
    global fuel,k,coin,score_value
    distance=sqrt(pow(enemy_x-player_x,2)+pow(enemy_y-player_y,2))
    req=[player.get_width(),player.get_height(),ene.get_width(),ene.get_height()]
    if (abs(enemy_x-player_x)<=req[0] or abs(enemy_x-player_x)<=req[2]) and (abs(enemy_y-player_y)<=req[1]-15 or abs(enemy_y-player_y)<=req[3]-15) and distance<=73:
        crashsound=mixer.Sound("D:\Python\Game\CAR GAME\\audio\crash.mp3")
        crashsound.play()
        game_over_text()
    elif fuel!=[]:
        distance=sqrt(pow(fuel[0]['x']-player_x,2)+pow(fuel[0]['y']-player_y,2))
        req=[player.get_width(),player.get_height(),fuel[0]['img'].get_width(),fuel[0]['img'].get_height()]
        if (abs(fuel[0]['x']-player_x)<=req[0] or abs(fuel[0]['x']-player_x)<=req[2]) and (abs(fuel[0]['y']-player_y)<=req[1]-15 or abs(fuel[0]['y']-player_y)<=req[3]-15) and distance<=73:
            k=1
            fuelsound=mixer.Sound("D:\Python\Game\CAR GAME\\audio\\fuel_sound.mp3")
            fuelsound.play()
            fuel.pop()
    




Fuel=p.transform.scale(p.image.load("D:\Python\Game\CAR GAME\sprites\Fuel.png"),(50,90))

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
                playerx_change=-x_velocity
            if event.key==p.K_RIGHT:
                playerx_change=x_velocity
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
    player_velocity=2
    screen.blit(player,(player_x,player_y))
    if sc%(250*5)==0 and enemy_velocity<5 and score_value>0:
        enemy_velocity+=0.7
        x_velocity+=0.3
    for i in List:
        
        iscollision(i['x'],i['y'],player_x,player_y,i['img'])
    show_score(350,50)
    p.display.update()
    sc+=1
    if sc%(250*13)==0:
        mixer.music.rewind()
p.quit()
quit()