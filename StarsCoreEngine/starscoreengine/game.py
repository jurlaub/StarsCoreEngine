"""
    This file is part of Stars Core Engine, which provides an interface and 
    processing of Game data. 

    Copyright (C) 2014  <Joshua Urlaub + Contributors>

    Stars Core Engine is free software: you can redistribute it and/or modify
    it under the terms of the Lesser GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Stars Core Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Lesser GNU General Public License for more details.

    You should have received a copy of the Lesser GNU General Public License
    along with Stars Core Engine.  If not, see <http://www.gnu.org/licenses/>.

    Contributors to this project agree to abide by the interpretation expressed 
    in the COPYING.Interpretation document.

"""

'''
Items used by the client that need some information / code from the model layer.
http://starsautohost.org/sahforum2/index.php?t=msg&th=2780&start=0&rid=0


'''
import sys
import argparse

from .space_objects import SpaceObjects
from .universe import UniverseObject
from .planet import Colony
from .productionQ import ProductionQ
from . import fleets
from .custom_setup import customSetupDialog
from .custom_setup import customSetupController
from .custom_setup import customTechDialog
from .player import RaceData, Player
from .template import planetNameTemplate
from .template import StandardGameTemplate
from .game_utility import printGameValues
from .game_utility import GamePickle, createXYFile, createMFile
from .game_utility import loadFileFromJSON, saveFileToJSON
from .game_xfile import processDesign
from .order_of_events import OrderOfEvents
from .tech import Component, Hull, ShipDesign
from .template_race import startingDesigns





class Game(object):
    """
    Game will follow a 'singleton' concept. There can be Only One game of 
    any given name in the same folder

    Game() accepts game data from the StandardGameTemplate and turns it into
    a complete game with its cooresponding game obects.

    StandardGameTemplate grabs race (r1) files from the cwd.

    NOTE:
    Game should be the primary source connected to all data objects in the game. 
    No data objects should be independent of the Game object. 
    OrderOfEvents processes the Game object.

    """

    def __init__(self, template):
        # singleton game name check?

        self.game_name = template.game_name
        self.year = 2400 
        self.game_variables = {"DesignCapacity" : 12 }

        # -- a dictionary of Technology Component Objects
        self.technology = self.generateTechnology(template)

        # -- A dictionary of Universe Objects
        self.game_universe = self.generateUniverses(template)

        # -- a dictionary of Player Objects
        self.players = self.generatePlayers(template)  #--TODO-- resolve name conflict with UniverseObject.Players


    


    def generateUniverses(self, template):
        '''
        Generates the number of universes specified in the template file. 
        >> template.universeNumber must be >= 1
        

        '''

        tmpUniverses = {}
        #---TODO--- PLANET_NAMES access planet name list

        for i in range(0, int(template.universeNumber)):

            # --TODO-- PLANET_NAMES send planet name list to universes => each 
            #          planet should have a unique name across universes
            newUni = UniverseObject(i, template.universe_data[i])       
            tmpUniverses[i] = newUni

        return tmpUniverses

    def generateTechnology(self, template):
        """ generateTechnology translates the Technology Tree from 
        StandardGameTemplate into a mix of Hull and Component objects. 

        input: (vetted) Technology Tree from StandardGameTemplate
        output: dictionary of Component and Hull objects - key is Component Name

        """
        tmpTechnology = {}
        techTree = template.technology

        for eachKey, eachObj in techTree.items():
            #eachObj = techTree[eachKey]

            if 'slot' in eachObj:  
                newTech = Hull()
            else:    
                newTech = Component()

            # newTech.__dict__.update(eachObj.__dict__)   # ?
            for i in eachObj:
                newTech.__dict__[i] = eachObj[i]


            tmpTechnology[eachKey] = newTech

        return tmpTechnology

    def generatePlayers(self, template):
        '''
        input: list of raceData objects 
                (StandardGameTemplate grabs from .r1 
                files or development standard object)

        output: creates a dictionary of player objects
                Player Object Dictionary key = "player" + (0 to N)


        '''

        raceObjectList = template.players_data

        # --TODO --- way to see the min spacing between players? 
        # --TODO --- randomly sort players by universe -> or use the SGT value

        tmpPlayers = {}

        n = 0
        for race in raceObjectList:
            tmpKey = ("player%s" % str(n))
            player = Player(race, n, self.game_universe, self.technology)
            #player.playerNumber = n

            # updating players design capacity
            if self.game_variables['DesignCapacity'] != player.designs.DesignCapacity:

                designCapacity = self.game_variables['DesignCapacity']
                player.design.DesignCapacity = designCapacity


            # -------- add starting ship designs --------
            startingShipDesigns = startingDesigns()
            processDesign(startingShipDesigns, player, self.technology)



            tmpPlayers[tmpKey] = player
            n+=1


        # Go through Universe list and assign players to Universe
        # if Universes have more player slots then players = no additional value added
        # if Universes have less player slots then players are not assigned.

        playNumb = 0
        for uniKey, universe in self.game_universe.items():   
            #universe = self.game_universe[uniKey]   
            
            # add players' HW to each universe
            for p in range(0, int(universe.Players)):
                tmpKey = ("player%s" % str(playNumb))

                # if there are enough players add to the universe
                if tmpKey in tmpPlayers:
                    player = tmpPlayers[tmpKey]

                    #bonusMinerals = (0,0,0)  # per template? or RW setup

                    planetHW = universe.createHomeworldPlanet(player.raceData)

                    # Need to add the HW colony manually. Cannot use 
                    # colonizePlanet as it does not have the flexibility 
                    # necessary to setup a HW
                    homeworld = Colony(player.raceData, planetHW, template.starting_population)
                    homeworld.scanner = True

                    productionQ = ProductionQ(homeworld, player)
                    homeworld.productionQ = productionQ

                    player.colonies[planetHW.ID] = homeworld

                playNumb += 1


        return tmpPlayers

        
    def generateGameVariables(self, template):

        #return dict of variables
        pass



    def ImportTurnFiles(self):
        """ ImportTurnFiles is used to import players .x files into the Game Object.


        """

        # for each player number, check xFileSubmissionForYear()
        # ###if True, then JSON object. else None
        
        # process new ship design
        
        # updatePlayerShipDesign()


        # sort/direct orders to the approprate place in game/player object.


        pass

  




# _______ Delete ____ covered by custom_setup.py
# def getSetupFileDict(setupFile):
#     '''
#     Access setupfile contained within folder, 
#     translate text to key value pairs
#     store into a dictionary and return

#     <game setup>
#     <victory conditions>
#     <player setup>    
#     <tech tree and modifications>
#     '''
#     #----TODO ---- 
#     # ADD obtain key:value pairs from setupfile

#     return {"setupFileName": setupFile}


#*********************************************************************


def cmdLineParseArgs():
    '''
    Uses argparse to capture commands from the command line

    TODO - 
        Race files fileNames' should be in the following format:
        <'game_name'.rn>. Where .rn = race number, like: rabid_weasels.r1; 
        rabid_weasels.r2; rabid_weasels.r3; etc.

    '''
    parser = argparse.ArgumentParser()

    # help
    # load game file    gameFile
    # new game          gameName
    
    # Load an existing game  
    parser.add_argument('-l', action='store', default=None, dest='gameFile', \
        help='Load .hst file for game. Specify game to load. Generates 1 Year. ')


    parser.add_argument('-T', action='store', default=1, dest='gameTurns', \
        help='''The number of years to generate after loading a game. 
        Default is 1. Is unnecessary if generating a single game turn''')

    
    # generate a new game from the standard template.
    # ---- how does this arg know the number of players and victory conditions? ---
    # may not be a viable command
    parser.add_argument('-n', action='store', default=None, dest='newGame', \
        help='''Enter name for new game. Name must be unique within the same 
        folder. Note: In order to generate a new game this argument is required.
        ''')

    # Generate a game from an existing game setup file. 
    parser.add_argument('-g', action='store', default=None, dest='customGame', \
        help=''' Generate a new game from a game setup file named: 
        <'game_name'.json>. Enter file name after the '-g'. Without this setting,
        the game will be generated from the StandardGameTemplate.
        
         Use '-c_setup' arg to create this setup file. 
        ''')
    
    # tech tree mod's could occur with a standard new game.  
    parser.add_argument('-t', action='store', default=None, dest='techTree', \
        help='''Use a custom tech tree to generate game. FileName should be <tech_tree.tech>.
        Enter tech filename after "-t". 
        If "OnlyUseCustomTechTree" : "True" key:value is set within the file 
        then the custom file will replace the standard tech tree.

        ''')


    parser.add_argument('-r', action='store', default=None, dest='newRace', \
        help='''Enter race name. Name must be unique within the same 
        folder. 
        ''')



    # generate a custom tech object file using command line or plain text editor
    parser.add_argument('-c_tech', action='store', default=None, dest='customTechTree', \
        help='''Tech tree variations can be loaded by using a seperate 
        <tech_tree.tech> file. 

        \nUsers have three options: 
        \n1)  Use the command line prompts to add customized tech to the tech file.
        
        \n2)  Indicate the number of new tech items that are desired. A template 
            will be generated in the correct format for the desired number of 
            items. The user can fill in the data from a plain text editor. 
        
        \n3) Existing Tech tree will be saved to file. 
             Set "OnlyUseCustomTechTree" : "True" in the file to replace standard 
             tech tree. 

        \nNo other arguments viable.

        ''')

            # \n4)  Existing tech can be modified by including the tech identifier 
            # and the dictionary key:value to replace. User must provide the exact
            # standard tech template - tech identifier and the correct dictionary 
            # value in order for a change to occur. Changes to standard tech will
            # affect the common tech tree for all players. 

    # generate a custom universe json object file using command line.
    parser.add_argument('-c_setup', action='store', default=None, dest='customSetup', help='''
    The custom setup dialog creates an interactive command line session allowing
    the game host to customize StandardGameTemplate values. The configuration 
    results are saved to an .json file that can be used to generate future games.
    
    \nNo other arguments viable.    

        ''')

    #add game setup flow that does not save the custom setup dialog

    # test cheange

    # add setup command ==> command line dialog using the standard template and turns into a setup file

    # add player arg
    # add victoryconditions (could also be in setupfile?)

    return parser.parse_args()



def CustomSetupFile(fileName):

    standardTemplate = StandardGameTemplate.standardUniverse(None) 
    customSetupDict = customSetupController(standardTemplate, fileName)

    # probably do not need to return the custom setup. 
    # Note: original intent was to have an option to save to file or create a new game. 
    # simplified version is now: create a file. Then use it to generate a game. 
    return customSetupDict

def CustomTechTreeFile(fileName):
    print("Custom Tech Tree module is still under development ")
    # tech expansion here
    treeFileName, techTree = customTechDialog(fileName)
    saveFileToJSON(techTree, treeFileName)


def CustomRaceFile():
    print("Custom RaceFile still under development")

def GenerateMFiles(game):
    '''
    input: game object
    output: sends one player's data
            Game year

            to createMFile()

    '''

    createMFile(game)


def SaveGameFile(game):
    fileName = game.game_name + '.hst'
    pickleTest = (game)
    GamePickle.makePickle(fileName, pickleTest)



def CreateNewGameTemplate(results):
    '''
    Method for creating a new game template. 

    Handles all new game command line arg logic and decision making.
    Assembles all pieces of a template into a StandardGameTemplate or Custom 
    version. 

    Output is gameTemplate - which comprises all template logic necessary to 
    generate game files. 

    '''
    """
    options:
    1) new game
    2) new game with customGame
    3) new game with customTechTree
    4) new game with customGame and customTechTree

    """

    gameName = results.newGame
    gameUniverseNumber = 1
    playerFileList = ['testPlayer1', 'testPlayer2', 'testPlayer3']
    techDict = {}

    if results.customGame:

        customSetupDict = loadFileFromJSON(results.customGame)
        
        if 'number_of_universes' in customSetupDict:
            gameUniverseNumber = customSetupDict['number_of_universes']

        if 'player_file_names' in customSetupDict:
            playerFileList = customSetupDict['player_file_names']

    if results.techTree:

        techDict = loadFileFromJSON(results.techTree)


    #***************************
    # Player file's parsing here
    # pull in player data from file : Key = "players_data"
    #***************************
    # Player data here
    print("Player Data under development")

    #*****************************
    # Victory conditions file/data here
    # pull in other data from file : Key = "victory_conditions_data"
    #*****************************
    # victory conditions here
    print("Victory Conditions under development")

    
    gameTemplate = StandardGameTemplate(gameName, playerFileList, customSetupDict, 
            gameUniverseNumber, techDict)

    #print("create new game %s" %results.standardGame)

    return gameTemplate








def main():

    """
    #user runs hosted game from command line (or gui host - not in this project)
    game looks in current folder:
        .hst file
        .rn = player n race
        .xn = file  # 1 off file sent to user
        .mn = file  # player's turn file submited to the host 
        .h = history file, contains previous turn info
        .xy = universe definitions
            - universe size
            - victory conditions
            - visible planets (for now all planets)
            - players (as player 1 - n; player names are typically hidden)
            >> this is the file that helps start the game. It provides the 
                starting stats for the player



    """


    #**********************************************
    # Command line args using argparser
    #
    #
    #*********************************************
    results = cmdLineParseArgs()


    #*****************************
    #   Assemble a custom Game Template
    #***************************** 
    if results.customSetup:

        gameTemplate = CustomSetupFile(results.customSetup)
        sys.exit()  



    #*****************************
    #   Create a custom Tech File
    #***************************** 
    elif results.customTechTree:

        CustomTechTreeFile(results.customTechTree)    
        sys.exit()


 
    #*****************************
    #   Create a custom race file
    #***************************** 
    elif results.newRace:

        CustomRaceFile()
        sys.exit()




    #*****************************
    #   Create a game
    #       all new games require '-n'
    #***************************** 
    elif results.newGame:

        #*****************************
        #   The Standard Game Template (or modified version) creates the game
        #*****************************
        gameTemplate = CreateNewGameTemplate(results) 
        game = Game(gameTemplate)  

        createXYFile(game)   # source -> game_utility.py


    #***************************** 
    #   Load <'game_name'.hst> file   &   do something
    #***************************** 
    elif results.gameFile:
 
        print("loading gamefile named %s" % results.gameFile)

        # ------- TODO ---------
        # test for .hst file matching results.gameFile in cwd 
        game = GamePickle.unPickle(results.gameFile)  # gameTemplate to be removed

        # ---TODO--- import each players .x file
        # --TODO-- process each players .x file data
        game.ImportTurnFiles()

        # all .x player data should be in place before OrderOfEvents.
        for year in range(0, int(results.gameTurns)):
            OrderOfEvents(game)
        # ---TODO--- intel and any other turn actions (in order of events?)

    else:
        print("\n\n\n\t***Stars Core Engine***\nPlease use '-h' to see the correct options.\n\n\n")
        sys.exit()


    #*****************************
    #   Save .hst files after turn is finished
    #***************************** 

    SaveGameFile(game)


 
    # fileName = game.game_name + '.hst'
    # pickleTest = (gameTemplate, game)
    # GamePickle.makePickle(fileName, pickleTest)





    #*****************************
    #   Save .m files for each player. 
    #***************************** 

    #createMFile(game)     #source -> game_utility.py 
    GenerateMFiles(game)    # sends player data that can generate a game turn












