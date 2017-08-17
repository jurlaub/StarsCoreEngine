"""
    This file is part of Stars Core Engine, which provides an interface and 
    processing of Game data. 

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


import os
import os.path

from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_not_in, assert_true, assert_false


from ..starscoreengine.game import Game
from ..starscoreengine.template import *
from ..starscoreengine.player import Player
from ..starscoreengine.player import RaceData as Race
from ..starscoreengine.player_designs import PlayerDesigns
from ..starscoreengine.ship_design import ShipDesign 
from ..starscoreengine.productionQ import *
from ..starscoreengine.game_xfile import processDesign, processProductionQ
from ..starscoreengine.template_race import startingShipDesignsCount, startingDesignsCount






class TestStarsCoreEngineGame(object):
    """
    
    """

    def setup_class():
        """
        Generating 1 tech tree for all tests by making the techTree a class 
        level dictionary. (due to python namespace, the class tree will be found)

        """


        self = TestStarsCoreEngineGame

        print("TestStarsCoreEngineGame: Setup")


        self.playerFileList = ['Wolfbane', 'Bunnybane']
        self.testGameName = 'rabidTest'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.game = Game(self.gameTemplate)
        self.techTree = self.game.technology
        self.player = self.game.players['player1']

        self.techLevels = self.player.research.techLevels
        self.LRT = self.player.LRT

        #--------- obtain colony worlds -------------
        self.newColony = []
        self.universePlanets = self.game.game_universe[0].planets
        self.universe = self.game.game_universe[0]

        # find planets == newColonyCount in universe without an owner
        newColonyCount = 5 
        for kee, obj in self.universePlanets.items():
            if len(self.newColony) > newColonyCount:
                break

            if not obj.owner:
                self.newColony.append(kee)

        # colonize planets that are identified in self.newColony list
        for each in self.newColony:
            self.player.colonizePlanet(self.universePlanets[each], 150000)

        self.colony2_name = self.newColony[0] 
        self.colony2_object = self.player.colonies[self.colony2_name]
        

        #--------- obtain HW -------------
        self.target_colony_name = None
        self.target_colony_obj = None
        for kee, each in self.player.colonies.items():
            if each.planet.HW:
                self.target_colony_name = kee
                self.target_colony_obj = each
                break
        #--------- end ------------------










        self.d1_name = "Seer"
        self.d2_name = "Dark Star I"
        self.d3_name = "Dark Falcon"

        self.testShip1_name = 'doomShip1'
        self.testShip2_name = 'basic scout'
        self.testShip3_name = 'doomShip3'
        self.testShip4_name = 'doomShip4'

        self.testStarbase_OF = "Orbital Fort"
        self.testStarbase_SB = "Space Station"

        #  ---------------------- test PlayerDesigns.addDesign -----------------
        self.testShip1 = {'designName': self.testShip1_name, 
                          'designID': 4,
                          'hullID': 'Scout',
                          'component': {"B": {"itemID": "Fuel Mizer", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Mole Scanner", "itemQuantity": 1}
                            } }

        self.testShip2 = {'designName': self.testShip2_name , 
                          'designID': 5,
                          'hullID': 'Scout',
                          'component': {"B": {"itemID": "Quick Jump 5", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Bat Scanner", "itemQuantity": 1}
                            } }


        self.testShip3 = {'designName': self.testShip3_name, 
                          'designID': 6,
                          'hullID': 'Destroyer',
                          'component': {"G": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1 },
                                        "E": {"itemID": "Energy Capacitor", "itemQuantity": 1},
                                        "D": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 1},
                                        "F": {"itemID": "Crobmnium", "itemQuantity": 1},
                                        "C": {"itemID": "X-Ray Laser", "itemQuantity": 1},
                                        "B": {"itemID": "X-Ray Laser", "itemQuantity": 1},
                                        "A": {"itemID": "Manoeuvring Jet", "itemQuantity": 1}
                                                                    } }
        self.testShip4 = {'designName': self.testShip4_name, 
                          'designID': 7,
                          'hullID': "Privateer",
                          'component': {"A": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 2 },
                                        "B": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "D": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "E": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1},
                                                                    } }

        self.testStarbase1 = {  'designName': self.testStarbase_OF, 
                                'designID': 0,
                                'hullID': self.testStarbase_OF,
                                'component': {  "A": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 5 },
                                                "B": {"itemID": "X-Ray Laser", "itemQuantity": 5}
                                                                    } }

        self.testStarbase2 = {  'designName': self.testStarbase_SB, 
                                'designID': 2,
                                'hullID': self.testStarbase_SB,
                                'component': {  "A": {"itemID": "Wolverine Diffuse Shield", "itemQuantity": 2 },
                                                "B": {"itemID": "Colloidal Phaser", "itemQuantity": 5},
                                                "F": {"itemID": "Crobmnium", "itemQuantity": 1},
                                                "D": {"itemID": "Jihad Missile", "itemQuantity": 1}
                                                                    } }






        self.player1_shipDesignCount = 7
        self.player1_starbaseDesignCount = 2
        # not a complete x file, contains: Ship Design, Prod_Q, Prod_List
        self.player1_xFile = {
            "NewDesign" : { 
                "Design1" : 
                    {   "designName": self.d1_name, 
                        "designID": 1,
                        "hullID": "Scout",
                        "component":  {"B": {"itemID": "Quick Jump 5", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Bat Scanner", "itemQuantity": 1}
                                        }
                    },
                "Design2" : 
                    {   "designName": self.d2_name, 
                        "designID": 2,
                        "hullID": "Destroyer",
                        "component": {"G": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1 },
                                        "E": {"itemID": "Energy Capacitor", "itemQuantity": 1},
                                        "D": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 1},
                                        "F": {"itemID": "Crobmnium", "itemQuantity": 1},
                                        "C": {"itemID": "X-Ray Laser", "itemQuantity": 1},
                                        "B": {"itemID": "X-Ray Laser", "itemQuantity": 1},
                                        "A": {"itemID": "Manoeuvring Jet", "itemQuantity": 1}
                                        }

                    },
                "Design3" : 
                    {   "designName": self.d3_name, 
                        "designID": 3,
                        "hullID": "Privateer",
                        "component": {"A": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 2 },
                                        "B": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "D": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "E": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1},
                                        }

                    },
                "Design4" : self.testShip1,
                "Design5" : self.testShip2,
                "Design6" : self.testShip3,
                "Design7" : self.testShip4,
                "Design8" : self.testStarbase1,
                "Design9" : self.testStarbase2

            
            },
            "RemoveDesign" : []

        }

        # use existing method to import gamefile data
        processDesign(self.player1_xFile, self.player, self.game.technology)


        # used by ProductionQ for itemType
        self.productionID_Ship = "Ship"
        self.productionID_Starbase = "Starbase"






    def teardown_class():
        self = TestStarsCoreEngineGame
        

        print("TestStarsCoreEngineGame: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))



    def setup(self):
        print("TestStarsCoreEngineGame: Setup")

        self.produceNumberDefault = 1
        self.productNumberThree = 3
        self.productNumberSeven = 7

        self.produceShipDefault = self.testShip1_name
        self.produceScoutShip = self.d1_name
        self.produceDestroyerShip = self.testShip3_name
        self.produceTypeDefault = self.productionID_Ship


        self.test_1_item_template = {"ProductionQ" : 
            {
                self.target_colony_name:
                    {
                        "productionOrder" : [ self.produceShipDefault ],
                        "productionItems" : { self.produceShipDefault : {"quantity": self.produceNumberDefault, "designID": self.produceShipDefault, "itemType" : self.produceTypeDefault }                                             
                                            }

                    }

                }
            }

        self.test_starbase1_template = {"ProductionQ" : 
            {
                self.target_colony_name:
                    {
                        "productionOrder" : [ self.testStarbase_OF ],
                        "productionItems" : { self.testStarbase_OF : {"quantity": self.produceNumberDefault, "designID": self.testStarbase_OF, "itemType" : self.productionID_Starbase }                                             
                                            }

                    }

                }
            }



        self.test_2_item_template = {"ProductionQ" : 
            {
                self.target_colony_name:
                    {
                        "productionOrder" : [ self.produceScoutShip ],
                        "productionItems" : { self.produceScoutShip : {"quantity": self.produceNumberDefault, "designID": self.produceScoutShip, "itemType" : self.produceTypeDefault }                                             
                                            }

                    }

                }
            }

        self.test_destroyer = {"ProductionQ" : 
            {
                self.target_colony_name:
                    {
                        "productionOrder" : [ "destroyer_ship_alpha" ],
                        "productionItems" : { "destroyer_ship_alpha" : {"quantity": self.productNumberThree, "designID": self.produceDestroyerShip, "itemType" : self.produceTypeDefault }                                             
                                            }

                    }

                }
            }

        self.test_build_many_ships = {"ProductionQ" : 
            {
                self.target_colony_name:
                    {
                        "productionOrder" : [   "destroyer_ship_alpha", self.produceScoutShip, self.produceShipDefault ],
                        "productionItems" : {   "destroyer_ship_alpha" : {"quantity": self.productNumberThree, "designID": self.produceDestroyerShip, "itemType" : self.produceTypeDefault },
                                                self.produceScoutShip : {"quantity": self.productNumberSeven, "designID": self.produceScoutShip, "itemType" : self.produceTypeDefault},
                                                self.produceShipDefault : {"quantity": self.productNumberThree, "designID": self.produceShipDefault, "itemType" : self.produceTypeDefault }
                                            
                                            }

                    }

                }
            }     

        self.test_build_10_ships = {"ProductionQ" : 
            {
                self.target_colony_name:
                    {
                        "productionOrder" : [   "destroyer_ship_alpha", self.produceScoutShip, self.produceShipDefault ],
                        "productionItems" : {   "destroyer_ship_alpha" : {"quantity": self.productNumberSeven, "designID": self.produceDestroyerShip, "itemType" : self.produceTypeDefault },
                                                self.produceScoutShip : {"quantity": self.produceNumberDefault, "designID": self.produceScoutShip, "itemType" : self.produceTypeDefault},
                                                self.produceShipDefault : {"quantity": self.produceNumberDefault, "designID": self.produceShipDefault, "itemType" : self.produceTypeDefault }
                                            
                                            }

                    }

                }
            }  


        self.target_colony_obj.planet.factories = 10
        self.target_colony_obj.planet.surfaceIron = 200
        self.target_colony_obj.planet.surfaceBor = 200
        self.target_colony_obj.planet.surfaceGerm = 200
        self.target_colony_obj.population = 450000




        self.ironOnHW = self.target_colony_obj.planet.surfaceIron
        self.borOnHW = self.target_colony_obj.planet.surfaceBor
        self.germOnHW = self.target_colony_obj.planet.surfaceGerm
        self.populationOnHW = self.target_colony_obj.population

        # print("setup: On HW pop:%d iron: %d bor: %d germ: %s" % (self.populationOnHW, self.ironOnHW, self.borOnHW, self.germOnHW))

        # ----- ship design -----
        self.playerDesigns = self.player.designs
        self.design_testShip1 = self.player.designs.currentShips[self.testShip1_name]

        # print("setup: shipDesign:%d  \n%s"%(len(self.playerDesigns.currentShips), self.playerDesigns.currentShips))
        # print("setup: %s ::: %s" % (self.testShip1_name, self.design_testShip1.designName))

        self.colonyPQ = self.target_colony_obj.productionQ

        self.colonyPQ.test_ship = 0
        self.colonyPQ.productionOrder = []     
        self.colonyPQ.productionItems = {} 
        self.colonyPQ.test_ResourcesConsumed = 0



        self.player.fleetCommand.fleets = {}
        self.player.fleetCommand.currentFleetID = 0
        self.universe.fleetObjects = {}
        self.universe.objectsAtXY[self.target_colony_obj.planet.xy] = []

        # self.baseFleets = self.player.fleetCommand.fleets #= {}
        # self.baseFleetID = self.player.fleetCommand.currentFleetID # = 0
        # self.baseFleetObjects = self.universe.fleetObjects # = {} 
        # self.baseObjectsAtXY = self.universe.objectsAtXY #[self.target_colony_obj.planet.xy] = []    # target_colony_obj exists here

        self.player.research.researchTax = .01    # set to 0 for production tests


    def teardown(self):
        print("TestStarsCoreEngineGame: Teardown")

        # self.player.fleetCommand.fleets = self.baseFleets
        # self.player.fleetCommand.currentFleetID = self.baseFleetID
        # self.universe.fleetObjects = self.baseFleetObjects
        # self.universe.objectsAtXY = self.baseObjectsAtXY



    def test_produce_Starbase(self):
        
        starbaseQ = self.test_starbase1_template


        print("starbaseQ: %s " % starbaseQ)

        assert_true(self.target_colony_obj.planet.orbitalStarbase == None) #--TODO-- HW should start with starbase, need to change this

        processProductionQ(starbaseQ, self.player)

        assert_equal(len(self.colonyPQ.productionOrder), 1)
        assert_equal(len(self.colonyPQ.productionItems), 1)

        # assert_equal(self.colonyPQ.test_ship, 0)

        self.colonyPQ.productionController()
        
        # assert_equal(self.colonyPQ.test_ship, 1)  # placeholder to test Starbases
        print("test_produce_Starbase. orbitalStarbase:%s " %self.target_colony_obj.planet.orbitalStarbase)
        assert_equal(self.target_colony_obj.planet.orbitalStarbase.planetID, self.target_colony_obj.planet.ID)
        starbaseID = self.target_colony_obj.planet.ID + "_" + str(self.player.playerNumber)
        assert_equal(self.target_colony_obj.planet.orbitalStarbase.ID, starbaseID)

        assert_equal(len(self.target_colony_obj.planet.orbitalStarbase.tokens), 1) 


    def test_produced_fleet_added_to_universe_objectsAtXY(self):
        """
        a produced fleet must be added to universe.objectsAtXY 
        """
        ZERO = 0
        ONE = 1

        newFleetID = '1_0'

        fleetCommand = self.player.fleetCommand
        location = self.colonyPQ.colony.planet.xy

        objectsAtLocation = self.universe.objectsAtXY[location]
        countOfObjects = len(objectsAtLocation)
        print("objectsAtXY: %s count:%s" % (objectsAtLocation, countOfObjects))

        
        # ---------- produce ship & new fleet should be created ----
        processProductionQ(self.test_1_item_template, self.player)
        self.colonyPQ.productionController()    # a new fleet will be built



        # ------- test fleets ------
        assert_equal(len(fleetCommand.fleets), ONE)   # one fleets should exist
        print("test_produce_fleet_with_one_ship: fleetObject: %s" % self.universe.fleetObjects)
        assert_equal(len(self.universe.fleetObjects), ONE) 

        assert_true(newFleetID in self.universe.fleetObjects)

        assert_true(newFleetID in objectsAtLocation)
        print("objectsAtXY: keys:%s values:%s" % (self.universe.objectsAtXY.keys(), self.universe.objectsAtXY.values()))
        #assert_true(False)

        

        # playerFleet ID should now exist
        # playerFleets = self.universe.fleetObjects[self.player.playerNumber]

        # assert_equal(len(playerFleets), 1)      
        newFleet = self.universe.fleetObjects[newFleetID]

        setOfObjects = set(self.universe.objectsAtXY[location])
        #print("objectsAtXY: set:%s \nobjects:%s" % ( setOfObjects, self.universe.objectsAtXY[location]))
        assert_true(newFleetID in setOfObjects ) 
        
