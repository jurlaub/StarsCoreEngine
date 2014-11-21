"""
    This file is part of Stars Core Engine, which provides an interface and 
    processing of Stars data. 

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
import sys
import random
import pickle
import argparse
from .space_objects import SpaceObjects
from .universe import UniverseObject
from . import planet
from . import fleets
from .custom_setup import customSetupDialog
from .custom_setup import customSetupController
from .custom_setup import loadCustomSetupJSON
from .player import RaceData, Player






class Game(object):
    """
    Game will follow a 'singleton' concept. There can be Only One game of 
    any given name in the same folder

    Game() accepts game data from the StandardGameTemplate and turns it into
    a complete game with its cooresponding game obects.



    """

    def __init__(self, template):
        # singleton game name check?
        #create universe from gameDict
        # if standard == 1:

        #     print ("at Game, standard = %d dict=%s" % (standard, gameDict))
        # elif standard == "hello":
        #     print("standard was not 1")
        # else:
        #     print("hmm")

        ############
        ##### ! gameTemplate.universe_data hardcoded to a list, 
        #####  requires updating!          
        ############


        # -- A dictionary of Universe Objects
        self.game_universe = self.generateUniverses(template)

        # -- a dictionary of Player Objects
        self.players = {}



    


    def generateUniverses(self, template):
        '''
        Generates the number of universes specified in the template file. 
        >> template.universeNumber must be >= 1
        

        '''

        tmpUniverses = {}

        for i in range(0, int(template.universeNumber)):

            #newUni_name = template.universe_data[i]['UniverseName']
            universeSize = template.universe_data[i]['UniverseSizeXY']

            newUni = UniverseObject(i, universeSize)
           
            newUni.planets = self.createPlanetObjects(template.universe_data[i])   #dict

            tmpUniverses[i] = newUni




        return tmpUniverses


    def generatePlayers(self):
        pass

        
    def createPlanetObjects(self, u_template):
        """
        generates planet objects

        inputs: single universe dictionary data
        returns: dictionary of planet objects

        Eventually planet object generation within a universe should be shifted
        to the Universe class. 

        """
        planets = {}


        # ----- TODO ----
        # template should a single universe definition
        uSize = u_template["UniverseSizeXY"]
        uPlanet = int(u_template["UniversePlanets"])
        uNumber = u_template["UniverseNumber"]

        # create and add Planet objects with random locations, names and ID's
        for i in range(0, uPlanet):
            xy = (random.randrange(0, uSize[0]), random.randrange(0, uSize[1]))
            name = getPlanetNameFromTemplate(i)
            ID = str(uNumber) + str(i)
            newPlanet = planet.Planet(xy, ID, name)
            planets[ID] = newPlanet

        return planets 


    def randomPlanetLocations(self, uSize, uPlanet):
        pass


    def setPlanetLocation(self):
        pass




    def createXYFile(self):
        """
            contains:
            - Universe information object
            -
        """
        pass




# -- define the universe data in a standard values object, similar format, 
class StandardGameTemplate(object):
    """
    StandardGameTemplate is a class for generating a standard universe. 
    
    The standard universe data can be modified by passing in a dictionary 
    containing key:value pairs which will be used to update the standard values.

    Use the provided command line arguments to create a custom universe file as 
    well as modify/add technology. 

    """
    '''
    #u_name = ["Prime", "Alpha", "Beta", "Gamma", "Delta", "Omega", "Zeta"]

    planet_density = (.5, 1, 1.5) 
    planets = 10
    standard_universe_size_small = {"UniverseSizeXY":(200,200)}
    standard_universe_size_medium = {"UniverseSizeXY":(600,600)}
    standard_universe_size_large = {"UniverseSizeXY":(1000,1000)}

    standard_universe = {"UniverseNumber":1, "UniverseSizeXY": (200,200), \
    "UniverseName":("Prime"), "UniversePlanets":planets, \
    "PlanetDensity": planet_density[1], "Players":(1)}
    '''

    # instantiate the standard object
    #                           customUniverse = {}, customTech = {}, customVC = {}
    def __init__(self, game_name = None, playerFileList = [], setupDict = {}, universeNumber = 1):
        # instantiates a new game dictionary while merging setup data
        
        # self.game_name = game_name # "rabid_weasels"
        if not game_name:
            self.game_name = "rabid_weasels"
        else:
             self.game_name = game_name # "rabid_weasels"

        self.planet_names = planetNameTemplate()
        self.universeNumber = int(universeNumber)
        self.universe_data = []    # list of universe dictionary data

        #self.technology_data       #template would have technology
        #self.victory_conditions    # standard VC template with changes        


        # ---- HARDCODED =>> requires updating custom setup
        self.players_data = self.getPlayerRaceFile(playerFileList)    # list of player race file names 
        


        if universeNumber < 1:
            sys.exit("universeNumber must be greater then 1")
        else:

            for i in range(0, int(universeNumber)):
                x = self.standardUniverse()
                x['UniverseNumber'] = i

                #merge setupDict (the customized dictionary) with standard
                if setupDict:
                    tmp_universe = 'UniverseNumber' + str(i)
                    customUniverseObject = setupDict[tmp_universe]

                    x = self.mergeDictionaryData(x, customUniverseObject)

                self.universe_data.append(x)          # NOTE: appending to a list
                






    def standardUniverse(self):
        # standard universe comprises standard settings for 1 universe.

        standard_universe = {"UniverseNumber":0, "UniverseSizeXY": (200,200), \
        "UniverseName": "Prime", "UniversePlanets":6, "Players":(1)}
        
        return standard_universe



    def mergeDictionaryData(self, dict1, dict2):
        '''
        input: dict1, dict2
        output: dict1

        if items in dict2 are in dict1, merge those items into dict1
        '''

        for n in dict2:
            if n in dict1:
                dict1[n] = dict2[n]

        return dict1

    def getPlayerRaceFile(self, fileList):
        # 'race name'.r1
        # look for all r1 files in folder
        # should match number of players
        raceObjects = []

        for each in fileList:

            #--- TODO  change from grabbing a dev race to grabbing a .r1 file
            # and turning it into a RaceData() object
            raceObjects.append(self.getDevRaceFile())

        return raceObjects

    def getDevRaceFile(self):
        # returns a development file that will substitute as a player race file

        return RaceData()


def getPlanetNameFromTemplate( n):
        planet_names = planetNameTemplate()
        x = int(n % len(planet_names))
        return planet_names[x]

def planetNameTemplate():
        planet_names = ["Alan", "Fenge", "Fenris", "Shill", "239_Alf", "Wolf359",\
         "Dark Star", "Kirk", "Flo Rida", "Pluto", "Centari", "Mau Tai", "Zeta"]
        return planet_names

      



class GamePickle(object):

    def makePickle(fileName, p_object):
        with open(fileName, "bw") as a_file:    # file closed by the with statement
            pickle.dump(p_object, a_file)


    def unPickle(fileName):
        '''
        unpickle 

        requires a fileName,
            - test if the name uses the game name or fileName (i.e. <name>.hst)
            - add .hst and other values to unpack relevant values

        returns a number of objects:
            gameTemplate = StandardGameTemplate
            game = data after Game
        '''
        with open(fileName, "rb") as fn:
            #(gameTemplate, game) = pickle.load(fn)
            #p_object = pickle.load(fn)
            #return p_object
            return pickle.load(fn)


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
        help='Load .hst file for game. Specify game to load. \nNo other arguments viable. ')


    
    # generate a new game from the standard template.
    # ---- how does this arg know the number of players and victory conditions? ---
    # may not be a viable command
    parser.add_argument('-n', action='store', default=None, dest='newGame', \
        help='''Enter name for new game. Name must be unique within the same 
        folder. 
        ''')

    # Generate a game from an existing game setup file. 
    parser.add_argument('-g', action='store', default=None, dest='customGame', \
        help=''' Generate a new game from a game setup file named: 
        <'game_name'.json>. Enter file name after the '-g'. Without this setting,
        the game will be generated from the StandardGameTemplate.
        
         Use '-s' arg to create this setup file. 
        ''')
    
    # tech tree mod's could occur with a standard new game.  
    parser.add_argument('-t', action='store', default=None, dest='techTree', \
        help='''Use a custom tech tree to generate game. FileName should be <tech_tree.tech>.
        Enter tech filename after "-t". ''')





    # generate a custom tech object file using command line or plain text editor
    parser.add_argument('-c_tech', action='store', default=None, dest='customTechTree', \
        help='''Tech tree variations can be loaded by using a seperate 
        <tech_tree.tech> file. 

        \nUsers have three options: 
        \n1)  Use the command line prompts to add customized tech to the tech file.
        
        \n2)  Indicate the number of new tech items that are desired. A template 
            will be generated in the correct format for the desired number of 
            items. The user can fill in the data from a plain text editor. 
        
        \n3)  Existing tech can be modified by including the tech identifier 
            and the dictionary key:value to replace. User must provide the exact
            standard tech template - tech identifier and the correct dictionary 
            value in order for a change to occur. Changes to standard tech will
            affect the common tech tree for all players. 
       
        \nNo other arguments viable.

        ''')

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


def SetupFileInterface(results):
    '''
    Interface layer between command line args and Game(). 

    Handles all command line arg logic and decision making

    Output is gameTemplate - which comprises all template logic necessary to 
    generate game files. 

    '''


    

    # Tech tree - generate a custom techTree file and then quit
    if results.customTechTree:
        print("Custom Tech Tree module is still under development ")
        
        # tech expansion here
         
        sys.exit()


    # Custom Uni - generate custom universe file and quit 
    elif results.customSetup:

        standardTemplate = StandardGameTemplate.standardUniverse(None) 
        customSetupDict = customSetupController(standardTemplate, results.customSetup)
        
        sys.exit()  # 


    # ('-n' + '-g') + '-t' options handled here
    if results.newGame and results.customGame:
        #"Generates a new game using a custom dictionary."
        customSetupDict = loadCustomSetupJSON(results.customGame)
        
        gameName = results.newGame
        gameUniverseNumber = customSetupDict['number_of_universes']
        #gamePlayerNumber = customSetupDict['number_of_players']
        playerFileList = customSetupDict['player_file_names']

        gameTemplate = StandardGameTemplate(gameName, playerFileList, customSetupDict, 
            gameUniverseNumber)

    elif results.newGame:
        #*****************************
        #   The Standard Game Template can be modifed to create game variations
        #*****************************
        gameTemplate = StandardGameTemplate(results.newGame)

    # elif results.customGame:
    #     #*****************************
    #     #   Universe Setup File Parsing 
    #     #       pass to the Standard Game Template
    #     #*****************************
    #     customSetupDict = loadCustomSetupJSON(results.customGame)

    #     gameTemplate = StandardGameTemplate

    #     pass
    else: 
        print("Unexpected command line option. Please review options and try again.")
        sys.exit()


    #**************************
    # Tech data parsing here
    # ****** in same setup file? ********d
    # pull in Game tech tree data : Key = "tech_data"
    #### contains the standard tech (includes race specific tech) 
    #### will contain additional general tech 
    #### ultimately contains specific player tech (not associated with race wizard) : Key = "player_n_tech" 
    #**************************
    # tech file data here
    print("Tech Tree import under development: tech file name %s" % results.techTree)




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

        create an .xy file that will house .xy data



    """


    #**********************************************
    # Command line args using argparser
    #
    #
    #*********************************************
    results = cmdLineParseArgs()


    #   Load <'game_name'.hst> file
    if results.gameFile:
 
        print("loading gamefile named %s" % results.gameFile)

        # ------- TODO ---------
        # test for .hst file matching results.gameFile in cwd 
        gameTemplate, game = GamePickle.unPickle(results.gameFile)

    else:
   
        gameTemplate = SetupFileInterface(results)

        #*****************************
        #   The Standard Game Template (or modified version) creates the game
        #*****************************
        game = Game(gameTemplate)  



    #Test when game needs to be saved as a .hst file.
    # saject = input("Do you wish to save this object? (y/n)")

    # if saject == 'y':
    #     #pickle called here
 
    #     fileName = gameTemplate.game_name + '.hst'
    #     pickleTest = (gameTemplate, game)
    #     GamePickle.makePickle(fileName, pickleTest)




    ##**********************************************
    #  For command line review:
    #        print out of planet information
    #
    ##**********************************************
    print("%s" % gameTemplate.game_name)
    for zz in iter(game.game_universe):
        print("\t%s%s%d%s"%('-'*20, 'UniverseNumber:', zz,'-'*20 ))

        for x in iter(game.game_universe[zz].planets):
            
            nn = game.game_universe[zz].planets[x]

            temp, grav, rad = nn.origHab
            ironC, borC, germC = nn.origConc 
            print("ID:%s, %s:  %s  - Owner:%s" % (nn.ID, nn.name, nn.xy, nn.owner))
            print("\tEnvironment: \t\t(%sc, %sg, %smr) " % (temp, grav, rad))
            print("\tMineral Concentration: \t(i:%skt, b:%skt, g:%skt)" % (ironC, borC, germC))



# if __name__ == "__main__":
#     main()
