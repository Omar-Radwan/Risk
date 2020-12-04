import pygame, sys, ctypes


# chaning the cursor of the mouse and making sound on click


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picturepath):
        super().__init__()
        self.image = pygame.image.load(picturepath)
        self.rect = self.image.get_rect()
        self.attack = pygame.mixer.Sound('attack.wav')

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self):
        self.attack.play()


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


pygame.init()
clock = pygame.time.Clock()
# pygame.mouse.set_visible(False)

backgroundimage = pygame.image.load('backgroundimage.jpg')
unitedstatesmap = pygame.image.load('unitedstatesmap.png')

crosshair = Crosshair('sword.png')

crosshairgroup = pygame.sprite.Group()
crosshairgroup.add(crosshair)

class GameState():
    def __init__(self,):
        self.state = 'intro'

    def intro(self):
        image = pygame.image.load('backgroundimage.jpg')
        screen = pygame.display.set_mode((image.get_width(), image.get_height()))
        screen.blit(backgroundimage, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # if playing mode pressed
                if screen.get_width() / 4 - 40 + 700 > mouse[
                    0] > screen.get_width() / 4 - 40 and screen.get_height() / 2 - 50 + 100 > mouse[
                    1] > screen.get_height() / 2 - 50:
                    self.state = "playingmode"
                # if simulation mode pressed
                elif screen.get_width() / 4 - 100 + 850 > mouse[
                    0] > screen.get_width() / 4 - 100 and screen.get_height() / 2 + 100 + 100 > mouse[
                    1] > screen.get_height() / 2 + 100:
                    # scren change
                    print('lel')
        # game title
        text = pygame.font.Font('freesansbold.ttf', 300)
        textsurf, textrect = text_objects("RISK", text, (0, 0, 0))
        textrect.center = (screen.get_width() / 2, screen.get_height() / 2 - 200)
        screen.blit(textsurf, textrect)

        # play button that goes to the playing mode
        text = pygame.font.Font('freesansbold.ttf', 100)
        textsurf, textrect = text_objects("Playing Mode", text, (255, 255, 255))
        textrect.center = (screen.get_width() / 2 - 25, screen.get_height() / 2)
        screen.blit(textsurf, textrect)
        s = pygame.Surface((700, 100), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((255, 255, 255, 0))  # notice the alpha value in the color
        screen.blit(s, (screen.get_width() / 4 - 40, screen.get_height() / 2 - 50))

        # play button that goes to the simulation mode
        text = pygame.font.Font('freesansbold.ttf', 100)
        textsurf, textrect = text_objects("Simulation Mode", text, (255, 255, 255))
        textrect.center = (screen.get_width() / 2 - 25, screen.get_height() / 2 + 150)
        screen.blit(textsurf, textrect)
        s = pygame.Surface((850, 100), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((255, 255, 255, 0))  # notice the alpha value in the color
        screen.blit(s, (screen.get_width() / 4 - 100, screen.get_height() / 2 + 100))
        pygame.display.update()


    def playingmode(self):
        image = pygame.image.load('unitedstatesmap.png')
        screen = pygame.display.set_mode((image.get_width(), image.get_height()))
        screen.blit(image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                crosshair.shoot()
        crosshairgroup.draw(screen)
        crosshairgroup.update()


        #code for putting the number of armies in each city
        #for city in cities

        text1 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text1,(0,255,0)) #get city.armyCount
        textrect.center = (screen.get_width() / 2, screen.get_height() / 2) #get city location
        screen.blit(textsurf, textrect)
        text2 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("2", text2, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 180, screen.get_height() / 2)  # get city location
        screen.blit(textsurf, textrect)
        text3 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("2", text3, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 350, screen.get_height() / 2)  # get city location
        screen.blit(textsurf, textrect)
        text4 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("2", text4, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 480, screen.get_height() / 2)  # get city location
        screen.blit(textsurf, textrect)
        text5 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text5, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 550, screen.get_height() / 2 + 80)  # get city location
        screen.blit(textsurf, textrect)
        text6 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text6, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 20, screen.get_height() / 2 + 120)  # get city location
        screen.blit(textsurf, textrect)
        text7 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text7, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 350, screen.get_height() / 2 + 170)  # get city location
        screen.blit(textsurf, textrect)
        text8 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("3", text8, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 250, screen.get_height() / 2 + 170)  # get city location
        screen.blit(textsurf, textrect)
        text9 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("2", text9, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 20, screen.get_height() / 2 + 250)  # get city location
        screen.blit(textsurf, textrect)
        text10 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text10, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 100, screen.get_height() / 2 + 140)  # get city location
        screen.blit(textsurf, textrect)

        text11 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("2", text11, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 495, screen.get_height() / 2 - 300)  # get city location
        screen.blit(textsurf, textrect)
        text12 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text12, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 -515, screen.get_height() / 2 - 195)  # get city location
        screen.blit(textsurf, textrect)
        text13 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text13, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 -255, screen.get_height() / 2 -250)  # get city location
        screen.blit(textsurf, textrect)
        text14 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text14, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 -65, screen.get_height() / 2 -165)  # get city location
        screen.blit(textsurf, textrect)

        text15 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text15, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 390, screen.get_height() / 2 - 160)  # get city location
        screen.blit(textsurf, textrect)
        text16 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("2", text16, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 245, screen.get_height() / 2 - 115)  # get city location
        screen.blit(textsurf, textrect)
        text17 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text17, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 65, screen.get_height() / 2 - 255)  # get city location
        screen.blit(textsurf, textrect)
        text18 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text18, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 +35, screen.get_height() / 2 - 200)  # get city location
        screen.blit(textsurf, textrect)

        text19 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("2", text19, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 - 30, screen.get_height() / 2 - 70)  # get city location
        screen.blit(textsurf, textrect)
        text20 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text20, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 80, screen.get_height() / 2 - 95)  # get city location
        screen.blit(textsurf, textrect)
        text21 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text21, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 145, screen.get_height() / 2 - 165)  # get city location
        screen.blit(textsurf, textrect)
        text22 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text22, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 360, screen.get_height() / 2 + 190)  # get city location
        screen.blit(textsurf, textrect)

        text23 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text23, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 110, screen.get_height() / 2 + 25)  # get city location
        screen.blit(textsurf, textrect)
        text24 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text24, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 175, screen.get_height() / 2 - 25)  # get city location
        screen.blit(textsurf, textrect)
        text25 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text25, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 182, screen.get_height() / 2 + 190)  # get city location
        screen.blit(textsurf, textrect)
        text26 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("2", text26, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 105, screen.get_height() / 2 + 200)  # get city location
        screen.blit(textsurf, textrect)

        text27 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text27, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 235, screen.get_height() / 2 - 45)  # get city location
        screen.blit(textsurf, textrect)
        text28 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text28, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 300, screen.get_height() / 2 - 20)  # get city location
        screen.blit(textsurf, textrect)
        text29 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text29, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 290, screen.get_height() / 2 + 55)  # get city location
        screen.blit(textsurf, textrect)
        text30 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text30, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 260, screen.get_height() / 2 + 125)  # get city location
        screen.blit(textsurf, textrect)
        text31 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text31, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 405, screen.get_height() / 2 + 245)  # get city location
        screen.blit(textsurf, textrect)

        text32 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text32, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 305, screen.get_height() / 2 - 70)  # get city location
        screen.blit(textsurf, textrect)
        text33 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text33, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 400, screen.get_height() / 2 -115)  # get city location
        screen.blit(textsurf, textrect)
        text34 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text34, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 410, screen.get_height() / 2 + 110)  # get city location
        screen.blit(textsurf, textrect)
        text35 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text35, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 485, screen.get_height() / 2 + 20)  # get city location
        screen.blit(textsurf, textrect)

        text36 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text36, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 450, screen.get_height() / 2 - 50)  # get city location
        screen.blit(textsurf, textrect)
        text37 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text37, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 380, screen.get_height() / 2 - 50)  # get city location
        screen.blit(textsurf, textrect)
        text38 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text38, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 480, screen.get_height() / 2 - 225)  # get city location
        screen.blit(textsurf, textrect)
        text39 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text39, (255, 0, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 240, screen.get_height() / 2 -175)  # get city location
        screen.blit(textsurf, textrect)
        text40 = pygame.font.Font('freesansbold.ttf', 30)
        textsurf, textrect = text_objects("1", text40, (0, 255, 0))  # get city.armyCount
        textrect.center = (screen.get_width() / 2 + 530, screen.get_height() / 2 - 265)  # get city location
        screen.blit(textsurf, textrect)
        pygame.display.update()

    def statemanager(self):
        if self.state == 'intro':
            self.intro()
        elif self.state == 'playingmode':
            self.playingmode()

#initializing gamestate
gamestate = GameState()
while True:
    gamestate.statemanager()
    clock.tick(60)

# code for making text
# text =  pygame.font.Font('freesansbold.ttf',110)
# textsurf , textrect = text_objects("A bit racey", text)
# textrect.center = (screen.get_width()/2,screen.get_height()/2)
# screen.blit(textsurf,textrect)


# the equation for collision between mouse and a rec is if mouse.x > rec.x+width && mouse.y > rec.y+height

# the equation for collision between mouse and a rec is if mouse.x > rec.x+width && mouse.y > rec.y+height

