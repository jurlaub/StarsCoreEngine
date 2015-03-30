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
import os
import os.path


from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_not_in, assert_true, assert_false



from ..starscoreengine.productionQ import *

from ..starscoreengine.game import Game
from ..starscoreengine.template import *
from ..starscoreengine.player import Player
# from ..starscoreengine.player import RaceData as Race
from ..starscoreengine.player_designs import PlayerDesigns
# from ..starscoreengine.tech import ShipDesign 
from ..starscoreengine.game_xfile import processDesign, processProductionQ



class TestProductionQ(object):
    """
    Tests for ProductionQ



    """

    def setup_class():
        """
        Generating 1 tech tree for all tests by making the techTree a class 
        level dictionary. (due to python namespace, the class tree will be found)

        """


        self = TestProductionQ

        print("TestProductionQ: Setup")


        self.playerFileList = ["Wolfbane", "Bunnybane"]
        self.testGameName = "rabidTest"
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.game = Game(self.gameTemplate)
        self.techTree = self.game.technology
        self.player = self.game.players["player0"]

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

                    }
            
            },
            "RemoveDesign" : []

        }

        processDesign(self.player1_xFile, self.player, self.game.technology)





    def teardown_class():
        self = TestProductionQ
        

        print("TestProductionQ: Teardown")
        try:
            tmpFileName = self.testGameName + "_TechTreeDataError"
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))


    def setup(self):
        print("TestProductionQ: Setup")

        self.standardQ = {"ProductionQ" : 
                {
                self.target_colony_name : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { 
                            "entryID1" : {
                                "quantity": 5, 
                                "productionID": "item1"
                                }, 
                            "entryID2" : {
                                "quantity": 5, 
                                "productionID": "item1"} }
                    }

                }
            }

        self.testQ = {"ProductionQ" : 
                {
                self.target_colony_name : 
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2" ],
                        "productionItems" : 
                            { 
                            "entryID1" : 
                                {
                                "quantity": 5, 
                                "productionID": "mines"
                                }, 
                            "entryID2" : 
                                {
                                "quantity": 10, 
                                "productionID": "factories"
                                },
                            "entryID4" : 
                                {
                                "quantity": 455, 
                                "productionID": "mines"
                                }                 
                            }
                    }

                }
            }
        
        # set a number of variables to the same value - so they can be reused
        surfaceMinerals1 = [100, 20, 31]
        population1 = 150000
        popEfficiency = 1000


        #self.colony2_object.planet.updateSurfaceMinerals(surfaceMinerals1)
        self.colony2_object.planet.surfaceIron = surfaceMinerals1[0]
        self.colony2_object.planet.surfaceBor = surfaceMinerals1[1]
        self.colony2_object.planet.surfaceGerm = surfaceMinerals1[2]

        self.colony2_object.population = population1
        self.colony2_object.calcTotalResources(popEfficiency)






    def teardown(self):
        # print("TestProductionQ: Teardown")
        # try:
        #     tmpFileName = self.testGameName + "_TechTreeDataError"
        #     cwd = os.getcwd()
        #     tmpFileName = r"%s/%s"% (cwd, tmpFileName)
        #     if os.path.isfile(tmpFileName):
        #         os.remove(tmpFileName)
        # except IOError as e:
        #     print("Unable to remove file: %s" % (tmpFileName))
        pass


    def test_PQ_suppliesAreSufficient(self):
        """ class test for ProductionQ.suppliesAreSufficient

        """

        ts1 = [11, 23, 58, 1321]
        ts2 = [11, 0, 58, 1321]
        ts3 = [0, 0, 0, 0]
        availableSupplies1 = [0, 0, 0, 0]
        availableSupplies2 = [20, 20, 20, 20]
        availableSupplies3 = [1000, 1000, 1000, 2000]

        test1_false = ProductionQ.suppliesAreSufficient(ts1, availableSupplies1)
        assert_false(test1_false)

        test2_false = ProductionQ.suppliesAreSufficient(ts1, availableSupplies2)
        assert_false(test2_false)

        test3_false = ProductionQ.suppliesAreSufficient(ts2, availableSupplies1)
        assert_false(test3_false)

        test4_false = ProductionQ.suppliesAreSufficient(ts2, availableSupplies2)
        assert_false(test4_false)

        test5_true = ProductionQ.suppliesAreSufficient(ts1, availableSupplies3)
        assert_true(test5_true)

        test6_true = ProductionQ.suppliesAreSufficient(ts2, availableSupplies3)
        assert_true(test6_true)

        test7_true = ProductionQ.suppliesAreSufficient(ts3, availableSupplies3)
        assert_true(test7_true)

        test8_true = ProductionQ.suppliesAreSufficient(ts3, availableSupplies1)
        assert_true(test8_true)

        

    def test_PQ_limit(self):
        """ class test for ProductionQ.limit


        """
        quantity1 = 1
        quantity2 = 15
        quantity3 = 20
        quantity4 = 0

        ts1 = [11, 23, 58, 132]
        ts2 = [11, 0, 1, 13]
        ts3 = [0, 0, 0, 0]

        as1 = [0, 0, 0, 0]
        as2 = [20, 20, 20, 20]
        as3 = [1000, 1000, 1000, 2000]
        as4 = [200, 0, 20, 600]

        # -------------- ts1 --------------
        buildQuantity, buildMaterial = ProductionQ.limit(quantity1, ts1, as1)
        assert_true(buildQuantity == 0)
        assert_equal(buildMaterial, [0, 0, 0, 0])

        buildQuantity, buildMaterial = ProductionQ.limit(quantity1, ts1, as3)
        assert_true(buildQuantity == 1)
        assert_equal(buildMaterial, [11, 23, 58, 132])       
        

        # -------------- ts2 --------------
        buildQuantity, buildMaterial = ProductionQ.limit(quantity2, ts2, as2)
        assert_true(buildQuantity == 1)
        assert_equal(buildMaterial, [11, 0, 1, 13])  

        buildQuantity, buildMaterial = ProductionQ.limit(quantity3, ts2, as3)
        #print("%d:%s" % (buildQuantity, str(buildMaterial)))
        assert_true(buildQuantity == 20)
        assert_equal(buildMaterial, [220, 0, 20, 260])          
        
        buildQuantity, buildMaterial = ProductionQ.limit(quantity3, ts2, as4)
        #print("%d:%s" % (buildQuantity, str(buildMaterial)))
        assert_true(buildQuantity == 18)
        assert_equal(buildMaterial, [198, 0, 18, 234])  

        # -------------- ts3 --------------
        buildQuantity, buildMaterial = ProductionQ.limit(quantity2, ts3, as2)
        #print("%d:%s" % (buildQuantity, str(buildMaterial)))
        assert_true(buildQuantity == 0)
        assert_equal(buildMaterial, [0, 0, 0, 0]) 

        buildQuantity, buildMaterial = ProductionQ.limit(quantity3, ts3, as1)
        assert_true(buildQuantity == 0)
        assert_equal(buildMaterial, [0, 0, 0, 0]) 

        buildQuantity, buildMaterial = ProductionQ.limit(quantity3, ts3, as4)
        assert_true(buildQuantity == 0)
        assert_equal(buildMaterial, [0, 0, 0, 0]) 

        # -------------- ts2 --------------
        buildQuantity, buildMaterial = ProductionQ.limit(quantity4, ts2, as2)
        #print("%d:%s" % (buildQuantity, str(buildMaterial)))
        assert_true(buildQuantity == 0)
        assert_equal(buildMaterial, [0, 0, 0, 0]) 

        # -------------- ts3 --------------
        buildQuantity, buildMaterial = ProductionQ.limit(quantity4, ts3, as2)
        #print("%d:%s" % (buildQuantity, str(buildMaterial)))
        assert_true(buildQuantity == 0)
        assert_equal(buildMaterial, [0, 0, 0, 0]) 


    def test_SplitEntryIntoTwo(self):
        """
        need:
            ProductionQ
            entry in Q with more then 1 entry
            entry with quantity = 2+
            entry with quantity = 2 and work done
            entry wiht quantity 1
        """
        tmpMaterials = [3, 1, 5, 4]

        colonyHW = self.target_colony_obj.productionQ
        assert_true(colonyHW)

        # 2nd colony - sanity check Pre-first call
        assert_equal(colonyHW.productionOrder, [])
        assert_equal(colonyHW.productionItems, {}) 

        processProductionQ(self.testQ, self.player)
        assert_equal(len(colonyHW.productionOrder), 3)
        assert_equal(len(colonyHW.productionItems), 3)

        currentEntry = colonyHW.productionOrder[0]
        targetQuantity = 3
        colonyHW.productionItems[currentEntry]["quantity"] = targetQuantity
        colonyHW.productionItems[currentEntry]["materialsUsed"] = tmpMaterials

        colonyHW.splitEntryIntoTwo(currentEntry)

        assert_equal(len(colonyHW.productionOrder), 4)
        assert_equal(len(colonyHW.productionItems), 4)
        print(colonyHW.productionOrder)

        assert_equal(currentEntry, colonyHW.productionOrder[1])

        splitEntry_name = colonyHW.productionOrder[0]
        splitEntry_obj = colonyHW.productionItems[splitEntry_name]
        assert_equal(splitEntry_obj["quantity"], 1)
        assert_equal(splitEntry_obj["materialsUsed"], tmpMaterials)
        
        assert_equal(colonyHW.productionItems[currentEntry]["quantity"], targetQuantity - 1)
                

    def test_buildLimit(self):
        """
        buildLimit is like ProductionQ.limit() but is connected to the colony 
        resources.
        
        specify the colony.planet resources 
        test resources
        ensure the tests work within the resource availibility.

        surfaceMinerals1 = (100, 20, 31)
        population1 = 150000
        popEfficiency = 1000

        """
        # ------- update productionQ resources ------
        # this process is typically done in productionController
        colony2_resources = self.colony2_object.totalResources
        self.colony2_object.productionQ.resources = colony2_resources
        #--------------------------------------------


        quantity1 = 5
        materials1 = [20, 5, 10, 30]

        quantity_result1, materials_result1 = self.colony2_object.productionQ.buildLimit(quantity1, materials1)

        assert_equal(quantity_result1, 3)       
        assert_equal(materials_result1, [60, 15, 30, 90])

        


    def test_productionObjectVariables(self):
        print(self.target_colony_obj.planet.ID)
        print("%s:%s" % (self.target_colony_obj.planet.owner, self.target_colony_obj.planet.name))
        print(self.player.designs.currentShips.keys())
        #assert_true(False)



    def test_Add_RemoveItemFromQ(self):
        pass


    def test_controller(self):
        """ 
        beginning test. ProductionController goes through each item and 

        """
        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                self.colony2_name:
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "mines"}, 
                                            "entryID2" : {"quantity": 10, "productionID": "factories"},
                                            "entryID4" : {"quantity": 455, "productionID": "mines"},
                                            "entryID5" : {"quantity": 1, "productionID": "factories"},
                                            "entryID6" : {"quantity": 4, "productionID": "mines"}                                              
                                            }

                    }

                }
            }

        processProductionQ(xfileSetup_PQ_v1, self.player)

        pass

    def test_validateTargetPlayerSetup(self):
        """
        Tests that target player used for all other tests has the correct inital
        values. That all the pieces needed to test is captured and correct. 
        Individual tests may alter the standard but this should be the standard.

        """

        pass




    def test_entryController_produce_Mine_one(self):
        """
        entry controller should result in 1 mine value from entry controller
        """


        #colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                self.colony2_name:
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "mines"}, 
                                            "entryID2" : {"quantity": 10, "productionID": "factories"},
                                            "entryID4" : {"quantity": 455, "productionID": "mines"},
                                            "entryID5" : {"quantity": 1, "productionID": "factories"},
                                            "entryID6" : {"quantity": 4, "productionID": "mines"}                                              
                                            }

                    }

                }
            }

        pass

    def test_producePlanetUpgrades_Mine_one(self):
        """
        producePlanetUpgrades should be prompted to produce 1 mine on the 
        appropriate colony. 
        """
        pass



    def test_entryController_produce_Mine_Max(self):
        """
        the max planetary mines should be produced. Max = maximum mines that a 
        player can place on a planet.

        """
        pass

    def test_producePlanetUpgrades_Mine_Max(self):
        """
        producePlanetUpgrades the max planetary mines should be produced. Max = maximum mines that a 
        player can place on a planet.
        """
        pass

    def test_entryController_produce_Mine_TooMany(self):
        """
        The entry controller should handle the case of Too Many mines being requested.
        More then the player Mine cap on the planet

        """
        pass

    def test_producePlanetUpgrades_Mine_TooMany(self):
        """
        producePlanetUpgrades should produce the number of mines sent to it. The 
        Entry Controller should handle the problem of too many mines.
        """
        pass



