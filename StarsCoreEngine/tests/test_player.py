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

import os
import os.path

from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_true, assert_false


from ..starscoreengine.game import Game
from ..starscoreengine.template import *
from ..starscoreengine.player import Player
from ..starscoreengine.player import RaceData as Race
from ..starscoreengine.player_designs import PlayerDesigns
from ..starscoreengine.tech import ShipDesign as SuperShipDesign



class TestPlayerObject(object):
    """ 
    Unit Tests for player Object

    """

    def setup(self):
        print("TestPlayerObject: Setup")
        self.raceName = 'Wolfbane'
        self.RaceData = Race(self.raceName)
        self.player = Player(self.RaceData, {})


    def teardown(self):
        print("TestPlayerObject: Teardown")

    def test_PlayerValues(self):
        player = self.player
        race = self.RaceData

        assert(self.raceName == player.raceName)


class ShipDesign(SuperShipDesign):

    def __init__(self):
        super(ShipDesign, self).__init__()

    def isShipDesignValid(self, techTree = {}):

        if techTree: return False

        return True




class TestPlayerDesign(object):
    """
    Tests for PlayerDesign



    """

    def setup(self):
        print("TestPlayerDesign: Setup")

        self.testShip1 = {'designName': 'doomShip1', 
                          'designID': 1,
                          'hullID': 'Scout',
                          'component': {"B": {"itemID": "Fuel Mizer", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Bat Scanner", "itemQuantity": 1}
                            } }
        self.testShip2 = {'designName': 'doomShip2', 
                          'designID': 2,
                          'hullID': 'Destroyer',
                          'component': {"G": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1 },
                                        "E": {"itemID": "Energy Capacitor", "itemQuantity": 1},
                                        "D": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 1},
                                        "F": {"itemID": "Crobmnium", "itemQuantity": 1},
                                        "C": {"itemID": "X-Ray Laser", "itemQuantity": 1},
                                        "B": {"itemID": "X-Ray Laser", "itemQuantity": 1},
                                        "A": {"itemID": "Manoeuvring Jet", "itemQuantity": 1}
                                                                    } }
        self.testShip3 = {'designName': 'doomShip3', 
                          'designID': 3,
                          'hullID': "Privateer",
                          'component': {"A": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 2 },
                                        "B": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "D": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "E": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1},
                                                                    } }

        #self.raceName = 'Wolfbane'
        #self.RaceData = Race(self.raceName)
        #self.player = Player(self.RaceData)
        self.playerFileList = ['Wolfbane', 'Bunnybane']
        self.testGameName = 'rabidTest'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.game = Game(self.gameTemplate)
        self.player1 = self.game.players['player1']

        self.techTree = self.game.technology


    def teardown(self):
        print("TestPlayerDesign: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))


    def test_AddDesign(self):
        """PlayerDesigns.AddDesign unit tests

        # check newDesign.hull for starbase or ship type
        # check that capacity has not been reached
        # check that name is not a duplicate

        # Instantiate ShipDesign
        # update values
        
        # add to appropriate currentDict

        """
        # design is added to correct dictionary (ship/starbase)
        #if we are at capacity, what should be done?

        #Ship Design added

        # values are correct

        for player in self.game.players.values():
            designs = player.designs

            shipCount = len(designs.currentShips)
            starbaseCount = len(designs.currentStarbases)


            #see PlayerDesigns.AddDesign for design name
            assert_not_in(self.testShip1['designName'], designs.currentShips)

            # add design

            #assert count for ship went up
            # assert count for starbase is same

            #assert ship now in design
            #assert ship component or two are in ShipDesign object



        


    def test_AddDesign_OverCapacity(self):
        """PlayerDesigns.AddDesign unit tests

        # check newDesign.hull for starbase or ship type
        # check that capacity has not been reached
        # check that name is not a duplicate

        # Instantiate ShipDesign
        # update values
        
        # add to appropriate currentDict

        """
        
        pass

    def test_AddDesign_DuplicateEntries(self):
        """PlayerDesigns.AddDesign unit tests

        # check newDesign.hull for starbase or ship type
        # check that capacity has not been reached
        # check that name is not a duplicate

        # Instantiate ShipDesign
        # update values
        
        # add to appropriate currentDict

        """
        
        pass


    def test_RemoveDesign(self):
        pass

    def test_TransferDesign(self):
        pass

    def test_ValidDesignForProduction(self):
        pass



