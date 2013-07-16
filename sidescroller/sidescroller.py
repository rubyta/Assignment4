"""Source file name: mailPilot.py
     Author's name: Rubyta Herwinda 200183528
     Last Modified by: Rubyta Herwinda
     Date last Modified: 
     Program description:
         arcade game underwater ship seeeking treasure chests,
         avoid fish.
         
         mpChests - add treasure chest sprite
     
     Revision History:
      """
    
import pygame
from pygame.locals import *
from sys import exit
import random

pygame.init()

screen = pygame.display.set_mode((800,600))
keys = [False, False, False, False]

class Ship(pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ship.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        if not pygame.mixer:
            print ("problem with sound")
        else:
            pygame.mixer.init()
            self.sndDrop = pygame.mixer.Sound("dooropen.ogg")
            self.sndCrash = pygame.mixer.Sound("watersplash.ogg")
            self.sndShip = pygame.mixer.Sound("Submarine_Sound.ogg")
            self.sndOcean = pygame.mixer.Sound("ocean.ogg")
            #play background music
            self.sndOcean.play(-1)
            self.sndShip.play(fade_ms=1)
    
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, 400)
        
class Chests(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("treasure.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dy = 3
        
    def update(self):
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()
            
    def reset(self):
        self.rect.top = 0
        self.rect.centerx = random.randrange(3, screen.get_width())
        
class Fish(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bluefish.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()
    
    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(3, 6)
        self.dx = random.randrange(-3, 3)     

#explossion effect      
#class Effect(pygame.sprite.Sprite):
 #   def __init__(self):
  #      pygame.sprite.Sprite.__init__(self)
   #     self.images = []
    #    self.images.append(pygame.image.load("blood51.bmp"))
     #   self.images.append(pygame.image.load("blood52.bmp"))
      #  self.images.append(pygame.image.load("blood53.bmp"))
       # self.images.append(pygame.image.load("blood54.bmp"))
        #self.images.append(pygame.image.load("blood55.bmp"))
        #self.images.append(pygame.image.load("blood56.bmp"))
        
        #self.index = 0
        #self.image = self.images[self.index]
        #self.rect = pygame.Rect(5, 5, 16, 16)
            
    #def update(self):
        
     #   self.index +=1
      #  if self.index >= len(self.images):
       #     self.index = 0
        #self.image = self,images[self, index]
                    
class Underwater(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("underwater.gif")
        self.rect = self.image.get_rect()
        self.dy = 5
        self.reset()
        
    def update(self):
        self.rect.bottom += self.dy
        if self.rect.bottom >= 768:
            self.reset() 
    
    def reset(self):
        self.rect.top = -650
        
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 30)
        
    def update(self):
        self.text = "ships: %d, score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
            
def game():
    pygame.display.set_caption("Treasure Seeker!")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    ship = Ship()
    chest = Chests()
    fish1 = Fish()
    fish2 = Fish()
    fish3 = Fish()
    #blood = Effect()
    #blood_group = pygame.sprite.Group(blood)
    underwater = Underwater()
    scoreboard = Scoreboard()

    friendSprites = pygame.sprite.OrderedUpdates(underwater, chest, ship)
    fishSprites = pygame.sprite.Group(fish1, fish2, fish3)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        
        clock.tick(60)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        
        #check collisions
        
        if ship.rect.colliderect(chest.rect):
            ship.sndDrop.play()
            chest.reset()
            scoreboard.score += 100

        hitFish = pygame.sprite.spritecollide(ship, fishSprites, False)
        if hitFish:
            scoreboard.lives -= 1
            if scoreboard.lives <= 0:
                keepGoing = False
            for theFish in hitFish:
                theFish.reset()
        
        friendSprites.update()
        fishSprites.update()
        scoreSprite.update()
     #   blood_group.update()
        
        friendSprites.draw(screen)
        fishSprites.draw(screen)
        scoreSprite.draw(screen)
      #  blood_group.draw(screen)
        pygame.display.flip()
    
    ship.sndShip.stop()
    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return scoreboard.score
    
def instructions(score):
    pygame.display.set_caption("Treasure Seeker!")

    ship = Ship()
    underwater = Underwater()
    
    allSprites = pygame.sprite.Group(underwater, ship)
    insFont = pygame.font.SysFont(None, 30)
    insLabels = []
    instructions = (
    "Treasure Seeker.   Last score: %d" % score ,
    "Instructions:  You are a submarine treasure seeker,",
    "searching treasure in deep ocean.",
    "",
    "dive underwater to take treasure chests,",
    "but be careful not to sail to close",    
    "to the fish. You dont want to kill blue fish.",
    "Save the environment! Plus you dont have to have blood cloth from fish",
    "Steer with the mouse.",
    "",
    "good luck!",
    "",
    "click to start, escape to quit..."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (0, 255, 50))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    ship.sndShip.stop()    
    pygame.mouse.set_visible(True)
    return donePlaying
        
def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()


if __name__ == "__main__":
    main()
