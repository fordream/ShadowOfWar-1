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
    board.append({'team':'red','defenses':[{'name':'knight','img':load('images/knight.png'),'pos':[240,480]}],'x':pos[0],'y':pos[1],'adj':[],
                          'buildings':[{'name':'fortress','img':load('images/fortressred.png'),'pos':[640,480]}]})
for pos in poslistwhite:
    board.append({'team':'white','defenses':[{'name':'knight','img':load('images/knight.png'),'pos':[240,480]}],'x':pos[0],'y':pos[1],'adj':[],
                          'buildings':[{'name':'fortress','img':load('images/fortresswhite.png'),'pos':[640,480]}]})
for pos in poslistblue:
    board.append({'team':'blue','defenses':[{'name':'knight','img':load('images/knight.png'),'pos':[240,480]}],'x':pos[0],'y':pos[1],'adj':[],
                          'buildings':[{'name':'fortress','img':load('images/fortressblue.png'),'pos':[640,480]}]})

def getterr(pos):
    for i in board:
        if i['x'] == pos[0] and i['y'] == pos[1]:
            return i
    
for i in board:
    for terr in vars()['poslist'+i['team']]:
        i['adj'].append(getterr(terr))

    for t in board:
        if distance(i['x'],i['y'],t['x'],t['y']) <= 640:
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
    selected = None
    if turn == 'red':
        attackbutton = Button(attack_r,[50,900])
    else:
        attackbutton = Button(attack_b,[50,900])
    bg = pygame.image.load('images/map.png')
    trainbutton = Button(load('images/train.png'),[200,900])
    sellbutton = Button(load('images/sell.png'),[433,900])
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
                if attackbutton.hover() and not selected == None: # If attack button clicked...
                    click.play()

                    total = 0
                    
                    if turn == 'red':
                        for i in troopsred:
                            total+=troopsred[i]
                    else:
                        for i in troopsblue:
                            total += troopsblue[i]
                    
                    if total > 0:        
                        attack(selected)

                if trainbutton.hover():
                    click.play()
                    traintroop()

                if sellbutton.hover():
                    click.play()
                    selltroop()
                    

        screen.fill([80,48,0])
        screen.blit(bg,[-x,0])
        for land in board:
            for adj in land['adj']:
                pygame.draw.line(screen,[0,0,0],[land['x']-x,land['y']],[adj['x']-x,adj['y']],3)
        for land in board:
            pygame.draw.circle(screen,colors[land['team']],[land['x']-x,land['y']],16)
            for adj in land['adj']:
                if adj['team'] == turn and not land['team'] == turn:
                    selected = land
                    pygame.draw.circle(screen,colors[land['team']],[land['x']-x,land['y']],r,2)

        attackbutton.render(screen)
        trainbutton.render(screen)
        sellbutton.render(screen)

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
        if distance(high['pos'][0],high['pos'][1],pos[0],pos[1]) > distance(b['pos'][0],b['pos'][1],pos[0],pos[1]):
            high = b

    return b
        

def attack(selected):
    tile = load('images/grass.png')
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
                
        for building in selected['buildings']:
            blitcenter(building['img'],building['pos'])

        for t in troops:
            blitcenter(t[0],t[1])
            target=getnear(t[1])['pos']
            pos=t[1]
            if t[2]=='ninja':speed=32
            elif t[2]=='knight':speed=8
            else:speed=16
            if distance(pos[0], pos[1], target[0], target[1])>speed:
                diff=[target[0]-pos[0], target[1]-pos[1]]
                direction=math.atan(diff[1]/diff[0])
                x=math.cos(direction)*speed+pos[0]
                y=math.sin(direction)*speed+pos[1]
                t[1]=[x, y]
        
            

        for t in selected['defenses']:
            blitcenter(t['img'],t['pos'])
                         
                

        if turn == 'red':
            text(50,50,text='Troop selected: '+troopnames[troopselected].title()+' ('+str(troopsred[troopnames[troopselected]])+'). Press Space to change',size=40)
        else:
            text(50,50,text='Troop selected: '+troopnames[troopselected].title()+' ('+str(troopsblue[troopnames[troopselected]])+'). Press Space to change',size=40)

        flip()

doneloading = True

titlescreen()



