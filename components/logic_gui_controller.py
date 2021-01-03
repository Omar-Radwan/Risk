from time import sleep

from agents.minimax_agent import MiniMaxAgent
from agents.nearly_pacifist_agent import NearlyPacifistAgent
from agents.greedy_agent import GreedyAgent
from components.game_engine import GameEngine
from game_componenets.game import Game
from gui import GUI
from game_componenets.map import Map

from agents.agressive_agent import AggressiveAgent
from agents.passive_agent import PassiveAgent

from agents.human_agent import HumanAgent
from agents.a_star_agent import AStarAgent
from agents.realtime_a_star_agent import RealTime


class LogicGuiController:
    def __init__(self):
        self.humanAgent = False
        pass

    def start(self):
        # assets = GUI()
        gameState = GUI.GameState()
        gameState.start()  # start the first two scenes to get the required parameters (tuple)
        isSimulation, redAgentString, greenAgentString, gameimage = gameState.returnTuple()
        redAgent = self.getAgent(redAgentString, True)
        greenAgent = self.getAgent(greenAgentString, False)
        print(gameimage)
        map = Map(gameimage)  # for now just read the USmap
        game = Game(map)
        gameEngine = GameEngine(isSimulation, game, redAgent, greenAgent)
        if self.humanAgent is False:
            print("msh human agent")
            while not gameEngine.gameEnded():
                gameState.modesmanager(gameEngine.game)
                sleep(0.5)
                gameEngine.play()
        else:
            print("human agent")
            while not gameEngine.gameEnded():
                while gameState.ready is False:
                    gameState.modesmanager(gameEngine.game)
                army = gameState.withArmy
                print("army is  : ", army)
                if (gameState.attackingCity.armyCount > int(army) and int(
                        army) > 1) and gameState.defendingCity.armyCount < gameState.attackingCity.armyCount:
                    gameEngine.game.move(gameState.attackingCity.id, gameState.defendingCity.id, int(army))
                    gameEngine.playvsHuman()
                gameState.defendingCity = ''
                gameState.attackingCity = ''
                gameState.withArmy = ''
                gameState.bonusAttack = False
                gameState.ready = False
                # GreedyAgent.print()

    def getAgent(self, agent, isRed):
        if agent == "greedy":
            return GreedyAgent(isRed)
        elif agent == "RT A*":
            return RealTime(isRed)
        elif agent == "aStar":
            return AStarAgent(isRed)
        elif agent == "minimax":
            return MiniMaxAgent(isRed)
        elif agent == "passive":
            return PassiveAgent(isRed)
        elif agent == "agressive":
            return AggressiveAgent(isRed)
        elif agent == "nearly":
            return NearlyPacifistAgent(isRed)
        elif agent == "human":
            self.humanAgent = True
            return HumanAgent(isRed)

    # def test(self):
    #     gameState = GUI.GameState()
    #     gameState.start()  # start the first two scenes to get the required parameters (tuple)
    #     isSimulation, redAgentString, greenAgentString, gameimage = gameState.returnTuple()
    #     map = Map()  # for now just read the USmap
    #     game = Game(map)
    #     gameEngine = GameEngine(isSimulation, game, AStarAgent(True), NearlyPacifistAgent(False))
    #     while not gameEngine.gameEnded():
    #         gameState.modesmanager(gameEngine.game)
    #         # sleep(0.5)
    #         gameEngine.play()

    def setTuple(self, isSimulation, aiAgent, nonAiAgent):
        gameState = GUI.GameState()
        print(gameState.intro())
        # tul ma m7dsh ksab el while tsht8l w ana sh8ala 3al simulation bs dlw2ty

        # print(isSimulation)
        # print(aiAgent)
        # print(nonAiAgent)

        # start the assets and take choices from the user
        # tuple(isSimulation, agent1, agent2)
        # create gameEngine and attach game to it
        # render the initial state of the game
        # ask gameEngine to process a play
        # render the new game to assets
        # ask gameEngine to process a new play
        # ........
