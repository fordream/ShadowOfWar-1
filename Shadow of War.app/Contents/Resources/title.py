import pygame, random
pygame.init()
mixer=pygame.mixer
mixer.init()
music=mixer.music
screen=pygame.display.set_mode([1280, 960])

flip=pygame.display.flip
load=pygame.image.load
blit=screen.blit
fill=screen.fill
pygame.display.set_icon(load("images/appicon.png"))
def title():
    music.load("music/Theme.mp3")
    music.play(-1)
    title=load("images/title.png")
    f=pygame.font.Font("font.ttf", 144)
    surf=f.render("Press Space to begin", True, [0,0,0])
    flashimg=load("images/darkdragon2.png")
    pos=[140,255]
    while True:
        fill([150,0,0])
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    music.stop()
                    return screen #Go to full program
        blit(flashimg, pos)
        blit(title, [0,0])
        blit(surf, [125,500])
        flip()

if __name__=="__main__":
    title()
    pygame.quit()
    raise SystemExit
