import pygame
import framework
import units
import random
import math
import socket
import os
import threading

pygame.init()

screen = pygame.display.set_mode([1280,960],pygame.NOFRAME) # Create window

pygame.display.set_caption("Shadow of War")

doneloading = False
font=pygame.font.Font("font.ttf", 72)

def blitcenter(surf,pos): # Blit pygame.Surface with center anchor
    screen.blit(surf,[pos[0]-surf.get_size()[0]/2,pos[1]-surf.get_size()[1]/2])

def loading():
    while not doneloading: # Mainloop
        for event in pygame.event.get(): # Event loop
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
        font=pygame.font.Font("font.ttf", 72)
        loading = font.render("Loading...",0,[200,0,0])
        blitcenter(loading,[640,480])
        pygame.display.flip()
def getangle(x1,y1,x2,y2):
    a = x2-x1
    b = y2-y1

    h = math.sqrt(a**2+b**2)

    theta = math.asin(b/float(h))

    return math.degrees(theta)

loading_thread = threading.Thread(target=loading,name='_shadowofwarloadscreen')
loading_thread.start()


logo = pygame.image.load('images/title.png')
pygame.display.set_icon(pygame.image.load('images/appicon.png'))
field = framework.Map([])
board = [] # Game map
colors = {'red':[255,0,0],'white':[255,255,255],'blue':[0,0,255]}
attack_r = pygame.image.load('images/attackred.png')
attack_b = pygame.image.load('images/attackblue.png')
selected = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mixer=pygame.mixer
music=mixer.music
fill=screen.fill
blit=screen.blit
flip=pygame.display.flip
load=pygame.image.load
click=mixer.Sound("sounds/click.wav")

click.set_volume(3)
stage=1

turn = random.choice(['red','blue'])

troopsred = {'swordsman':0,'archer':0,'orc':0,'dwarf':0,'goblin':0,'ninja':0,
          'knight':0,'wizard':0}

troopsblue = {'swordsman':0,'archer':0,'orc':0,'dwarf':0,'goblin':0,'ninja':0,
          'knight':0,'wizard':0}
goldred = 6400
goldblue = 6400

canattack = True

troopinfo = {'swordsman':{'img':load('images/swordsman.png'),'hp':75,'damage':25},
             'archer':{'img':load('images/archer.png'),'hp':75,'damage':30},
             'orc':{'img':load('images/orc.png'),'hp':90,'damage':30},
             'dwarf':{'img':load('images/dwarf.png'),'hp':100,'damage':45},
             'goblin':{'img':load('images/goblin.png'),'hp':75,'damage':40},
             'ninja':{'img':load('images/ninja.png'),'hp':50,'damage':45},
             'knight':{'img':load('images/knight.png'),'hp':200,'damage':40},
             'wizard':{'img':load('images/wizard.png'),'hp':75,'damage':50}}
                          

music.load("music/Title.mp3")
music.play(-1)

cnfg = open('options.txt','r')

lines = cnfg.readlines()

for i in lines:
    i = i.strip('\n')

music_on = lines[0] == 'True'

if not music_on:
    music.pause()

cnfg.close()

myip = socket.gethostbyname(socket.gethostname())

# Options

audio = True

def distance(x1,y1,x2,y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

def save_cfg():
    cnfg = open('options.txt','w+')
    cnfg.write(str(music_on))
    cnfg.close()
                

class Button:
    def __init__(self,surf,pos):
        self.surf = surf
        self.pos = pos
    def hover(self):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        sizex = self.surf.get_size()[0]
        sizey = self.surf.get_size()[1]
        if x>=self.pos[0] and x<=self.pos[0]+sizex:
            if y>=self.pos[1] and y<=self.pos[1]+sizey:
                return True
    def render(self,window):
        window.blit(self.surf,self.pos)

        

board = []

poslistred = [[320,640],[480,480],[480,800],[640,640]]
poslistwhite = [[320+640,640],[480+640,480],[480+640,800],[640+640,640]]
poslistblue = [[320+1280,640],[480+1280,480],[480+1280,800],[640+1280,640]]

for pos in poslistred:
    board.append({'team':'red','defenses':[[troopinfo['knight']['img'],[240,640],'knight',troopinfo['knight']['hp']]],'x':pos[0],'y':pos[1],'adj':[]})
for pos in poslistwhite:
    board.append({'team':'white','defenses':[[troopinfo['knight']['img'],[240,640],'knight',troopinfo['knight']['hp']]],'x':pos[0],'y':pos[1],'adj':[]})                       
for pos in poslistblue:
    board.append({'team':'blue','defenses':[[troopinfo['knight']['img'],[240,640],'knight',troopinfo['knight']['hp']]],'x':pos[0],'y':pos[1],'adj':[]})
        

def getterr(pos):
    for i in board:
        if i['x'] == pos[0] and i['y'] == pos[1]:
            return i
    
for i in board:
    for terr in vars()['poslist'+i['team']]:
        i['adj'].append(getterr(terr))

    for t in board:
        if distance(i['x'],i['y'],t['x'],t['y']) <= 480:
            if not t['team'] == i['team']:
                i['adj'].append(t)

    
def text(x,y,**kwargs):
    if not 'text' in kwargs:
        kwargs['text'] = ''
    if not 'color' in kwargs:
        kwargs['color'] = [0,0,0]
    if not 'size' in kwargs:
        kwargs['size'] = 50
    if not 'font' in kwargs:
        
        kwargs['font'] = 'font.ttf'
    if kwargs['font'] == None:
        kwargs['font'] = 'Consolas.ttf'
        
        
    font = pygame.font.Font(kwargs['font'],kwargs['size'])

    txt = font.render(kwargs['text'],0,kwargs['color'])

    screen.blit(txt,[x,y])

    return txt

def titlescreen(): # Titlescreen function
    red = 32
    mode = 0.5
    x = -840
    font = pygame.font.Font('font.ttf',100)
    txt = font.render("Play",0,[0,0,255])
    start = Button(txt,[x,800])

    size = txt.get_size()[0]
    
    while True: # Mainloop
        for event in pygame.event.get(): # Event loop
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                save_cfg()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start.hover():
                    click.play()
                    stage1()

        # Game render code

        screen.fill([int(red),0,0])
        blitcenter(logo,[640,400])
        start.pos = [x,800]
        start.render(screen)

        text(960,900,text='Press escape to quit',color=[0,255,0],size=40)
        pygame.display.flip() # Update

        red+=mode

        if red == 32:
            mode = 0.5
        if red == 64:
            mode = -0.5

        if x+64 < (1280-size)/2:
            x+=64
        else:
            x+=(1280-size)/2-x

def options():
    global music_on
    run = 1

    musictxt = font.render("Music On/Off",0,[200,0,0])
    back = font.render("Back",0,[200,0,0])
    musicbutton = Button(musictxt,[50,50])
    backbutton = Button(back,[50,200])

    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                save_cfg()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if musicbutton.hover():
                    click.play()
                    if not music_on:
                        music.unpause()
                        music_on = True
                    else:
                        music.pause()
                        music_on = False
                if backbutton.hover():
                    click.play()
                    stage1()
                    return

        fill([0,0,0])
        musicbutton.render(screen)
        backbutton.render(screen)
        flip()
        
        
def displayturn():
    okbutton = Button(load('images/ok.png'),[601,640])
    txt = font.render("It's the "+turn+" team's turn!",0,[200,0,0])

    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                save_cfg()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if okbutton.hover():
                    click.play()
                    run = False

        fill([0,0,0])
        okbutton.render(screen)
        blitcenter(txt,[640,320])
        flip()
        
def msg(message):
    okbutton = Button(load('images/ok.png'),[601,640])
    txt = font.render(message,0,[200,0,0])

    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                save_cfg()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if okbutton.hover():
                    click.play()
                    run = False

        fill([0,0,0])
        okbutton.render(screen)
        blitcenter(txt,[640,320])
        flip()


def stage1():
    global oppo
    stage=1
    while stage==1:
        fill([0,0,0])
        surf1=font.render("Start Game", True, [200,0,0])
        surf2=font.render("Options", True, [200,0,0])
        surf3=font.render("Back", True, [200,0,0])
        b1 = Button(surf1,[100,100])
        b2 = Button(surf2,[100,250])
        b3 = Button(surf3,[100,400])
        b1.render(screen)
        b2.render(screen)
        b3.render(screen)
        flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                save_cfg()
                raise SystemExit
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if b1.hover():
                    click.play()
                    displayturn()
                    mainmap()
                    return
                elif b2.hover():
                    click.play()
                    options()
                    return
            
                elif b3.hover():
                    click.play()
                    titlescreen()
                                            
                    return


def mainmap():
    global selected
    global turn
    global canattack

    if turn == 'red':
        attackbutton = Button(attack_r,[50,900])
    else:
        attackbutton = Button(attack_b,[50,900])
    bg = pygame.image.load('images/map.png')
    trainbutton = Button(load('images/train.png'),[200,900])
    sellbutton = Button(load('images/sell.png'),[433,900])
    placebutton = Button(load('images/place.png'),[645,900])
    endbutton = Button(load('images/end.png'),[908,900])
    x = 0
    r = 24
    rmode = 2
    pygame.key.set_repeat(1,1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                save_cfg()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x > 0:
                        x-=32
                elif event.key == pygame.K_RIGHT:
                    if x < 1067:
                        x+=32
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if attackbutton.hover() and not selected == None and canattack: # If attack button clicked...
                    click.play()

                    total = 0
                    
                    if turn == 'red':
                        for i in troopsred:
                            total+=troopsred[i]
                    else:
                        for i in troopsblue:
                            total += troopsblue[i]
                    
                    if total > 0:
                        for i in selected['adj']:
                            if not selected['team'] == turn:
                                if i['team'] == turn:
                                    attack()

                if trainbutton.hover():
                    click.play()
                    traintroop()

                if sellbutton.hover():
                    click.play()
                    selltroop()

                if placebutton.hover():
                    click.play()
                    if not selected == None:
                        if selected['team'] == turn:
                            placetroops()
                if endbutton.hover():
                    click.play()

                    if not canattack:
                        if turn == 'red':
                            turn = 'blue'
                        else:
                            turn = 'red'

                        displayturn()
                        canattack = True
                        selected = None
                        mainmap()

                pos = pygame.mouse.get_pos()
                for i in board:
                    if distance(i['x'],i['y'],pos[0]+x,pos[1]) <= 16:
                        selected = i
                    

        screen.fill([80,48,0])
        screen.blit(bg,[-x,0])
        for land in board:
            for adj in land['adj']:
                pygame.draw.line(screen,[0,0,0],[land['x']-x,land['y']],[adj['x']-x,adj['y']],3)
        for land in board:
            pygame.draw.circle(screen,colors[land['team']],[land['x']-x,land['y']],16)

            if not selected == None:
                pygame.draw.circle(screen,colors[selected['team']],[selected['x']-x,selected['y']],r,2)

        attackbutton.render(screen)
        trainbutton.render(screen)
        sellbutton.render(screen)
        placebutton.render(screen)

        if not canattack:
            endbutton.render(screen)

        if r == 30:
            rmode = -1
        if r == 24:
            rmode = 1
        r += rmode
        

        pygame.display.flip()
        
def traintroop():
    global troopsred
    global troopsblue
    global goldred
    global goldblue
    
    top = font.render("Train Troops",0,[200,0,0])

    donetxt = font.render("Done",0,[200,0,0])

    done = Button(donetxt,[1000,800])

    troopnames = ['swordsman','archer','orc','dwarf','goblin','ninja',
                  'knight','wizard']
    prices = {'swordsman':200,'archer':300,'orc':400,'dwarf':400,'goblin':500,
              'ninja':600,'knight':800,'wizard':1000}
    trooplist = ['images/swordsman.png','images/archer.png','images/orc.png',
                 'images/dwarf.png','images/goblin.png','images/ninja.png',
                 'images/knight.png','images/wizard.png']

    x = 128
    
    for i in trooplist:
        trooplist[trooplist.index(i)] = Button(load(i),[x,320])
        x+=128

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                save_cfg()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in trooplist:
                    if b.hover():
                        click.play()

                        if turn == 'red':
                            if prices[troopnames[trooplist.index(b)]] <= goldred:
                                troopsred[troopnames[trooplist.index(b)]]+=1
                                goldred-=prices[troopnames[trooplist.index(b)]]
                        else:
                            if prices[troopnames[trooplist.index(b)]] <= goldblue:
                                troopsblue[troopnames[trooplist.index(b)]]+=1
                                goldblue-=prices[troopnames[trooplist.index(b)]]

                if done.hover():
                    click.play()
                    mainmap()
                    return
                        

        fill([0,0,0])
        blitcenter(top,[640,64])

        if turn == 'red':
            top2 = font.render("Gold: "+str(goldred),0,[200,0,0])
        else:
            top2 = font.render("Gold: "+str(goldblue),0,[200,0,0]) 
        blitcenter(top2,[640,164])

        for i in trooplist:
            trooplist[trooplist.index(i)].render(screen)

        done.render(screen)
        
        y = 480

        for i in troopnames: # Half of the following line is for the sake of spacing
            if turn == 'red':
                text(512,y,text='Price: '+str(prices[i])+(' '*(4-len(str(prices[i]))))+'      '+i+': '+str(troopsred[i]),color=[200,0,0],size=48)
            else:
                text(512,y,text='Price: '+str(prices[i])+(' '*(4-len(str(prices[i]))))+'      '+i+': '+str(troopsblue[i]),color=[200,0,0],size=48)
            y+=48
        flip()

def selltroop():
    global troopsred
    global troopsblue
    global goldred
    global goldblue
    
    top = font.render("Sell Troops",0,[200,0,0])

    donetxt = font.render("Done",0,[200,0,0])

    done = Button(donetxt,[1000,800])

    troopnames = ['swordsman','archer','orc','dwarf','goblin','ninja',
                  'knight','wizard']
    prices = {'swordsman':200,'archer':300,'orc':400,'dwarf':400,'goblin':500,
              'ninja':600,'knight':800,'wizard':1000}
    trooplist = ['images/swordsman.png','images/archer.png','images/orc.png',
                 'images/dwarf.png','images/goblin.png','images/ninja.png',
                 'images/knight.png','images/wizard.png']

    x = 128
    
    for i in trooplist:
        trooplist[trooplist.index(i)] = Button(load(i),[x,320])
        x+=128
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                save_cfg()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in trooplist:
                    if b.hover():
                        click.play()

                        if turn == 'red':
                            if troopsred[troopnames[trooplist.index(b)]] > 0:
                                troopsred[troopnames[trooplist.index(b)]]-=1
                                goldred+=prices[troopnames[trooplist.index(b)]]
                        else:
                            if troopsblue[troopnames[trooplist.index(b)]] > 0:
                                troopsblue[troopnames[trooplist.index(b)]]-=1
                                goldblue+=prices[troopnames[trooplist.index(b)]]

                if done.hover():
                    click.play()
                    mainmap()
                    return
                        

        fill([0,0,0])
        blitcenter(top,[640,64])

        if turn == 'red':
            top2 = font.render("Gold: "+str(goldred),0,[200,0,0])
        else:
            top2 = font.render("Gold: "+str(goldblue),0,[200,0,0]) 
        blitcenter(top2,[640,164])

        for i in trooplist:
            trooplist[trooplist.index(i)].render(screen)

        done.render(screen)
        
        y = 480

        for i in troopnames: # Half of the following line is for the sake of spacing
            if turn == 'red':
                text(512,y,text='Price: '+str(prices[i])+(' '*(4-len(str(prices[i]))))+'      '+i+': '+str(troopsred[i]),color=[200,0,0],size=48)
            else:
                text(512,y,text='Price: '+str(prices[i])+(' '*(4-len(str(prices[i]))))+'      '+i+': '+str(troopsblue[i]),color=[200,0,0],size=48)
            y+=48
        flip()

def getnear(pos):
    high=selected['defenses'][0]
    for b in selected['defenses']:
        if distance(high[1][0],high[1][1],pos[0],pos[1]) > distance(b[1][0],b[1][1],pos[0],pos[1]):
            high = b

    return b
        
def placetroops():
    global selected
    global troopsred
    global troopsblue
    
    donetxt = font.render("Done",0,[200,0,0])
    done = Button(donetxt,[1000,800])
    
    tile = load('images/grass.png')
    fort = load('images/fortress'+selected['team']+'.png')
    troopnames = ['swordsman','archer','orc','dwarf','goblin','ninja',
                  'knight','wizard']

    troops = []
    
    troopselected = 0

    pygame.key.set_repeat(1,100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    save_cfg()
                    raise SystemExit
                elif event.key == pygame.K_SPACE:
                    if troopselected == len(troopnames)-1:
                        troopselected = 0
                    else:
                        troopselected += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                troopinfo[troopnames[troopselected]]['pos'] = pos
                if done.hover():
                    click.play()

                    mainmap()
                if turn == 'red':
                    if troopsred[troopnames[troopselected]] > 0:
                        selected['defenses'].append([troopinfo[troopnames[troopselected]]['img'],pos,troopnames[troopselected],troopinfo[troopnames[troopselected]]['hp']])
                        troopsred[troopnames[troopselected]] -= 1
                else:
                    if troopsblue[troopnames[troopselected]] > 0:
                        selected['defenses'].append([troopinfo[troopnames[troopselected]]['img'],pos,troopnames[troopselected],troopinfo[troopnames[troopselected]]['hp']])
                        troopsblue[troopnames[troopselected]] -= 1


                     
        for x in range(0,1280,256):
            for y in range(0,960,256):
                blit(tile,[x,y])
                
        blitcenter(fort,[640,480])

        for t in selected['defenses']:
            blitcenter(pygame.transform.flip(t[0],True,False),t[1])

            if t[3] < troopinfo[t[2]]['hp']:
                pygame.draw.rect(screen,[255,0,0],[t[1][0]-32,t[1][1]-72,64,8])
                pygame.draw.rect(screen,[0,255,0],[t[1][0]-32,t[1][1]-72,int(t[3]/float(troopinfo[t[2]]['hp'])*64),8])

        done.render(screen)
        
        if turn == 'red':
            text(50,50,text='Troop selected: '+troopnames[troopselected].title()+' ('+str(troopsred[troopnames[troopselected]])+'). Press Space to change',size=40)
        else:
            text(50,50,text='Troop selected: '+troopnames[troopselected].title()+' ('+str(troopsblue[troopnames[troopselected]])+'). Press Space to change',size=40)
    
        flip()


def attack():
    global goldred
    global goldblue
    global selected
    global turn
    global troopsred
    global troopsblue
    global canattack
    
    tile = load('images/grass.png')
    fort = load('images/fortress'+selected['team']+'.png')
    music.stop()
    music.load('music/Attack.wav')
    troopnames = ['swordsman','archer','orc','dwarf','goblin','ninja',
                  'knight','wizard']

    troops = []
    
    troopselected = 0

    if music_on:
        music.play(-1)

    pygame.key.set_repeat(1,100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    save_cfg()
                    raise SystemExit
                elif event.key == pygame.K_SPACE:
                    if troopselected == len(troopnames)-1:
                        troopselected = 0
                    else:
                        troopselected += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                troopinfo[troopnames[troopselected]]['pos'] = pos
                if turn == 'red':
                    if troopsred[troopnames[troopselected]] > 0:
                        troops.append([troopinfo[troopnames[troopselected]]['img'],[0,pos[1]],troopnames[troopselected],troopinfo[troopnames[troopselected]]['hp']])
                        troopsred[troopnames[troopselected]] -= 1
                else:
                    if troopsblue[troopnames[troopselected]] > 0:
                        troops.append([troopinfo[troopnames[troopselected]]['img'],[0,pos[1]],troopnames[troopselected],troopinfo[troopnames[troopselected]]['hp']])
                        troopsblue[troopnames[troopselected]] -= 1

                     
        for x in range(0,1280,256):
            for y in range(0,960,256):
                blit(tile,[x,y])
                
        blitcenter(fort,[640,480])

        for t in troops:
            blitcenter(t[0],t[1])

            if t[3] < troopinfo[t[2]]['hp']:
                pygame.draw.rect(screen,[255,0,0],[t[1][0]-32,t[1][1]-72,64,8])
                pygame.draw.rect(screen,[0,255,0],[t[1][0]-32,t[1][1]-72,int(t[3]/float(troopinfo[t[2]]['hp'])*64),8])
            targettroop=getnear(t[1])
            pos=t[1]
            if t[2]=='ninja':speed=32
            elif t[2]=='knight':speed=8
            else:speed=16
            targetpos = [targettroop[1][0]-32,targettroop[1][1]]

            deg = getangle(t[1][0],t[1][1],targetpos[0],targetpos[1])
            
            if distance(pos[0], pos[1], targetpos[0], targetpos[1])>speed:
                dx = math.cos(math.radians(deg))
                dy = math.sin(math.radians(deg))
                
                t[1] = [int(dx*speed)+t[1][0],int(dy*speed)+t[1][1]]
            else:
                targettroop[3]-=troopinfo[t[2]]['damage']/16

                if targettroop[3] <= 0:
                    selected['defenses'].remove(targettroop)

                t[3] -= troopinfo[targettroop[2]]['damage']/16

                if t[3] <= 0:
                    troops.remove(t)

                total = 0

                if turn == 'red':
                    for i in troopsred:
                        total += troopsred[i]
                else:
                    for i in troopsblue:
                        total += troopsblue[i]
                     
                if troops == [] and total == 0:
                    music.load('music/Title.mp3')
                    if music_on:
                        music.play(-1)
                    msg('Defeat!')

                    if turn == 'red' and selected['team'] == 'blue':
                        goldblue+=6400
                    elif selected['team'] == 'red':
                        goldred+=6400
                    selected=None

                    canattack = False
                    mainmap()

                if t[3] < troopinfo[t[2]]['hp']:
                    pygame.draw.rect(screen,[255,0,0],[t[1][0]-32,t[1][1]-72,64,8])
                    pygame.draw.rect(screen,[0,255,0],[t[1][0]-32,t[1][1]-72,int(t[3]/float(troopinfo[t[2]]['hp'])*64),8])

                if len(selected['defenses']) == 0:
                    selected['team'] = turn
                    music.load('music/Title.mp3')
                    selected['defenses'].append([troopinfo['knight']['img'],[240,640],'knight',troopinfo['knight']['hp']])
                    if music_on:
                        music.play(-1)
                    msg('Victory!')
                    if turn == 'red':
                        goldred+=6400
                    else:
                        goldblue+=6400


                    selected=None

                    found = False
                    
                    for i in board:
                        if not i['team'] == turn:
                            found = True

                    if not found:
                        msg(turn+'team wins the game!')
                        pygame.quit()
                        raise SystemExit


                    canattack = False
                    
                    mainmap()
                    
        
            

        for t in selected['defenses']:
            blitcenter(pygame.transform.flip(t[0],True,False),t[1])
            
            if t[3] < troopinfo[t[2]]['hp']:
                pygame.draw.rect(screen,[255,0,0],[t[1][0]-32,t[1][1]-72,64,8])
                pygame.draw.rect(screen,[0,255,0],[t[1][0]-32,t[1][1]-72,int(t[3]/float(troopinfo[t[2]]['hp'])*64),8])
                         
        
        if turn == 'red':
            text(50,50,text='Troop selected: '+troopnames[troopselected].title()+' ('+str(troopsred[troopnames[troopselected]])+'). Press Space to change',size=40)
        else:
            text(50,50,text='Troop selected: '+troopnames[troopselected].title()+' ('+str(troopsblue[troopnames[troopselected]])+'). Press Space to change',size=40)

        flip()

doneloading = True

titlescreen()



