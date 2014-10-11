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
from space_objects import SpaceObjects
import planet
import fleets






class GameSetup(object):
    """
    GameSetup will follow a 'singleton' concept. There can be Only One game of 
    any given name in the same folder



    """

    def __init__(self, gameDict, standard = 1):
        #create universe from StandardGame
        if standard == 1:

            print ("at GameSetup, standard = %d dict=%s" % (standard, gameDict))
        elif standard == "hello":
            print("standard was not 1")
        else:
            print("hmm")



        

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
class StandardGameObjects(object):

    planet_density = (.5, 1, 1.5) 
    planets = 10
    standard_universe_size_small = {"UniverseSizeXY":(200,200)}
    standard_universe_size_medium = {"UniverseSizeXY":(600,600)}
    standard_universe_size_large = {"UniverseSizeXY":(1000,1000)}

    standard_universe = {"UniverseNumber":1, "UniverseSizeXY": (200,200), \
    "UniverseName":("Prime"), "UniversePlanets":(planets), \
    "PlanetDensity": planet_regular, "Players":(1), "VictoryConditions":(None)}


    # instantiate the standard object














if __name__ == "__main__":

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
    game = {"universe_data":{}, "players_data":{}, "victory_conditions_data":{}}

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



    GameSetup(game)

    print("yadda")



