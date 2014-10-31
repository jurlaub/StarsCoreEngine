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
from . import planet
from . import fleets
from .custom_setup import customSetupDialog






class GameSetup(object):
    """
    GameSetup will follow a 'singleton' concept. There can be Only One game of 
    any given name in the same folder

    GameSetup() accepts game data from the StandardGameTemplate and turns it into
    a complete game with its cooresponding game obects.

    """

    def __init__(self, template):
        # singleton game name check?
        #create universe from gameDict
        # if standard == 1:

        #     print ("at GameSetup, standard = %d dict=%s" % (standard, gameDict))
        # elif standard == "hello":
        #     print("standard was not 1")
        # else:
        #     print("hmm")

        ############
        ##### ! gameTemplate.universe_data hardcoded to a list, 
        #####  requires updating!          
        ############
        self.planets = self.createPlanetObjects(template)   #dict



        
    def createPlanetObjects(self, template):
        """
        generates planet objects

        inputs: single universe dictionary data
        returns: dictionary of planet objects

        """
        planets = {}

        uSize = template.universe_data[0]["UniverseSizeXY"]
        uPlanet = template.universe_data[0]["UniversePlanets"] 
        uNumber = template.universe_data[0]["UniverseNumber"]

        # create and add Planet objects with random locations, names and ID's
        for i in range(0, uPlanet):
            xy = (random.randrange(0, uSize[0]), random.randrange(0, uSize[1]))
            name = template.getPlanetNameFromTemplate(i)
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
    The class provides tools to modify the standard data. 

    To modify standard template, pass in dictionary containing key:value pairs 
    which will be used to update the standard dictionary.

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
    def __init__(self, game_name = None, setupDict = {}, universeNumber = 1, playerNumber = 1):
        # instantiates a new game dictionary while merging setup data
        
        self.game_name = game_name # "rabid_weasels"
        if not game_name:
            self.game_name = "rabid_weasels"
        else:
             self.game_name = game_name # "rabid_weasels"

        self.planet_names = self.planetNameTemplate()
        self.universe_data = []    # list of universe dictionary data
        #self.players_data = []     # list of player dictionary data
        #self.technology_data
        #self.victory_conditions

        if universeNumber < 1:
            sys.exit("universeNumber must be greater then 1")
        else:

            for i in range(0, universeNumber):
                x = self.standardUniverse()
                x['UniverseNumber'] = i
                # if i%2 == 0:
                #     x["UniverseSizeXY"] = (1100,13400)
                self.universe_data.append(x)          # NOTE: appending to a list
                

                #self.universe_data = self.standardUniverse()  #StandardGameTemplate.standard_universe

        # takes standard list and merges with setup dictionary.
        if setupDict:
            #merge variation with standard
            print ("StandardGameTemplate:init - setupDict is not empty")





    def standardUniverse(self):
        # standard universe comprises standard settings for 1 universe.
        #planets = 10
        #planet_density = (.5, 1, 1.5)
        standard_universe = {"UniverseNumber":0, "UniverseSizeXY": (200,200), \
        "UniverseName":("Prime"), "UniversePlanets":6, \
        "PlanetDensity": 1, "Players":(1)}
        
        return standard_universe


    '''
    def multiUniverse(self, n_universe = 2):
        """
        MultiUniverse dictionary data used to modify the standard universe 
        dictionary.
        """

        multi_universe = {"UniverseNumber":n_universe, \
        "UniverseSizeXY": (200,200)}


        #self.universe_data = self.mergeDictionaryData(self.universe_data, multi_universe)

        return self.universe_data
    '''


    def mergeDictionaryData(self, dict1, dict2):

        for n in dict2:
            dict1[n] = dict2[n]

        return dict1
    

    # def getUniverseSize(self):
    #     return tuple(x["UniverseSizeXY"] for x in self.universe_data)


    def getPlanetNameFromTemplate(self, n):
        planet_names = self.planetNameTemplate()
        x = int(n % len(planet_names))
        return planet_names[x]

    def planetNameTemplate(self):
        planet_names = ["Alan", "Fenge", "Fenris", "Shill", "239_Alf", "Wolf359",\
         "Dark Star", "Kirk", "Flo Rida", "Pluto", "Centari", "Mau Tai", "Zeta"]
        return planet_names

      

def PreGameSetup(gameDict, setupDict):
    """
    Merges Game Dictionary and Setup File data into one dictionary
    """


    pass




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
            game = data after GameSetup
        '''
        with open(fileName, "rb") as fn:
            #(gameTemplate, game) = pickle.load(fn)
            #p_object = pickle.load(fn)
            #return p_object
            return pickle.load(fn)



def getSetupFileDict(setupFile):
    '''
    Access setupfile contained within folder, 
    translate text to key value pairs
    store into a dictionary and return

    <game setup>
    <victory conditions>
    <player setup>    
    <tech tree and modifications>
    '''
    #----TODO ---- 
    # ADD obtain key:value pairs from setupfile

    return {"setupFileName": setupFile}





def cmdLineParseArgs():
    '''
    Uses argparse to capture commands from the command line

    '''
    parser = argparse.ArgumentParser()

    # help
    # load game file    gameFile
    # new game          gameName
    # generate a game using a setup file  
    parser.add_argument('-l', action='store', default=None, dest='gameFile', help='load .hst file for game')
    parser.add_argument('-n', action='store', default=None, dest='newGame', \
        help='enter name for new game. Name must be unique within the same folder')
    parser.add_argument('-g', action='store', default=None, dest='generate', \
        help='''Use a <game_name.setup> containing key:value pairs to modify the
        Standard Game Template. Each pair should be on a new line.''')
    parser.add_argument('-tech', action='store', default=None, dest='techTree', \
        help='''tech tree variations can be loaded by using a seperate 
        <tech_tree.tech> file. 
        New tech elements are added by including a complete description in a
        multi-level dictionary. All necessary values must be included

        Existing tech can be modified by including the tech identifier (or name?)
        and the dictionary key:value to replace

        ''')
    parser.add_argument('-s', action='store', default=None, dest='customSetup', help='''
    The custom setup dialog creates an interactive command line session allowing
    the game host to customize StandardGameTemplate values. The configuration 
    results are saved to an .ini file that can be used to generate future games.
        ''')

    # add setup command ==> command line dialog using the standard template and turns into a setup file

    # add player arg
    # add victoryconditions (could also be in setupfile?)

    return parser.parse_args()


def SetupFileHelper(results):
    #*****************************
    #   Universe Setup File Parsing 
    #       pass to the Standard Game Template
    #*****************************
    setupFileDict = getSetupFileDict(results.generate)

    #***************************
    # Player file's parsing here
    # pull in player data from file : Key = "players_data"
    #***************************
    # Player data here


    #*****************************
    # Victory conditions file/data here
    # pull in other data from file : Key = "victory_conditions_data"
    #*****************************
    # victory conditions here

    #**************************
    # Tech data parsing here
    # ****** in same setup file? ********d
    # pull in Game tech tree data : Key = "tech_data"
    #### contains the standard tech (includes race specific tech) 
    #### will contain additional general tech 
    #### ultimately contains specific player tech (not associated with race wizard) : Key = "player_n_tech" 
    #**************************
    # tech file data here
    print("tech file name %s" % results.techTree)


    #*****************************
    #   The Standard Game Template can be modifed to create game variations
    #*****************************
    gameTemplate = StandardGameTemplate(results.newGame, setupFileDict)
    

    #*****************************
    #   The Standard Game Template (or modified version) creates the game
    #*****************************
    game = GameSetup(gameTemplate)  



    print("load from command line: %s" % results.gameFile)
    print("%s"%setupFileDict)
    print("create new game %s" %results.newGame)

    return gameTemplate, game




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


    #*****************************
    # Command line args using argparser
    #
    #
    #****************************
    results = cmdLineParseArgs()

    if results.gameFile:
        """
        Loading a .hst file should result in (gameTemplate, game)

        more may be added (techTree, players, victoryConditions)

        """
        print("loading gamefile named %s" % results.gameFile)
        #unpickle here

        # ------- TODO ---------
        # test for .hst file matching results.gameFile in cwd 
        gameTemplate, game = GamePickle.unPickle(results.gameFile)

    elif results.customSetup:
        # just want the values from the standardUniverse. This however feels odd.
        standardTemplate = StandardGameTemplate.standardUniverse(None) 
        customSetupDict = customSetupDialog(standardTemplate)
        sys.exit()  # 

    else:

        gameTemplate, game = SetupFileHelper(results)
        
        #pickle called here
        '''

        '''
        fileName = gameTemplate.game_name + '.hst'
        pickleTest = (gameTemplate, game)
        GamePickle.makePickle(fileName, pickleTest)




    #####
    #  For command line review:
    #        print out of planet information
    #
    #####
    print("%s" % gameTemplate.game_name)
    for x in iter(game.planets):
        p = game.planets
        temp, grav, rad = p[x].origHab
        ironC, borC, germC = p[x].origConc 
        print("ID:%s, %s:  %s  - Owner:%s" % (p[x].ID, p[x].name, p[x].xy, p[x].owner))
        print("\tEnvironment: \t\t(%sc, %sg, %smr) " % (temp, grav, rad))
        print("\tMineral Concentration: \t(i:%skt, b:%skt, g:%skt)" % (ironC, borC, germC))



# if __name__ == "__main__":
#     main()
