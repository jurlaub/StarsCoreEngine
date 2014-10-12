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
from .space_objects import SpaceObjects
from . import planet
from . import fleets






class GameSetup(object):
    """
    GameSetup will follow a 'singleton' concept. There can be Only One game of 
    any given name in the same folder

    """

    def __init__(self, gameDict):
        # singleton game name check?
        #create universe from gameDict
        # if standard == 1:

        #     print ("at GameSetup, standard = %d dict=%s" % (standard, gameDict))
        # elif standard == "hello":
        #     print("standard was not 1")
        # else:
        #     print("hmm")
        pass


        

    def getUniverseSize(self):
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

    planet_density = (.5, 1, 1.5) 
    planets = 10
    standard_universe_size_small = {"UniverseSizeXY":(200,200)}
    standard_universe_size_medium = {"UniverseSizeXY":(600,600)}
    standard_universe_size_large = {"UniverseSizeXY":(1000,1000)}

    standard_universe = {"UniverseNumber":1, "UniverseSizeXY": (200,200), \
    "UniverseName":("Prime"), "UniversePlanets":(planets), \
    "PlanetDensity": planet_density[1], "Players":(1), "VictoryConditions":(None)}

    # instantiate the standard object
    def __init__(self, setupDict = {}):
        # instantiates a new game dictionary while merging setup data
        
        #setting up dictionary to return
        self.universe_data = {}
        #self.players_data = {}
        # technology
        # victory conditions

        # takes standard list and merges with setup dictionary.
        if setupDict:
            #merge variation with standard
            print ("StandardGameTemplate:init - setupDict is not empty")

        #print(StandardGameTemplate.standard_universe)
        self.universe_data = StandardGameTemplate.standard_universe


        



def PreGameSetup(gameDict, setupDict):
    """
    Merges Game Dictionary and Setup File data into one dictionary
    """


    pass












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
    # >>> send in setup derived dictionary

    #game = {"universe_data":{}, "players_data":{}, "victory_conditions_data":{}}
    #game = {}

    # PreGameSetup()? # from setup file include setup file dictionary with GameSetup call
    #game = PreGameSetup(game, {})
    game = StandardGameTemplate()
    print(game.universe_data)

    #GameSetup(game)  

    print("yadda")




# if __name__ == "__main__":
#     main()
