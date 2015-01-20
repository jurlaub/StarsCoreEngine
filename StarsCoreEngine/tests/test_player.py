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
"""
Purpose:    To test the player object. 
            To test instantiated Ship Designs


"""



import os
import os.path

from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_not_in, assert_true, assert_false


from ..starscoreengine.game import Game
from ..starscoreengine.template import *
from ..starscoreengine.player import Player
from ..starscoreengine.player import RaceData as Race
from ..starscoreengine.player_designs import PlayerDesigns
from ..starscoreengine.tech import ShipDesign 






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







class TestPlayerDesign(object):
    """
    Tests for PlayerDesign



    """

    def setup(self):
        print("TestPlayerDesign: Setup")

        self.testShip1 = {'designName': 'doomShip1', 
                          'designID': 0,
                          'hullID': 'Scout',
                          'component': {"B": {"itemID": "Fuel Mizer", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Mole Scanner", "itemQuantity": 1}
                            } }

        self.testShip2 = {'designName': 'basic scout', 
                          'designID': 1,
                          'hullID': 'Scout',
                          'component': {"B": {"itemID": "Quick Jump 5", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Bat Scanner", "itemQuantity": 1}
                            } }


        self.testShip3 = {'designName': 'doomShip2', 
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
        self.testShip4 = {'designName': 'doomShip3', 
                          'designID': 3,
                          'hullID': "Privateer",
                          'component': {"A": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 2 },
                                        "B": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "D": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "E": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1},
                                                                    } }

        # need ship with 'restricted tech' so that producing it will be off

        



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

            assert_not_in(self.testShip1['designName'], designs.currentShips)


            designs.addDesign(self.testShip1, self.techTree)  


            assert_equal(len(designs.currentShips), shipCount + 1)
            assert_equal(len(designs.currentStarbases), starbaseCount)
            assert_in(self.testShip1["designName"], designs.currentShips) #assert ship now in design
            
            t1 = designs.currentShips[self.testShip1["designName"]]
            tmpHull = self.testShip1[hullID]       
            tmpScanner = 100  #Mole scanner normal range is 0
            assert_not_in("NAS", player.LRT)


            assert_equal(t1.normalScanRange, tmpScanner)
            assert_equal(t1.hullID, tmpHull)
            assert_equal(t1.designName, self.testShip1["designName"])

            assert_equal(t1.owner, player.raceName)         # different then the player key. 

        


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



class Test_ShipDesign(object):
    """
    May need to be moved to test_tech.py

    This tests that a given design has the correct information. That it is 
    correctly costed per the hull and assigned components.
    """

    def setup_class():
        """
        Generating 1 tech tree for all tests by making the techTree a class 
        level dictionary. (due to python namespace, the class tree will be found)

        """


        self = Test_ShipDesign

        print("Test_ShipDesign: Setup")


        self.playerFileList = ['Wolfbane', 'Bunnybane']
        self.testGameName = 'rabidTest'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.game = Game(self.gameTemplate)
        self.techTree = self.game.technology
        self.player = self.game.players['player1']



    def teardown_class():
        self = Test_ShipDesign
        

        print("Test_ShipDesign: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))



    def setup(self):
        print("Test_ShipDesign: Setup")

        # see 
        self.testShip1 = {'designName': 'doomShip1', 
                          'designID': 0,
                          'hullID': 'Scout',
                          'component': {"B": {"itemID": "Fuel Mizer", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Mole Scanner", "itemQuantity": 1}
                            } }

        self.testShip2 = {'designName': 'basic scout', 
                          'designID': 1,
                          'hullID': 'Scout',
                          'component': {"B": {"itemID": "Quick Jump 5", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Bat Scanner", "itemQuantity": 1}
                            } }


        self.testShip3 = {'designName': 'doomShip2', 
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
        self.testShip4 = {'designName': 'doomShip3', 
                          'designID': 3,
                          'hullID': "Privateer",
                          'component': {"A": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 2 },
                                        "B": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "D": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "E": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1},
                                                                    } }


    def teardown(self):
        print("Test_ShipDesign: Teardown")


    def test_testShip1(self):
        """
        scout + fuel mizer + fuel tank + Mole scanner

        hull    = (iron, bor, germ, resources, mass)
        scout   = (4,  2,  4, 10,  8)
        fMizer  = (8,  0,  0, 11,  6)
        fTank   = (6,  0,  0,  4,  3)
        mScan   = (2,  0,  2,  9,  2)
        total   = (20, 2,  8, 34, 19)


        fuelCapacity = (50 + 250)
        armorDP = 20
        scanning = 100


        """
        # assert_equal(len(self.player.design.currentShips), 0)
        # self.player.design.addDesign(self.testShip1, self.techTree)
        # assert_equal(len(self.player.design.currentShips), 1)

        ship = ShipDesign(self.testShip1, self.techTree) #self.testShip1['hullID'], self.testShip1, self.testShip1['designName']

        assert_equal(ship.iron, 20)
        assert_equal(ship.bor, 2)
        assert_equal(ship.germ, 8)
        assert_equal(ship.resources, 34)
        assert_equal(ship.mass, 19)

        assert_equal(ship.normalScanRange, 100)
        assert_equal(ship.armorDP, 20)
        assert_equal(ship.fuelCapacity, 300)
        assert_equal(ship.hasLRT, "IFE")

        assert_equal(ship.owner, None)      # owner is added when assigned to a players.design object
        assert_equal(ship.isDesignLocked, False)
        assert_equal(ship.designValidForProduction, False)

        assert_equal(ship.hullID, self.testShip1['hullID'])

        # tech values are different
        assert_equal(ship.energy, 0)         #should only show the max tech (not a sum)
        assert_equal(ship.weapons, 0)        #should only show the max tech (not a sum)
        assert_equal(ship.propulsion, 2)     #should only show the max tech (not a sum)
        assert_equal(ship.construction, 0)   #should only show the max tech (not a sum)
        assert_equal(ship.electronics, 4)    #should only show the max tech (not a sum)
        assert_equal(ship.biotechnology, 0)  #should only show the max tech (not a sum)


        # other values should not change
        assert_equal(ship.stealFromPlanets, False)
        assert_equal(ship.terraform, False)
        assert_equal(ship.warp10safe, False)

        assert_equal(ship.fuelGeneration, None)
        assert_equal(ship.cloaking, None)
        assert_equal(ship.cargoCapacity, None)











