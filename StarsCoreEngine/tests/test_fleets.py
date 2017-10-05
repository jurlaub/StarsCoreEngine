"""
    This file is part of Stars Core Engine, which provides an interface and processing of Game data.
    Copyright (C) 2017  <Joshua Urlaub + Contributors>

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
 assert_raises, raises, assert_in, assert_not_in, assert_true, assert_false

from ..starscoreengine.game import Game
from ..starscoreengine.template import *
from ..starscoreengine.player import Player
# from ..starscoreengine.player_designs import PlayerDesigns
# from ..starscoreengine.ship_design import ShipDesign 
from ..starscoreengine.productionQ import *
from ..starscoreengine.game_xfile import processDesign, processProductionQ
from ..starscoreengine.planet import Colony, Planet
from ..starscoreengine.fleets import FleetObject, Token
from ..starscoreengine.fleet_command import FleetCommand

from ..starscoreengine.universe import UniverseObject
from ..starscoreengine.template_race import startingDesigns, startingShipDesignsCount, startingDesignsCount #colonyShip, scoutShip, destroyerShip, smallFrieghterShip


from .helper import findPlayerHW, PlayerTestObject


class TestFleets(object):
    """
    Test structure for Fleets, FleetOrders, FleetCommand classes

    """

    def setup_class():
        """
        Generating 1 tech tree for all tests by making the techTree a class 
        level dictionary. (due to python namespace, the class tree will be found)

        """


        self = TestFleets

        print("TestFleets: Setup")


        self.playerFileList = ['Wolfbane', 'Bunnybane', 'Sharkbane']
        self.testGameName = 'rabidTest'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "3"}})
        self.game = Game(self.gameTemplate)

        #self.techTree = self.game.technology
        self.player0 = self.game.players['player0']
        self.player1 = self.game.players['player1']
        self.player2 = self.game.players['player2']

        #self.techLevels = self.player1.research.techLevels
        

        #--------- obtain colony worlds -------------
        
        self.universePlanets = self.game.game_universe[0].planets
        self.universe = self.game.game_universe[0]


        #--------- obtain HW -------------
        self.p0_colonyHW_name, self.p0_colonyHW_obj = findPlayerHW(self.player0.colonies)        
        self.p1_colonyHW_name, self.p1_colonyHW_obj = findPlayerHW(self.player1.colonies)
        self.p2_colonyHW_name, self.p2_colonyHW_obj = findPlayerHW(self.player2.colonies)



        #--------- end ------------------







    def teardown_class():
        self = TestFleets
        

        print("TestFleets: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))



    def setup(self):
        print("TestFleets: Setup")

        # ------- Generate Players Starting Ships ----------
        #self.game.generatePlayersStartingShips()

        # self.p1_colonyHW_obj.planet.factories = 10
        # self.p1_colonyHW_obj.planet.surfaceIron = 200
        # self.p1_colonyHW_obj.planet.surfaceBor = 200
        # self.p1_colonyHW_obj.planet.surfaceGerm = 200
        # self.p1_colonyHW_obj.population = 450000




        # print("setup: On HW pop:%d iron: %d bor: %d germ: %s" % (self.populationOnHW, self.ironOnHW, self.borOnHW, self.germOnHW))

        # ----- ship design -----
        #self.player1Designs = self.player1.designs


        # print("setup: shipDesign:%d  \n%s"%(len(self.playerDesigns.currentShips), self.playerDesigns.currentShips))
        # print("setup: %s ::: %s" % (self.testShip1_name, self.design_testShip1.designName))

        # self.p1_colonyPQ = self.p1_colonyHW_obj.productionQ

        # self.p1_colonyPQ.test_ship = 0
        # self.p1_colonyPQ.productionOrder = []     
        # self.p1_colonyPQ.productionItems = {} 
        # self.p1_colonyPQ.test_ResourcesConsumed = 0


        # self.player1.fleetCommand.fleets = {}
        # self.player1.fleetCommand.nextFleetID = 0
        # self.universe.fleetObjects = {} 
        # self.universe.objectsAtXY[self.p1_colonyHW_obj.planet.xy] = []    # target_colony_obj exists here

        # self.player1.research.researchTax = .01    # set to 0 for production tests




        self.baseFleets = self.player1.fleetCommand.fleets #= {}
        self.baseFleetID = self.player1.fleetCommand.nextFleetID # = 0
        self.baseFleetObjects = self.universe.fleetObjects # = {} 
        self.baseObjectsAtXY = self.universe.objectsAtXY #[self.target_colony_obj.planet.xy] = []    # target_colony_obj exists here




    def teardown(self):
        print("TestFleets: Teardown")

        if False: print("p1_fleets:%s\np1_nextFleetID:%s \nuniverseFleets:%s \nobjectsAtXY:%s" %(self.player1.fleetCommand.fleets, self.player1.fleetCommand.nextFleetID, self.universe.fleetObjects, self.universe.objectsAtXY))

        self.player1.fleetCommand.fleets = self.baseFleets
        self.player1.fleetCommand.nextFleetID = self.baseFleetID
        self.universe.fleetObjects = self.baseFleetObjects
        self.universe.objectsAtXY = self.baseObjectsAtXY

        if True: print("p1_fleets:%s \np1_nextFleetID:%s \nuniverseFleets:%s \nobjectsAtXY:%s" %(self.player1.fleetCommand.fleets, self.player1.fleetCommand.nextFleetID, self.universe.fleetObjects, self.universe.objectsAtXY))


    @staticmethod
    def _getHW_XY(player):

        for colony in player.colonies.values():
            if colony.planet.HW:
                return colony.planet.xy




    def test_setupClass(self):

        ONEPLANET = 1
        SIXTYTHREE = 63 # 60 standard planets + 3 players with HWs

        assert_true(isinstance(self.player0, Player))
        assert_true(isinstance(self.player1, Player))
        assert_true(isinstance(self.player2, Player))
        assert_true(isinstance(self.p0_colonyHW_obj, Colony))
        assert_true(isinstance(self.p1_colonyHW_obj, Colony))
        assert_true(isinstance(self.p2_colonyHW_obj, Colony))
        assert_true(isinstance(self.universe, UniverseObject))
        assert_true(isinstance(self.player2.fleetCommand.fleets, dict))
        assert_true(isinstance(self.player2.fleetCommand.fleets[0], FleetObject))


        assert_equal(len(self.universePlanets), SIXTYTHREE)
        
        for player in self.game.players.values():
            colonyXY = TestFleets._getHW_XY(player)
            assert_true(len(player.fleetCommand.fleets) == startingShipDesignsCount())   # fleets should be starting fleet values
            assert_true(len(self.universe.objectsAtXY[colonyXY]) == startingShipDesignsCount() + ONEPLANET) 


        # print("objectsAtXY\n%s" % self.universe.objectsAtXY)
        # assert_true(False)
        startingDesignCount = startingShipDesignsCount()

        assert_equal(self.player0.fleetCommand.nextFleetID, len(self.player0.fleetCommand.fleets)) # zero based id
        
        

    def test_fleetID(self):

        testfleet = "TEST_FLEET_STUB"

        startingID = self.player0.fleetCommand.nextFleetID
        startingFleets = len(self.player0.fleetCommand.fleets)
        assert_true(startingFleets == startingShipDesignsCount())
        assert_true(startingFleets > 0)
        assert_true(startingFleets == 4)
        print("fleet(0) name: %s" % self.player0.fleetCommand.fleets[0].tokens)
        assert_true(startingID == 4)


    def test_generateFleetID(self):

        testUniverse = "TEST_UNIVERSE_STUB"
        testFleet = "TEST_FLEET_STUB"
        testPlayer = PlayerTestObject()
        testPlayer.playerNumber = 55

        testCommand = FleetCommand(testPlayer, testUniverse)
        assert_true(testCommand.nextFleetID == 0)
        assert_true(len(testCommand.fleets) == 0)

        assert_true(testCommand.generateFleetID() == 0)

        # --------- add a fleet ---------
        testCommand.fleets[0] = testFleet
        assert_true(len(testCommand.fleets) == 1)
        assert_true(testCommand.generateFleetID() == 1)

        # --------- add 3 more fleets -------

        testCommand.fleets[1] = testFleet
        testCommand.fleets[2] = testFleet
        testCommand.fleets[3] = testFleet
        assert_true(len(testCommand.fleets) == 4)
        assert_true(testCommand.generateFleetID() == 4)

        # --------- remove a fleet number in the middle ----

        del testCommand.fleets[2]
        print("Fleet Keys: %s" % testCommand.fleets.keys())
        assert_true(testCommand.generateFleetID() == 2) # next id is 2 

        # -------- add fleet key out of order -----
        testCommand.fleets[4] = testFleet
        testCommand.fleets[6] = testFleet
        testCommand.fleets[17] = testFleet
        testCommand.fleets[22] = testFleet
        testCommand.fleets[33] = testFleet

        assert_true(testCommand.generateFleetID() == 2) # next id is 2 

        testCommand.fleets[2] = testFleet

        assert_true(testCommand.generateFleetID() == 5)  
        testCommand.fleets[5] = testFleet
        testCommand.fleets[7] = testFleet
        testCommand.fleets[8] = testFleet
        testCommand.fleets[9] = testFleet
        testCommand.fleets[10] = testFleet
        testCommand.fleets[11] = testFleet
        assert_true(testCommand.generateFleetID() == 12) # next id is 12

        del testCommand.fleets[3]
        del testCommand.fleets[4]
        del testCommand.fleets[7]
        assert_true(testCommand.generateFleetID() == 3) 

        print("Fleet Keys: %s" % testCommand.fleets.keys())
        # ---------- stress the numbers -------
        testCommand.fleets.clear()
        assert_true(len(testCommand.fleets) == 0)
        assert_equal(testCommand.generateFleetID(), 0)

        testCommand.fleets[40] = testFleet
        testCommand.fleets[42] = testFleet
        testCommand.fleets[43] = testFleet
        testCommand.fleets[44] = testFleet
        testCommand.fleets[45] = testFleet
        testCommand.fleets[46] = testFleet
        testCommand.fleets[4] = testFleet
        print("Fleet Keys: %s" % testCommand.fleets.keys())

        assert_equal(testCommand.generateFleetID(), 0) 
        testCommand.fleets[0] = testFleet
        assert_equal(testCommand.generateFleetID(), 1) 

        print("Fleet Keys: %s" % testCommand.fleets.keys())
        #assert_true(False)



    def test_addFleet(self):

        testUniverse = "TEST_UNIVERSE_STUB"
        testFleet = "TEST_FLEET_STUB"
        testAlternativeFleet = "TEST_ALTERNATIVE_FLEET_STUB"
        testPlayer = PlayerTestObject()
        testPlayer.playerNumber = 55

        testCommand = FleetCommand(testPlayer, testUniverse)
        assert_true(testCommand.nextFleetID == 0)
        assert_true(len(testCommand.fleets) == 0)

        testCommand.addFleet(0, testFleet)
        assert_true(len(testCommand.fleets) == 1)
        assert_true(testCommand.generateFleetID() == 1)

        # --------- add another more fleets -------

        testCommand.fleets[1] = testFleet
        assert_true(len(testCommand.fleets) == 2)
        assert_true(testCommand.generateFleetID() == 2)

        # --------- add a duplicate ID  -----------
        testCommand.addFleet(0, testAlternativeFleet)
        assert_true(len(testCommand.fleets) == 2)
        assert_true(testCommand.generateFleetID() == 2)

        assert_equal(testCommand.fleets[0], testFleet)




