"""
    This file is part of Stars Core Engine, which provides an interface and processing of Stars data.
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

    Contributors to this project agree to abide by the interpretation expressed in the 
    COPYING.Interpretation document.

"""
from .space_objects import *
import planet
import fleets



def main():
	print (" test !")

	t1 = space_objects.SpaceObjects(5,7,4433)
	print ("id=%", t1.getCurrentCoord())

    """
    # user runs hosted game from command line (or gui host - not in this project)
        game looks in current folder:
            .hst file
            .xn = file  # 1 off file sent to user
            .mn = file  # turn file submited to the host with a player's game turn details
            .h = history file, contains previous turn info, including scanner and graph data
            .xy = universe definitions
                - universe size
                - victory conditions
                - visible planets (for now all planets)
                - players (as player 1 - n; player names are typically hidden)
                >> this is the file that helps start the game. It provides the starting stats for the player

        create an .xy file that will house .xy data



    """

    #JSON_Universe = {"UniverseNumber": 1, }
    planets = 10
    standard_universe = {"UniverseNumber":1, "UniverseSizeXY": (200,200), "UniverseName":("Prime"), "UniversePlanets":(planets), "Players":(1), "VictoryConditions":(None) }



class GameSetup(object):

    def __init__(self):
        #create universe


    def createXYFile(self):
        """
            contains:
            - Universe information object
            -
        """










if __name__ == "__main__":
	main()