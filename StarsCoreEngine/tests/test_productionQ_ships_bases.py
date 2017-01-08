"""
    This file is part of Stars Core Engine, which provides an interface and processing of Game data.
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
Purpose:    To test building Ships and Starbases
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
from ..starscoreengine.productionQ import *
from ..starscoreengine.game_xfile import processDesign, processProductionQ






class TestShipDesign(object):
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


        self = TestShipDesign

        print("TestShipDesign: Setup")


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
        self = TestShipDesign
        

        print("TestShipDesign: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))



    def setup(self):
        print("TestShipDesign: Setup")

        self.produceNumberDefault = 1
        self.produceShipDefault = self.testShip1_name
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



        self.target_colony_obj.planet.surfaceIron = 200
        self.target_colony_obj.planet.surfaceBor = 200
        self.target_colony_obj.planet.surfaceGerm = 200
        self.target_colony_obj.population = 450000



        self.ironOnHW = self.target_colony_obj.planet.surfaceIron
        self.borOnHW = self.target_colony_obj.planet.surfaceBor
        self.germOnHW = self.target_colony_obj.planet.surfaceGerm
        self.populationOnHW = self.target_colony_obj.population

        print("setup: On HW pop:%d iron: %d bor: %d germ: %s" % (self.populationOnHW, self.ironOnHW, self.borOnHW, self.germOnHW))

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


    def teardown(self):
        print("TestShipDesign: Teardown")

    def test_setupClass(self):

        assert_equal(len(self.player.designs.currentShips), 7)
        assert_equal(len(self.player.designs.currentStarbases), 2)
        # ship = self.player.designs.currentShips
        # print("ship:%s  costs:%s" % (ship[self.d1_name].designName, ship[self.d1_name].currentCosts() ))

        # print("ship:%s  costs:%s" % (ship[self.testShip1_name].designName, ship[self.testShip1_name].currentCosts() ))

    def test_testShip3(self):
        """
        Destroyer + DaddyLongLegs + E_cap + BearShield + Crobmnium + X-Ray + X-Ray + Manoeuvring jet

        hull    = (iron, bor, germ, resources, mass)
        HULL    = (15, 3, 5, 35, 30)
        Engine  = (11, 0, 3, 12, 13)
        E_cap   = ( 0, 0, 8,  5,  1)
        shield  = ( 4, 0, 4,  8,  1)
        armor   = ( 6, 0, 0, 13, 56)
        X-Ray   = ( 0, 6, 0,  6,  1)
        X-Ray   = ( 0, 6, 0,  6,  1)
        Jet     = ( 5, 0, 5, 10, 35)
        total   = (41, 15, 25, 95, 138)


        fuelCapacity = (280)
        armorDP = 200 + 75
        shieldDP = 100
        scanning = 0

        range = 1
        beamPower = 16 + 16
        sapper = False
        capacitor = [.1]
        battleMovement = NOT TESTED YET!


        """
        # assert_equal(len(self.player.design.currentShips), 0)
        # self.player.design.addDesign(self.testShip1, self.techTree)
        # assert_equal(len(self.player.design.currentShips), 1)
        target = self.testShip3
        ship = ShipDesign(target, self.techTree, self.techLevels, self.LRT) #self.testShip1['hullID'], self.testShip1, self.testShip1['designName']
        
        assert_equal(ship.iron, 41)
        assert_equal(ship.bor, 15)
        assert_equal(ship.germ, 25)
        assert_equal(ship.resources, 95)
        assert_equal(ship.mass, 138)

        assert_equal(ship.normalScanRange, None)
        assert_equal(ship.armorDP, 275)
        assert_equal(ship.fuelCapacity, 280)
        assert_equal(ship.hasLRT, [])

        assert_equal(ship.owner, None)      # owner is added when assigned to a players.design object
        assert_equal(ship.isDesignLocked, False)
        assert_equal(ship.designValidForProduction, True)

        assert_equal(ship.hullID, target['hullID'])

        # tech values are different
        assert_equal(ship.energy, 10)         #should only show the max tech (not a sum)
        assert_equal(ship.weapons, 3)        #should only show the max tech (not a sum)
        assert_equal(ship.propulsion, 5)     #should only show the max tech (not a sum)
        assert_equal(ship.construction, 3)   #should only show the max tech (not a sum)
        assert_equal(ship.electronics, 4)    #should only show the max tech (not a sum)
        assert_equal(ship.biotechnology, 0)  #should only show the max tech (not a sum)

        assert_equal(ship.range, 1)
        assert_equal(ship.beamPower, 32)
        assert_equal(ship.sapper, False)
        assert_equal(ship.capacitor, [10])
        assert_equal(ship.shieldDP, 100)



        # other values should not change
        assert_equal(ship.stealFromPlanets, False)
        assert_equal(ship.terraform, False)
        assert_equal(ship.warp10safe, False)

        assert_equal(ship.fuelGeneration, None)
        assert_equal(ship.cloaking, [0])
        assert_equal(ship.cargoCapacity, 0)

    def test_testShip2(self):
        """
        scout + quick jump 5 + fuel tank + Bat scanner

        hull    = (iron, bor, germ, resources, mass)
        scout   = (4,  2,  4, 10,  8)
        qJump5  = (3,  0,  1,  3,  4)
        fTank   = (6,  0,  0,  4,  3)
        bScan   = (1,  0,  1,  1,  2)
        total   = (14, 2,  6, 18, 17)


        fuelCapacity = (50 + 250)
        armorDP = 20
        scanning = 0


        """
        # assert_equal(len(self.player.design.currentShips), 0)
        # self.player.design.addDesign(self.testShip1, self.techTree)
        # assert_equal(len(self.player.design.currentShips), 1)
        target = self.testShip2

        ship = ShipDesign(target, self.techTree, self.techLevels, self.LRT) #self.testShip1['hullID'], self.testShip1, self.testShip1['designName']

        assert_equal(ship.iron, 14)
        assert_equal(ship.bor, 2)
        assert_equal(ship.germ, 6)
        assert_equal(ship.resources, 18)
        assert_equal(ship.mass, 17)

        assert_equal(ship.normalScanRange, [0])
        assert_equal(ship.armorDP, 20)
        assert_equal(ship.fuelCapacity, 300)
        assert_equal(ship.hasLRT, [])

        assert_equal(ship.owner, None)      # owner is added when assigned to a players.design object
        assert_equal(ship.isDesignLocked, False)
        assert_equal(ship.designValidForProduction, True)

        assert_equal(ship.hullID, target['hullID'])

        # tech values are different
        assert_equal(ship.energy, 0)         #should only show the max tech (not a sum)
        assert_equal(ship.weapons, 0)        #should only show the max tech (not a sum)
        assert_equal(ship.propulsion, 0)     #should only show the max tech (not a sum)
        assert_equal(ship.construction, 0)   #should only show the max tech (not a sum)
        assert_equal(ship.electronics, 0)    #should only show the max tech (not a sum)
        assert_equal(ship.biotechnology, 0)  #should only show the max tech (not a sum)


        # other values should not change
        assert_equal(ship.stealFromPlanets, False)
        assert_equal(ship.terraform, False)
        assert_equal(ship.warp10safe, False)

        assert_equal(ship.fuelGeneration, None)
        assert_equal(ship.cloaking, [0])
        assert_equal(ship.cargoCapacity, 0)

    def test_testShip1(self):
        """
        scout + fuel mizer + fuel tank + Mole scanner

        hull    = (iron, bor, germ, resources, mass)
        scout   = (4,  2,  4, 10,  8)
        fMizer  = (8,  0,  0, 11,  6)
        fTank   = (6,  0,  0,  4,  3)
        mScan   = (2,  0,  2,  9,  2)
        total   = (20, 2,  6, 34, 19)


        fuelCapacity = (50 + 250)
        armorDP = 20
        scanning = 100


        """
        # assert_equal(len(self.player.design.currentShips), 0)
        # self.player.design.addDesign(self.testShip1, self.techTree)
        # assert_equal(len(self.player.design.currentShips), 1)
        target = self.testShip1
        ship = ShipDesign(target, self.techTree, self.techLevels, self.LRT) #self.testShip1['hullID'], self.testShip1, self.testShip1['designName']

        assert_equal(ship.iron, 20)
        assert_equal(ship.bor, 2)
        assert_equal(ship.germ, 6)
        assert_equal(ship.resources, 34)
        assert_equal(ship.mass, 19)

        assert_equal(ship.normalScanRange, [100])
        assert_equal(ship.armorDP, 20)
        assert_equal(ship.fuelCapacity, 300)
        assert_equal(ship.hasLRT, ["IFE"])

        assert_equal(ship.owner, None)      # owner is added when assigned to a players.design object
        assert_equal(ship.isDesignLocked, False)
        assert_equal(ship.designValidForProduction, True)

        assert_equal(ship.hullID, target['hullID'])

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
        assert_equal(ship.cloaking, [0])
        assert_equal(ship.cargoCapacity, 0)

    def test_starbase2(self):
        """
       
        hull                = (iron, bor, germ, resources, mass)
        Space Station       = (240,  160,  500, 1200,   8)
        Wolv Diff Shield    = (6,      0,    6,   12,   2)   =  (3,      0,    3,    6,   1)  x2                         
        Colloidal Phaser    = (0,     70,    0,   90,  10)  =  (0,     14,    0,   18,   2)  x5
        Crobmnium           = (6,      0,    0,   13,  56)
        Jihad Missile       = (37,    13,    9,   13,  35)
        total               = (289,  243,  515,  1328, 101)


        "A": {"itemID": "Wolverine Diffuse Shield", "itemQuantity": 2 },
        "B": {"itemID": "Colloidal Phaser", "itemQuantity": 5},
        "F": {"itemID": "Crobmnium", "itemQuantity": 1},
        "D": {"itemID": "Jihad Missile", "itemQuantity": 1}
                                                                    }

        """
        starbase = self.playerDesigns.currentStarbases[self.testStarbase_SB]
        print("costs: %s" % starbase.currentCosts)

        assert_equal(starbase.iron, 289)
        assert_equal(starbase.bor, 243)
        assert_equal(starbase.germ, 515)
        assert_equal(starbase.resources, 1328)

    def test_starbase1(self):
        """
       
        hull                = (iron, bor, germ, resources)
        Orbital Fort        = (24,  0,  34,      80)
        Bear Neutrino Barr  = (20,  0,  20,      40) = ( 4,  0,   4,      8) x5
        X-Ray Laser         = ( 0,  30,  0,      30) =  ( 0,  6,   0,      6)  x5
        
        total               = (44,  30,  54,     150)



        {  "A": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 5 },
        "B": {"itemID": "X-Ray Laser", "itemQuantity": 5}
                                                                    }

        """

        starbase = self.playerDesigns.currentStarbases[self.testStarbase_OF]
        print("costs: %s" % starbase.currentCosts)

        assert_equal(starbase.iron, 44)
        assert_equal(starbase.bor, 30)
        assert_equal(starbase.germ, 54)
        assert_equal(starbase.resources, 150)

    def test_targetItemCosts_Ship(self):
        # print("--TODO-- test_targetItemCosts_Ship Ship Resource Cost HARDCODED -[41, 12, 34, 138]- This one is dynamic and requires extra effort")
        ship = self.playerDesigns.currentShips
        expectedItemCosts = ship[self.testShip1_name].currentCosts()
        
        targetItem = self.target_colony_obj.productionQ.targetItemCosts(TestShipDesign.productionID_Ship, self.testShip1_name)

        assert_equal(targetItem, expectedItemCosts)

    def test_targetItemCosts_Starbase(self):
        print("--TODO-- test_targetItemCosts_Starbase Starbase Resource Cost HARDCODED -[71, 48, 34, 338]- This one is dynamic and requires extra effort")

        # expectedItemCosts = [71, 48, 34, 338]
        starbase = self.playerDesigns.currentStarbases
        expectedItemCosts = starbase[self.testStarbase_SB].currentCosts()


        targetItem = self.target_colony_obj.productionQ.targetItemCosts(TestShipDesign.productionID_Starbase, self.testStarbase_SB)

        assert_equal(targetItem, expectedItemCosts)





    def test_produce_Starbase(self):
        
        starbaseQ = self.test_starbase1_template


        print("starbaseQ: %s " % starbaseQ)

        assert_true(self.target_colony_obj.planet.orbitalStarbase == None) #--TODO-- HW should start with starbase, need to change this

        processProductionQ(starbaseQ, self.player)

        assert_equal(len(self.colonyPQ.productionOrder), 1)
        assert_equal(len(self.colonyPQ.productionItems), 1)

        assert_equal(self.colonyPQ.test_ship, 0)

        self.colonyPQ.productionController()
        
        assert_equal(self.colonyPQ.test_ship, 1)  # placeholder to test Starbases
        print("test_produce_Starbase. orbitalStarbase:%s " %self.target_colony_obj.planet.orbitalStarbase)
        assert_equal(self.target_colony_obj.planet.orbitalStarbase.planetID, self.target_colony_obj.planet.ID)
        starbaseID = self.target_colony_obj.planet.ID + "_" + str(self.player.playerNumber)
        assert_equal(self.target_colony_obj.planet.orbitalStarbase.ID, starbaseID)

        assert_equal(len(self.target_colony_obj.planet.orbitalStarbase.tokens), 1) 


    def test_produce_fleetID(self):
        """
        FleetIDs must be unique to the game and player.
        FleetIDs can be reused as long as the previous instance of the fleet no longer exists 

        tests FleetCommand object 

        """

        fleetCommand = self.player.fleetCommand
        assert_equal(len(fleetCommand.fleets), 0)

        fleet1 = fleetCommand.generateFleetID()
        fleet2 = fleetCommand.generateFleetID()

        assert_equal(fleet1, fleet2)  # no new fleet generated so 


        processProductionQ(self.test_1_item_template, self.player)

        assert_equal(len(self.colonyPQ.productionOrder), 1)
        assert_equal(len(self.colonyPQ.productionItems), 1)

        assert_equal(len(fleetCommand.fleets), 0)

        self.colonyPQ.productionController()    # a new fleet will be built
        
        assert_equal(len(fleetCommand.fleets), 1)
        # print("test_fleet: %s\n%s" % (fleetCommand.fleets.keys(), fleetCommand.fleets[0].ID))

        fleet3 = fleetCommand.generateFleetID()

        assert_not_equal(fleet1, fleet3)    # a fleet has been created, so new fleet ID should be used.
        assert_equal(fleet3, fleet1 + 1)

        assert_in(fleet1, fleetCommand.fleets)


    def test_produce_fleet_with_one_ship(self):
        """

        """
        ZERO = 0
        ONE = 1

        fleetCommand = self.player.fleetCommand

        # --------  test fleets -------
        assert_equal(len(fleetCommand.fleets), ZERO)   # no fleets should exist
        assert_equal(fleetCommand.currentFleetID, ZERO) # fleetID should be 0


        # ---------- produce ship & new fleet should be created ----
        processProductionQ(self.test_1_item_template, self.player)
        assert_equal(len(self.colonyPQ.productionOrder), 1)
        assert_equal(len(self.colonyPQ.productionItems), 1)

        assert_equal(self.colonyPQ.test_ship, 0)

        self.colonyPQ.productionController()    # a new fleet will be built

        # ------- test fleets ------
        assert_equal(len(fleetCommand.fleets), ONE)   # one fleets should exist
        fleet = fleetCommand.generateFleetID()
        assert_equal(fleet, ONE) # fleetID should be 1

        newFleet = fleetCommand.fleets[0]

        assert_equal(len(newFleet.tokens), 1)        

