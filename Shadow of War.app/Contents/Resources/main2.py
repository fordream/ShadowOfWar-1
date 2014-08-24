import title, pygame
mixer=pygame.mixer
music=mixer.music
screen = title.title()
fill=screen.fill
blit=screen.blit
flip=pygame.display.flip
load=pygame.image.load
click=mixer.Sound("sounds/click.wav")
font=pygame.font.Font("font.ttf", 72)
click.set_volume(3)
click.play()
stage=1
red=None
blue=None
oppo=None
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
def stage1():
    stage=1
    while stage==1:
        fill([0,0,0])
        surf=font.render("Press A to fight an AI opponent", True, [200,0,0])
        surf2=font.render("or press C to go online", True, [200,0,0])
        surf3=font.render("or press X to go back", True, [200,0,0])
        blit(surf, [0,0])
        blit(surf2, [0,150])
        blit(surf3, [0,300])
        flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type==pygame.KEYDOWN:
                click.play()
                if event.key==pygame.K_a:
                    oppo="AI"
                    stage2()
                    return
                elif event.key==pygame.K_x:
                    click.play()
                    return 'back'
                elif event.key==pygame.K_c:
                    oppo="Online"
                    stage2()
                    return

def stage2():
    stage=2
    font=pygame.font.Font("font.ttf", 48)
    while stage==2:
        red=Button(load("images/attackred.png"), [0,100])
        blue=Button(load("images/attackblue.png"), [0,150])
        fill([0,0,0])
        surf=font.render("Press a button to play that team or X to go back", False, [100,0,0])
        blit(surf, [0,0])
        red.render(screen)
        blue.render(screen)
        flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type==pygame.MOUSEBUTTONDOWN:
                click.play()
                if red.hover():
                    blue=oppo
                    red="Human"
                    return
                elif blue.hover():
                    red=oppo
                    blue="Human"
                    return
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x:
                    click.play()
                    stage1()
                    
stage1()
pygame.quit()
raise SystemExit

                    
    
    
