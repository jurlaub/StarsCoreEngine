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
from ..starscoreengine.planet import Planet
from ..starscoreengine.colony import Colony
from ..starscoreengine.fleets import FleetObject
from ..starscoreengine.fleet_command import FleetCommand

from ..starscoreengine.universe import UniverseObject
from ..starscoreengine.template_race import startingDesigns, startingShipDesignsCount, startingDesignsCount, startingDesignsNames #colonyShip, scoutShip, destroyerShip, smallFrieghterShip


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

        # self.baseFleets_0 = self.player0.fleetCommand.fleets #= {}
        # self.baseFleetID_0 = self.player0.fleetCommand.nextFleetID # = 0



        # self.baseFleets = self.player1.fleetCommand.fleets #= {}
        # self.baseFleetID = self.player1.fleetCommand.nextFleetID # = 0
        # self.baseFleetObjects = self.universe.fleetObjects # = {} 
        # self.baseObjectsAtXY = self.universe.objectsAtXY #[self.target_colony_obj.planet.xy] = []    # target_colony_obj exists here




    def teardown(self):
        print("TestFleets: Teardown")

        # if False: print("p1_fleets:%s\np1_nextFleetID:%s \nuniverseFleets:%s \nobjectsAtXY:%s" %(self.player1.fleetCommand.fleets, self.player1.fleetCommand.nextFleetID, self.universe.fleetObjects, self.universe.objectsAtXY))

        # # self.player0.fleetCommand.fleets = self.baseFleets_0 #= {}
        # # self.player0.fleetCommand.nextFleetID = self.baseFleetID_0 # = 0


        # self.player1.fleetCommand.fleets = self.baseFleets
        # self.player1.fleetCommand.nextFleetID = self.baseFleetID
        # self.universe.fleetObjects = self.baseFleetObjects
        # self.universe.objectsAtXY = self.baseObjectsAtXY

        # if True: print("p1_fleets:%s \np1_nextFleetID:%s \nuniverseFleets:%s \nobjectsAtXY:%s" %(self.player1.fleetCommand.fleets, self.player1.fleetCommand.nextFleetID, self.universe.fleetObjects, self.universe.objectsAtXY))


        # ---- cleanup -----

        for each in self.player0.fleetCommand.fleets.values():

            hwxy = self.p0_colonyHW_obj.planet.xy

            # if each.xy != hwxy:

            self.universe._updateObjectsAtXY(each.ID, self.p0_colonyHW_obj.planet.xy, each.xy )
            each.xy = self.p0_colonyHW_obj.planet.xy
            each.destinationXY = each.xy
            each.fleetOrders = []
            each.speed = 0
            each.newSpeed = each.speed
            
        # for each, obj in self.universe.objectsAtXY.items():
        #     print("{} {}".format(each, obj))




    @staticmethod
    def _getHW_XY(player):

        for colony in player.colonies.values():
            if colony.planet.HW:
                return colony.planet.xy

    @staticmethod
    def _update_xy_orders(currentXY, offsetXY):

        return (currentXY[0] + offsetXY[0], currentXY[1] + offsetXY[1])


    @staticmethod
    def _obtain_fleet_orders_from_offset(currentLocation, offset ):

        temp = { "orders" : [ 
                {
                "coordinates" : TestFleets._update_xy_orders(currentLocation, offset),    # or at currentLocation
                "velocity_command" : "speed_levels_from_list",
                "waypoint_action" : "action_from_list" 
                } ]
            }
        return temp



    @staticmethod
    def _standard_offset():
        NORTH_OFFSET = (0, 50, 0)
        EAST_OFFSET = (50, 0, 0)
        SOUTH_OFFSET = (0, -50, 0)
        WEST_OFFSET = (-50, 0, 0)
        OFFSET_LIST = [NORTH_OFFSET, EAST_OFFSET, SOUTH_OFFSET, WEST_OFFSET ]

        return OFFSET_LIST


        




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


    def test_xFileStartingDesigns(self):

        designNames = startingDesignsNames()

        assert_equal(len(designNames), startingDesignsCount())

        designList = startingDesigns()

        for each in designList["NewDesign"].keys():
            assert_true(each in designNames)



    def test_fleetsUpdateDestinationXY(self):


        fc_0 = self.player0.fleetCommand
        hw_0_xy = self.p0_colonyHW_obj.planet.xy
        print(hw_0_xy)
        assert_true(isinstance(hw_0_xy,  tuple))
        offset_locations = TestFleets._standard_offset()


        testCommands = {}
        for x in range(0, startingShipDesignsCount()):
            testCommands[x] = TestFleets._obtain_fleet_orders_from_offset(hw_0_xy, offset_locations[0] )

        assert_equal(len(testCommands), 4)

        
        # ----- test the coord values before orders ------
        for fleetObj in fc_0.fleets.values():
            assert_true(isinstance(fleetObj.xy,  tuple))
            assert_true(isinstance(fleetObj.destinationXY,  tuple))
            assert_equal(hw_0_xy, fleetObj.xy)
            assert_equal(fleetObj.destinationXY, hw_0_xy)
            


        # move action
        fc_0.addOrdersToFleetsForTurn(testCommands)

        #print(testCommands)
        for key, commands in testCommands.items():
            assert_equal(fc_0.fleets[key].destinationXY, commands["orders"][0]["coordinates"])
            





    def test_fleetObjectAtCorrectUniverseLocationAfterMove(self):

        fc_0 = self.player0.fleetCommand
        hw_0_xy = self.p0_colonyHW_obj.planet.xy
        offset_locations = TestFleets._standard_offset()


        testCommands = {}
        for x in range(0, startingShipDesignsCount()):
            testCommands[x] = TestFleets._obtain_fleet_orders_from_offset(hw_0_xy, offset_locations[0] )

        assert_equal(len(testCommands), 4)



        fc_0.addOrdersToFleetsForTurn(testCommands)
        fc_0.fleetsMove()

        # test for ship at new location
        for key, obj in testCommands.items():
            print("test object %s" % obj["orders"][0])

            tmp_coord = tuple(obj["orders"][0]["coordinates"])

            assert_true(isinstance(tmp_coord, tuple))

            print("temp coord %s %s" % tmp_coord)

            if tmp_coord in self.universe.objectsAtXY:
                test_items = self.universe.objectsAtXY[tmp_coord]
                print(test_items)
                assert_in('0_'+ str(key), test_items)
                assert_not_in('0_'+ str(key), self.universe.objectsAtXY[hw_0_xy] )

            
            else: 
                assert_in(tmp_coord, self.universe.objectsAtXY)
        
        # print("HW : (%s, %s)" % hw_0_xy)
        # for each, every in self.universe.objectsAtXY.items():
        #     print("{} : {} ".format(each, every))

        # assert_false(True)



    def test_fleetObjectHasCorrectXYAfterMove(self):

        fc_0 = self.player0.fleetCommand
        hw_0_xy = self.p0_colonyHW_obj.planet.xy
        offset_locations = TestFleets._standard_offset()


        testCommands = {}
        for x in range(0, startingShipDesignsCount()):
            testCommands[x] = TestFleets._obtain_fleet_orders_from_offset(hw_0_xy, offset_locations[0] )

        assert_equal(len(testCommands), 4)

        for fleetObj in fc_0.fleets.values():
            assert_true(fleetObj.xy == hw_0_xy)


        fc_0.addOrdersToFleetsForTurn(testCommands)
        fc_0.fleetsMove()

        for fleetObj in fc_0.fleets.values():
            assert_false(fleetObj.xy == hw_0_xy)

        # # test for ship at new location
        # for key, obj in testCommands.items():
        #     print("{} test object {}".format('0_'+ str(key), obj["orders"][0]))

        #     tmp_coord = tuple(obj["orders"][0]["coordinates"]) # xy coord from orders

        #     assert_true(isinstance(tmp_coord, tuple))

        #     print("temp coord %s %s" % tmp_coord)

        #     if tmp_coord in self.universe.objectsAtXY:
        #         test_items = self.universe.objectsAtXY[tmp_coord]
        #         print("HW{} New{} : {}".format(hw_0_xy, tmp_coord, test_items))
        #         assert_in('0_'+ str(key), test_items)
        #         assert_not_in('0_'+ str(key), self.universe.objectsAtXY[hw_0_xy] )


            
        #     else: 
        #         assert_in(tmp_coord, self.universe.objectsAtXY)
        




        # print("HW : (%s, %s)" % hw_0_xy)
        # for each, every in self.universe.objectsAtXY.items():
        #     print("{} : {} ".format(each, every))

        # assert_false(True)



    def test_addOrdersToFleetsForTurn(self):

        NORTH_OFFSET = (0, 50, 0)
        EAST_OFFSET = (50, 0, 0)
        SOUTH_OFFSET = (0, -50, 0)
        WEST_OFFSET = (-50, 0, 0)
        #OFFSET_LIST = [NORTH_OFFSET, EAST_OFFSET, SOUTH_OFFSET, WEST_OFFSET ]

        fc_0 = self.player0.fleetCommand
        hw_0_xy = self.p0_colonyHW_obj.planet.xy

        # ---------- setup and test -----------


        startingShipCount = startingShipDesignsCount()
        assert_equal(len(fc_0.fleets), startingShipCount)

        for key, obj in fc_0.fleets.items():
            assert_true( isinstance(obj.fleetOrders, list)) # fleet has list of orders
            assert_equal(len(obj.fleetOrders), 0)           # fleet orders is empty
            assert_equal(obj.xy, hw_0_xy)                   # fleet is at HW (x,y)

        # ----------- give orders and test -------

        print("hw_0_xy: %s; n_order: %s; e_order:%s" % (hw_0_xy, TestFleets._update_xy_orders(hw_0_xy, NORTH_OFFSET), TestFleets._update_xy_orders(hw_0_xy, EAST_OFFSET)))

        #assert_false(True)


        testCommands =      {
                0 : { "orders" : [ 
                            {
                                "coordinates" : TestFleets._update_xy_orders(hw_0_xy, NORTH_OFFSET),    # or at currentLocation
                                "velocity_command" : "speed_levels_from_list",
                                "waypoint_action" : "action_from_list" 

                            } ]
                    },
                1 : { "orders" : [
                            {
                                "coordinates" : TestFleets._update_xy_orders(hw_0_xy, EAST_OFFSET),     # or at currentLocation  
                                "velocity_command" : "speed_levels_from_list",
                                "waypoint_action" : "action_from_list"

                            } ] 
                    },
                2 : { "orders" : [ 
                            {
                                "coordinates" : TestFleets._update_xy_orders(hw_0_xy, SOUTH_OFFSET),    # or at currentLocation
                                "velocity_command" : "speed_levels_from_list",
                                "waypoint_action" : "action_from_list" 

                            }]
                    },
                3 : { "orders" : [
                            {
                                "coordinates" : TestFleets._update_xy_orders(hw_0_xy, WEST_OFFSET),     # or at currentLocation  
                                "velocity_command" : "speed_levels_from_list",
                                "waypoint_action" : "action_from_list"
                            } ] 
                    }

            }


        # send orders to fleet
        fc_0.addOrdersToFleetsForTurn(testCommands)



        for key, obj in fc_0.fleets.items():
            assert_true( isinstance(obj.fleetOrders, list)) # fleet has list of orders
            assert_equal(len(obj.fleetOrders), 1)           # fleet orders is empty





        



