import pygame, sys, ctypes
from pygame.transform import rotate

from game import Game
from map import Map

pygame.init()
backgroundimage = pygame.image.load('backgroundimage.jpg')
unitedstatesmap = pygame.image.load('unitedstatesmap.png')
worldMap=pygame.image.load('agents\kk.jpg')
clock = pygame.time.Clock()
gamemap = Map(filename="map1.txt")
game = Game(map=gamemap)
game.prepare()


# pygame.mouse.set_visible(False)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


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


crosshair = Crosshair('sword.png')

crosshairgroup = pygame.sprite.Group()
crosshairgroup.add(crosshair)


class GUI:
    # chaning the cursor of the mouse and making sound on click

    class GameState():
        def __init__(self, ):
            self.state = 'intro'
            self.aiAgent=''
            self.nonAiAgent=''

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
                        #self.state = "playingmode"
                        self.state="choosePlayerPlaying"
                    # if simulation mode pressed
                    elif screen.get_width() / 4 - 100 + 850 > mouse[
                        0] > screen.get_width() / 4 - 100 and screen.get_height() / 2 + 100 + 100 > mouse[
                        1] > screen.get_height() / 2 + 100:
                        # scren change
                        #self.state = "simulationMode"
                        self.state="choosePlayerSimulation"

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

        def simulationMode(self):
                image = pygame.image.load('agents\kk.jpg')

                cityList = game.getCityList()
                image = pygame.transform.scale(image, (1380, 720))
                screen = pygame.display.set_mode((image.get_width(), image.get_height()))
                screen.blit(image, (0, 0))
                for city in range(0, len(gamemap.worldMap), 1):  # msh 3aref hena lazem len(gamemap.map)-1 wala la
                    text = pygame.font.Font('freesansbold.ttf', 30)
                    if cityList[city].isRedArmy:
                        color = (255, 0, 0)
                    else:
                        color = (0, 255, 0)
                        # print(color , " " , cityList[city])
                    textsurf, textrect = text_objects(str(cityList[city].armyCount), text, color)  # get city.armyCount
                    # str(id) because the key in the dictionary is string
                    textrect.center = (gamemap.worldMap[str(city)][0], gamemap.worldMap[str(city)][1])  # get city location
                    screen.blit(textsurf, textrect)
                    # draw rectangle over text to detect clicks
                    rect = pygame.draw.rect(screen, color,
                                            pygame.Rect(gamemap.worldMap[str(city)][0] - 15, gamemap.worldMap[str(city)][1] - 15,
                                                        30,
                                                        30), 1)

                    # detect if a mouse hovered over a rect
                    # hanzawed code elsoldiers placing wala attack....
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        rect = pygame.draw.rect(screen, color,
                                                pygame.Rect(gamemap.worldMap[str(city)][0] - 20,
                                                            gamemap.worldMap[str(city)][1] - 20,
                                                            40, 40), 3)
                    else:
                        rect = pygame.draw.rect(screen, color,
                                                pygame.Rect(gamemap.worldMap[str(city)][0] - 15,
                                                            gamemap.worldMap[str(city)][1] - 15,
                                                            30, 30), 3)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEMOTION:
                        for city in range(0, len(gamemap.worldMap) - 1, 1):
                            if pygame.mouse.get_pos() == gamemap.worldMap[str(city)]:
                                text = pygame.font.Font('freesansbold.ttf', 30)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(pygame.mouse.get_pos())
                        crosshair.shoot()
                # loop over the cities to check the color with city is the index (or id) of the city

                crosshairgroup.draw(screen)
                crosshairgroup.update()
                pygame.display.update()
        def playingmode(self):
            image = pygame.image.load('unitedstatesmap.png')

            cityList = game.getCityList()
            screen = pygame.display.set_mode((image.get_width(), image.get_height()))
            screen.blit(image, (0, 0))

            Quit = pygame.draw.rect(screen, (0,0,255), [0,0, 140, 40])
            text = pygame.font.Font('freesansbold.ttf', 30)
            textsurf, textrect = text_objects("Quit", text, (0,0,0))  # get city.armyCount
            textrect.center = (Quit.center)
            screen.blit(textsurf, textrect)

            for city in range(0, len(gamemap.map), 1):  # msh 3aref hena lazem len(gamemap.map)-1 wala la
                text = pygame.font.Font('freesansbold.ttf', 30)
                if cityList[city].isRedArmy:
                    color = (255, 0, 0)
                else:
                    color = (0, 255, 0)
                    # print(color , " " , cityList[city])
                textsurf, textrect = text_objects(str(cityList[city].armyCount), text, color)  # get city.armyCount
                # str(id) because the key in the dictionary is string
                textrect.center = (gamemap.map[str(city)][0], gamemap.map[str(city)][1])  # get city location
                screen.blit(textsurf, textrect)
                # draw rectangle over text to detect clicks
                center = (gamemap.map[str(city)][0], gamemap.map[str(city)][1])
                rect = pygame.draw.circle(screen, color, center, 20,2)  # Here <<<

                #detect if a mouse hovered over a rect
                #hanzawed code elsoldiers placing wala attack....
                if rect.collidepoint(pygame.mouse.get_pos()):
                    center = (gamemap.map[str(city)][0], gamemap.map[str(city)][1])
                    pygame.draw.circle(screen, color, center, 30,3)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    for city in range(0, len(gamemap.map) - 1, 1):
                        if pygame.mouse.get_pos() == gamemap.map[str(city)]:
                            text = pygame.font.Font('freesansbold.ttf', 30)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 140 > pygame.mouse.get_pos()[0] > 0 and 40 > pygame.mouse.get_pos()[1] > 0:
                        print("Quit")
                        self.state = "intro"
                    print(pygame.mouse.get_pos())
                    crosshair.shoot()
            # loop over the cities to check the color with city is the index (or id) of the city

            crosshairgroup.draw(screen)
            crosshairgroup.update()
            pygame.display.update()
        def choosePlayerModeSimulation(self):
            image = pygame.image.load('backgroundimage.jpg')
            screen = pygame.display.set_mode((image.get_width(), image.get_height()))
            screen.blit(backgroundimage, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()

                    if screen.get_width()-873  > mouse[
                        0] > screen.get_width()-1013  and screen.get_height() -313 > mouse[
                        1] > screen.get_height()-354 :
                        print("greedy")

                    elif screen.get_width()-898 > mouse[
                        0] > screen.get_width()-1007 and screen.get_height() -214 > mouse[
                        1] > screen.get_height() -254:
                        # scren change
                        print("RT A*")
                    elif screen.get_width()-960 > mouse[
                        0] > screen.get_width()-1005 and screen.get_height() -264 > mouse[
                        1] > screen.get_height() -304:
                        # scren change
                        print("A*")
                    elif screen.get_width()-838 > mouse[
                        0] > screen.get_width()-1007 and screen.get_height() -164 > mouse[
                        1] > screen.get_height() -204:
                        # scren change
                        print("minimax")
                    elif screen.get_width() - 387 > mouse[
                        0] > screen.get_width() - 538 and screen.get_height() - 314 > mouse[
                        1] > screen.get_height() - 354:
                        # scren change
                        print("passive")
                    elif screen.get_width() - 346 > mouse[
                        0] > screen.get_width() - 539 and screen.get_height() - 263 > mouse[
                        1] > screen.get_height() - 305:
                        # scren change
                        print("agressive")
                    elif screen.get_width() - 252 > mouse[
                        0] > screen.get_width() - 533 and screen.get_height() - 213 > mouse[
                        1] > screen.get_height() - 254:
                        # scren change
                        print("nearly")
            # game title
            text = pygame.font.Font('freesansbold.ttf', 300)
            textsurf, textrect = text_objects("RISK", text, (0, 0, 0))
            textrect.center = (screen.get_width() / 2, screen.get_height() / 2 - 200)
            screen.blit(textsurf, textrect)

            # play button that goes to the playing mode
            text = pygame.font.Font('freesansbold.ttf', 50)
            textsurf, textrect = text_objects("AI Agents", text, (255, 255, 255))
            textrect.center = (screen.get_width() / 2 - 270, screen.get_height() / 2 - 30)
            screen.blit(textsurf, textrect)


            text = pygame.font.Font('freesansbold.ttf', 40)
            textsurf, textrect = text_objects("Greedy", text, (255, 255, 255))
            textrect.center = (screen.get_width() / 2 - 260, screen.get_height() / 2 + 50)
            screen.blit(textsurf, textrect)


            text = pygame.font.Font('freesansbold.ttf', 40)
            textsurf, textrect = text_objects("A*", text, (255, 255, 255))
            textrect.center = (screen.get_width() / 2 - 300, screen.get_height() / 2 + 100)
            screen.blit(textsurf, textrect)



            text = pygame.font.Font('freesansbold.ttf', 40)
            textsurf, textrect = text_objects("RT A*", text, (255, 255, 255))
            textrect.center = (screen.get_width() / 2 - 270, screen.get_height() / 2 + 150)
            screen.blit(textsurf, textrect)


            text = pygame.font.Font('freesansbold.ttf', 40)
            textsurf, textrect = text_objects("minimax", text, (255, 255, 255))
            textrect.center = (screen.get_width() / 2 - 240, screen.get_height() / 2 + 200)
            screen.blit(textsurf, textrect)


            text = pygame.font.Font('freesansbold.ttf', 50)
            textsurf, textrect = text_objects("Non AI Agents", text, (255, 255, 255))
            textrect.center = (screen.get_width() / 2 + 280, screen.get_height() / 2 -30)
            screen.blit(textsurf, textrect)


            text = pygame.font.Font('freesansbold.ttf', 40)
            textsurf, textrect = text_objects("Passive", text, (255, 255, 255))
            textrect.center = (screen.get_width() / 2 + 220, screen.get_height() / 2 + 50)
            screen.blit(textsurf, textrect)



            text = pygame.font.Font('freesansbold.ttf', 40)
            textsurf, textrect = text_objects("Agressive", text, (255, 255, 255))
            textrect.center = (screen.get_width() / 2 + 240, screen.get_height() / 2 + 100)
            screen.blit(textsurf, textrect)




            text = pygame.font.Font('freesansbold.ttf', 40)
            textsurf, textrect = text_objects("Nearly pacifist", text, (255, 255, 255))
            textrect.center = (screen.get_width() / 2 + 290, screen.get_height() / 2 +150)
            screen.blit(textsurf, textrect)

       


            pygame.display.update()
        def choosePlayerModePlaying(self):
                image = pygame.image.load('backgroundimage.jpg')
                screen = pygame.display.set_mode((image.get_width(), image.get_height()))
                screen.blit(backgroundimage, (0, 0))

                # game title
                text = pygame.font.Font('freesansbold.ttf', 300)
                textsurf, textrect = text_objects("RISK", text, (0, 0, 0))
                textrect.center = (screen.get_width() / 2, screen.get_height() / 2 - 200)
                screen.blit(textsurf, textrect)

                # play button that goes to the playing mode
                text = pygame.font.Font('freesansbold.ttf', 50)
                textsurf, textrect = text_objects("AI Agents", text, (255, 255, 255))
                textrect.center = (screen.get_width() / 2 , screen.get_height() / 2 - 30)
                screen.blit(textsurf, textrect)
                s = pygame.Surface((700, 60), pygame.SRCALPHA)  # per-pixel alpha
                s.fill((255, 255, 255, 0))  # notice the alpha value in the color
                screen.blit(s, (screen.get_width() / 4 - 40, screen.get_height() / 2 - 50))

                text = pygame.font.Font('freesansbold.ttf', 40)
                textsurf, textrect = text_objects("Greedy", text, (255, 255, 255))
                textrect.center = (screen.get_width() / 2 , screen.get_height() / 2 + 50)
                screen.blit(textsurf, textrect)
                s = pygame.Surface((700, 100), pygame.SRCALPHA)  # per-pixel alpha
                s.fill((255, 255, 255, 0))  # notice the alpha value in the color
                screen.blit(s, (screen.get_width() / 4 - 40, screen.get_height() / 2 - 50))

                text = pygame.font.Font('freesansbold.ttf', 40)
                textsurf, textrect = text_objects("A*", text, (255, 255, 255))
                textrect.center = (screen.get_width() / 2 , screen.get_height() / 2 + 100)
                screen.blit(textsurf, textrect)
                s = pygame.Surface((700, 100), pygame.SRCALPHA)  # per-pixel alpha
                s.fill((255, 255, 255, 0))  # notice the alpha value in the color
                screen.blit(s, (screen.get_width() / 4 - 40, screen.get_height() / 2 - 50))

                text = pygame.font.Font('freesansbold.ttf', 40)
                textsurf, textrect = text_objects("RT A*", text, (255, 255, 255))
                textrect.center = (screen.get_width() / 2 , screen.get_height() / 2 + 150)
                screen.blit(textsurf, textrect)
                s = pygame.Surface((700, 100), pygame.SRCALPHA)  # per-pixel alpha
                s.fill((255, 255, 255, 0))  # notice the alpha value in the color
                screen.blit(s, (screen.get_width() / 4 - 40, screen.get_height() / 2 - 50))

                text = pygame.font.Font('freesansbold.ttf', 40)
                textsurf, textrect = text_objects("minimax", text, (255, 255, 255))
                textrect.center = (screen.get_width() / 2 , screen.get_height() / 2 + 200)
                screen.blit(textsurf, textrect)
                s = pygame.Surface((700, 100), pygame.SRCALPHA)  # per-pixel alpha
                s.fill((255, 255, 255, 0))  # notice the alpha value in the color
                screen.blit(s, (screen.get_width() / 4 - 40, screen.get_height() / 2 - 50))
                pygame.display.update()


        def statemanager(self):
            if self.state == 'intro':
                self.intro()
            elif self.state == 'choosePlayerPlaying':
                self.choosePlayerModePlaying()
            elif self.state == 'choosePlayerSimulation':
                self.choosePlayerModeSimulation()
            elif self.state == 'playingmode':
                self.playingmode()
            elif self.state == 'simulationMode':
                self.simulationMode()

    # initializing gamestate
    gamestate = GameState()
    while True:
        gamestate.statemanager()
        clock.tick(60)

# # code for making text
# # text =  pygame.font.Font('freesansbold.ttf',110)
# # textsurf , textrect = text_objects("A bit racey", text)
# # textrect.center = (screen.get_width()/2,screen.get_height()/2)
# # screen.blit(textsurf,textrect)
#
#
# # the equation for collision between mouse and a rec is if mouse.x > rec.x+width && mouse.y > rec.y+height
#
# # the equation for collision between mouse and a rec is if mouse.x > rec.x+width && mouse.y > rec.y+height
