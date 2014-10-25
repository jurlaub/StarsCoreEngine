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
from .space_objects import SpaceObjects
from . import planet
from . import fleets






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
    Modification includes merging a 'setup' dictionary with the standard universe
    data.


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
    def __init__(self, setupDict = {}, universeNumber = 1, playerNumber = 1):
        # instantiates a new game dictionary while merging setup data
        
        self.game_name = "rabid_weasels"
        self.planet_names = self.planetNameTemplate()
        self.universe_data = []    # list of universe dictionary data
        #self.players_data = []     # list of player dictionary data
        #self.technology_data
        #self.victory_conditions

        #print(StandardGameTemplate.standard_universe)
        if universeNumber < 1:
            sys.exit("universeNumber must be greater then 1")
        else:

            for i in range(0, universeNumber):
                x = self.standardUniverse()
                x['UniverseNumber'] = i
                # if i%2 == 0:
                #     x["UniverseSizeXY"] = (1100,13400)
                self.universe_data.append(x)
                

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
        "UniverseName":("Prime"), "UniversePlanets":50, \
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
    

    def getUniverseSize(self):
        return tuple(x["UniverseSizeXY"] for x in self.universe_data)


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
        with open(fileName, "rb") as fn:
            #(gameTemplate, game) = pickle.load(fn)
            #p_object = pickle.load(fn)
            #return p_object
            return pickle.load(fn)








def main():

    """
    #user runs hosted game from command line (or gui host - not in this project)
    game looks in current folder:
        .hst file
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
    
    #game dictionary?

    #*****************************
    # Command line args here
    #*****************************
    # ### if a setup file is specified then pull setup file data 
    # ### collect in dictionary

    #*****************************
    #   Goes in a setup file parser class
    #*****************************
    # Universe Setup File Parsing Here
    # pull in universe_data from file : Key = "universe_data"

    # Player file's parsing here
    # pull in player data from file : Key = "players_data"

    # Tech data parsing here
    # pull in Game tech tree data : Key = "tech_data"
    #### contains the standard tech (includes race specific tech) 
    #### will contain additional general tech 
    #### ultimately contains specific player tech (not associated with race wizard) : Key = "player_n_tech" 

    # Victory conditions file/data here
    # pull in other data from file : Key = "victory_conditions_data"
    #*****************************

    #*****************************
    #  Go to standard game setup
    #*****************************
  

    # PreGameSetup()? # from setup file include setup file dictionary with GameSetup call

    gameTemplate = StandardGameTemplate()
    

    game = GameSetup(gameTemplate)  

    print("game.planets is a dictionary %s" % isinstance(game.planets, dict))
    for x in iter(game.planets):
        p = game.planets
        print("ID:%s, %s @%s" % (p[x].ID, p[x].name, p[x].xy))




    #pickle called here
    fileName = gameTemplate.game_name + '.hst'
    pickleTest = (gameTemplate, game)
    # with open(fileName, "bw") as a_file:    # file closed by the with statement
    #     pickle.dump(pickleTest, a_file)
    GamePickle.makePickle(fileName, pickleTest)





    print("\n\n after pickle \n ")
    for x in iter(game.planets):
        p = game.planets
        print("ID:%s, %s @%s" % (p[x].ID, p[x].name, p[x].xy))

    gameTemplate = None
    game = None
    #print("gameTemplate is None:%s  & game is None:%s " % (isinstance(gameTemplate, None), isinstance(game, None)))
    print("gameTemplate is None:%s  & game is None:%s " % (gameTemplate, game))
    

    #unpickle here
    # with open(fileName, "rb") as fn:
    #     (gameTemplate, game) = pickle.load(fn)
    gameTemplate, game = GamePickle.unPickle(fileName)


    print("\n\n after Unpickle \n ")
    for x in iter(game.planets):
        p = game.planets
        print("ID:%s, %s @%s" % (p[x].ID, p[x].name, p[x].xy))

    print("%s" % gameTemplate.game_name)
    print("%s" % gameTemplate.universe_data[0])

# if __name__ == "__main__":
#     main()
