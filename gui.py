from time import sleep

import pygame, sys, ctypes
from pygame.transform import rotate

from game import Game
from map import Map
from agents.greedy_agent import GreedyAgent
from agents.minimax_agent import MiniMaxAgent
from agents.nearly_pacifist_agent import NearlyPacifistAgent
from agents.agressive_agent import AggressiveAgent
# from agents.realtime_agent import
from passive_agent import PassiveAgent
from a_star_agent import AStarAgent

pygame.init()
backgroundimage = pygame.image.load('backgroundimage.jpg')
unitedstatesmap = pygame.image.load('unitedstatesmap.png')
worldMap = pygame.image.load('agents\kk.jpg')
clock = pygame.time.Clock()
gamemap = Map(filename="USmap.txt")
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

    class GameState:
        def __init__(self):
            self.state = 'intro'
            self.agent1 = ''
            self.agent2 = ''
            self.agent1bool = False
            self.agent2bool = False
            self.isSimulation = False
            self.gameimage = pygame.image.load('agents\kk.jpg')

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
                        # self.state = "playingmode"
                        self.state = "choosePlayerPlaying"
                    # if simulation mode pressed
                    elif screen.get_width() / 4 - 100 + 850 > mouse[
                        0] > screen.get_width() / 4 - 100 and screen.get_height() / 2 + 100 + 100 > mouse[
                        1] > screen.get_height() / 2 + 100:
                        # screen change
                        # self.state = "simulationMode"
                        self.state = "choosePlayerSimulation"

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

        def rendermap(self, map, cityList, screen):
            for city in range(0, len(map), 1):  # msh 3aref hena lazem len(gamemap.map)-1 wala la
                text = pygame.font.Font('freesansbold.ttf', 30)
                if cityList[city].isRedArmy:
                    color = (255, 0, 0)
                else:
                    color = (0, 255, 0)
                    # print(color , " " , cityList[city])
                textsurf, textrect = text_objects(str(cityList[city].armyCount), text, color)  # get city.armyCount
                # str(id) because the key in the dictionary is string
                textrect.center = (map[str(city)][0], map[str(city)][1])  # get city location
                screen.blit(textsurf, textrect)
                # draw rectangle over text to detect clicks
                rect = pygame.draw.rect(screen, color,
                                        pygame.Rect(map[str(city)][0] - 15,
                                                    map[str(city)][1] - 15,
                                                    30,
                                                    30), 1)

                # detect if a mouse hovered over a rect
                # hanzawed code elsoldiers placing wala attack....
                if rect.collidepoint(pygame.mouse.get_pos()):
                    rect = pygame.draw.rect(screen, color,
                                            pygame.Rect(map[str(city)][0] - 20,
                                                        map[str(city)][1] - 20,
                                                        40, 40), 3)
                else:
                    rect = pygame.draw.rect(screen, color,
                                            pygame.Rect(map[str(city)][0] - 15,
                                                        map[str(city)][1] - 15,
                                                        30, 30), 3)

        def renderSimulationMode(self, game: Game):

            cityList = game.getCityList()
            image = pygame.transform.scale(self.gameimage, (1380, 720))
            screen = pygame.display.set_mode((image.get_width(), image.get_height()))
            screen.blit(image, (0, 0))
            # for city in range(0, len(gamemap.worldMap), 1):  # msh 3aref hena lazem len(gamemap.map)-1 wala la
            #     text = pygame.font.Font('freesansbold.ttf', 30)
            #     if cityList[city].isRedArmy:
            #         color = (255, 0, 0)
            #     else:
            #         color = (0, 255, 0)
            #         # print(color , " " , cityList[city])
            #     textsurf, textrect = text_objects(str(cityList[city].armyCount), text, color)  # get city.armyCount
            #     # str(id) because the key in the dictionary is string
            #     textrect.center = (gamemap.worldMap[str(city)][0], gamemap.worldMap[str(city)][1])  # get city location
            #     screen.blit(textsurf, textrect)
            #     # draw rectangle over text to detect clicks
            #     rect = pygame.draw.rect(screen, color,
            #                             pygame.Rect(gamemap.worldMap[str(city)][0] - 15,
            #                                         gamemap.worldMap[str(city)][1] - 15,
            #                                         30,
            #                                         30), 1)
            #
            #     # detect if a mouse hovered over a rect
            #     # hanzawed code elsoldiers placing wala attack....
            #     if rect.collidepoint(pygame.mouse.get_pos()):
            #         rect = pygame.draw.rect(screen, color,
            #                                 pygame.Rect(gamemap.worldMap[str(city)][0] - 20,
            #                                             gamemap.worldMap[str(city)][1] - 20,
            #                                             40, 40), 3)
            #     else:
            #         rect = pygame.draw.rect(screen, color,
            #                                 pygame.Rect(gamemap.worldMap[str(city)][0] - 15,
            #                                             gamemap.worldMap[str(city)][1] - 15,
            #                                             30, 30), 3)
            if self.gameimage == pygame.image.load("unitedstatesmap.png"):
                map = "US"
            else:
                map = "WORLD"
            self.rendermap(map, cityList, screen)

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

        def renderPlayingmode(self, game):

            cityList = game.getCityList()

            screen = pygame.display.set_mode((self.gameimage.get_width(), self.gameimage.get_height()))
            screen.blit(self.gameimage, (0, 0))

            Quit = pygame.draw.rect(screen, (0, 0, 255), [0, 0, 140, 40])
            text = pygame.font.Font('freesansbold.ttf', 30)
            textsurf, textrect = text_objects("Quit", text, (0, 0, 0))  # get city.armyCount
            textrect.center = (Quit.center)
            screen.blit(textsurf, textrect)

            # for city in range(0, len(gamemap.map), 1):  # msh 3aref hena lazem len(gamemap.map)-1 wala la
            #     text = pygame.font.Font('freesansbold.ttf', 30)
            #     if cityList[city].isRedArmy:
            #         color = (255, 0, 0)
            #     else:
            #         color = (0, 255, 0)
            #     #print(color , " " , cityList[city])
            #     textsurf, textrect = text_objects(str(cityList[city].armyCount), text, color)  # get city.armyCount
            #     # str(id) because the key in the dictionary is string
            #     textrect.center = (gamemap.map[str(city)][0], gamemap.map[str(city)][1])  # get city location
            #     screen.blit(textsurf, textrect)
            #     # draw rectangle over text to detect clicks
            #     center = (gamemap.map[str(city)][0], gamemap.map[str(city)][1])
            #     rect = pygame.draw.circle(screen, color, center, 20, 2)  # Here <<<
            #
            #     # detect if a mouse hovered over a rect
            #     # hanzawed code elsoldiers placing wala attack....
            #     if rect.collidepoint(pygame.mouse.get_pos()):
            #         center = (gamemap.map[str(city)][0], gamemap.map[str(city)][1])
            #         pygame.draw.circle(screen, color, center, 30, 3)
            if self.gameimage == pygame.image.load("unitedstatesmap.png"):
                map = gamemap.map
            else:
                map = gamemap.worldMap
            self.rendermap(map, cityList, screen)

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
                    print(mouse)
                    if screen.get_width() - 873 > mouse[
                        0] > screen.get_width() - 1013 and screen.get_height() - 313 > mouse[
                        1] > screen.get_height() - 354:
                        print("greedy")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "greedy"
                        else:
                            self.agent2bool = True
                            self.agent2 = "greedy"

                    elif screen.get_width() - 898 > mouse[
                        0] > screen.get_width() - 1007 and screen.get_height() - 214 > mouse[
                        1] > screen.get_height() - 254:
                        # scren change
                        print("RT A*")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "RT A*"
                        else:
                            self.agent2bool = True
                            self.agent2 = "RT A*"
                    elif screen.get_width() - 960 > mouse[
                        0] > screen.get_width() - 1005 and screen.get_height() - 264 > mouse[
                        1] > screen.get_height() - 304:
                        # scren change
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "aStar"
                        else:
                            self.agent2bool = True
                            self.agent2 = "aStar"
                        print("A*")
                    elif screen.get_width() - 838 > mouse[
                        0] > screen.get_width() - 1007 and screen.get_height() - 164 > mouse[
                        1] > screen.get_height() - 204:
                        # scren change
                        print("minimax")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "minimax"
                        else:
                            self.agent2bool = True
                            self.agent2 = "minimax"
                    elif screen.get_width() - 387 > mouse[
                        0] > screen.get_width() - 538 and screen.get_height() - 314 > mouse[
                        1] > screen.get_height() - 354:
                        # scren change
                        print("passive")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "passive"
                        else:
                            self.agent2bool = True
                            self.agent2 = "passive"
                    elif screen.get_width() - 346 > mouse[
                        0] > screen.get_width() - 539 and screen.get_height() - 263 > mouse[
                        1] > screen.get_height() - 305:
                        # scren change
                        print("agressive")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "agressive"
                        else:
                            self.agent2bool = True
                            self.agent2 = "agressive"
                    elif screen.get_width() - 252 > mouse[
                        0] > screen.get_width() - 533 and screen.get_height() - 213 > mouse[
                        1] > screen.get_height() - 254:
                        # scren change
                        print("nearly")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "nearly"
                        else:
                            self.agent2bool = True
                            self.agent2 = "nearly"
                    elif 758 > mouse[0] > 609 and 696 > mouse[1] > 666:
                        self.gameimage = pygame.image.load("unitedstatesmap.png")
                    elif 1181 > mouse[0] > 926 and 696 > mouse[1] > 666:
                        self.gameimage = pygame.image.load("agents/kk.jpg")
                        # self.gameimage = pygame.transform.scale(self.gameimage, (1380, 720))

            # game title

            # coordinateList = [(),(),(),() .... ]
            # for tuple in coordinateList:
            #     width,height,dada,mama,oma7ma = tuple
            #

            self.coordinates(screen, 0, -200, "RISK")
            self.coordinates(screen, -270, -30, "AI Agents")
            self.coordinates(screen, -260, 50, "Greedy")
            self.coordinates(screen, -300, 100, "A*")
            self.coordinates(screen, -270, 150, "RT A*")
            self.coordinates(screen, -240, 200, "minimax")
            self.coordinates(screen, 220, 50, "Passive")
            self.coordinates(screen, 280, -30, "Non AI Agents")
            self.coordinates(screen, 240, 100, "Agressive")
            self.coordinates(screen, 290, 150, "Nearly pacifist")
            self.coordinates(screen, 0, 300, "USMAP")
            self.coordinates(screen, 380, 300, "WORLD MAP")

            if self.agent1bool is True and self.agent2bool is True:
                self.state = "simulationMode"
            pygame.display.update()
            # myTuple=(True,self.aiAgent,self.nonAiAgent)
            # print(myTuple)
            # return myTuple

        def coordinates(self, screen, x, y, string):
            text = pygame.font.Font('freesansbold.ttf', 40)
            textsurf, textrect = text_objects(string, text, (0, 0, 0))
            textrect.center = (screen.get_width() / 2 + x, screen.get_height() / 2 + y)
            screen.blit(textsurf, textrect)

        def choosePlayerModePlaying(self):
            image = pygame.image.load('backgroundimage.jpg')
            screen = pygame.display.set_mode((image.get_width(), image.get_height()))
            screen.blit(backgroundimage, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()

                    if screen.get_width() - 873 > mouse[
                        0] > screen.get_width() - 1013 and screen.get_height() - 313 > mouse[
                        1] > screen.get_height() - 354:
                        print("greedy")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "greedy"

                    elif screen.get_width() - 898 > mouse[
                        0] > screen.get_width() - 1007 and screen.get_height() - 214 > mouse[
                        1] > screen.get_height() - 254:
                        # scren change
                        print("RT A*")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "RT A*"
                    elif screen.get_width() - 960 > mouse[
                        0] > screen.get_width() - 1005 and screen.get_height() - 264 > mouse[
                        1] > screen.get_height() - 304:
                        # scren change
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "aStar"
                        print("A*")
                    elif screen.get_width() - 838 > mouse[
                        0] > screen.get_width() - 1007 and screen.get_height() - 164 > mouse[
                        1] > screen.get_height() - 204:
                        # scren change
                        print("minimax")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "minimax"
                    elif screen.get_width() - 387 > mouse[
                        0] > screen.get_width() - 538 and screen.get_height() - 314 > mouse[
                        1] > screen.get_height() - 354:
                        # scren change
                        print("passive")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "passive"
                    elif screen.get_width() - 346 > mouse[
                        0] > screen.get_width() - 539 and screen.get_height() - 263 > mouse[
                        1] > screen.get_height() - 305:
                        # scren change
                        print("agressive")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "agressive"
                    elif screen.get_width() - 252 > mouse[
                        0] > screen.get_width() - 533 and screen.get_height() - 213 > mouse[
                        1] > screen.get_height() - 254:
                        # scren change
                        print("nearly")
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "nearly"
                    elif 758 > mouse[0] > 609 and 696 > mouse[1] > 666:
                        self.gameimage = pygame.image.load("unitedstatesmap.png")
                    elif 1181 > mouse[0] > 926 and 696 > mouse[1] > 666:
                        self.gameimage = pygame.image.load("agents/kk.jpg")

            # game title

            # coordinateList = [(),(),(),() .... ]
            # for tuple in coordinateList:
            #     width,height,dada,mama,oma7ma = tuple

            self.coordinates(screen, 0, -200, "RISK")
            self.coordinates(screen, -270, -30, "AI Agents")
            self.coordinates(screen, -260, 50, "Greedy")
            self.coordinates(screen, -300, 100, "A*")
            self.coordinates(screen, -270, 150, "RT A*")
            self.coordinates(screen, -240, 200, "minimax")
            self.coordinates(screen, 220, 50, "Passive")
            self.coordinates(screen, 280, -30, "Non AI Agents")
            self.coordinates(screen, 240, 100, "Agressive")
            self.coordinates(screen, 290, 150, "Nearly pacifist")
            self.coordinates(screen, 0, 300, "USMAP")
            self.coordinates(screen, 380, 300, "WORLD MAP")
            if self.agent1bool is True:
                self.state = "playingmode"
            pygame.display.update()

        def statemanager(self):
            if self.state == 'intro':
                self.intro()
            elif self.state == 'choosePlayerPlaying':
                self.choosePlayerModePlaying()
            elif self.state == 'choosePlayerSimulation':
                self.isSimulation = True
                self.choosePlayerModeSimulation()

        def modesmanager(self, game):
            if self.state == 'playingmode':
                self.renderPlayingmode(game)
            elif self.state == 'simulationMode':
                self.renderSimulationMode(game)

        def returnTuple(self):
            while ((self.state == "choosePlayerPlaying" and (len(self.agent1) == 0 and len(self.agent2) == 0))
                   or (self.state == "choosePlayerSimulation" and (
                            len(self.agent1) == 0 or len(self.agent2) == 0))  # neb2a nshof elsimulation
                   or self.state == "intro"):
                self.statemanager()
                clock.tick(60)
            if self.gameimage == pygame.image.load("unitedstatesmap.png"):
                image = "US"
            else:
                image = "WORLD"
            return (self.isSimulation, self.agent1, self.agent2, image)

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
