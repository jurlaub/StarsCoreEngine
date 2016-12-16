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



        #--------- set productionID and typeID -------------
        #  from ProductionQ.itemType
        self.productionID_Defenses = "Defenses"
        self.productionID_Mines = "Mines"
        self.productionID_Factories = "Factories"
        self.productionID_Minerals = "Minerals"
        self.productionID_Terraform = "Terraform"
        self.productionID_Scanner = "Scanner"
        self.productionID_Minerals = "Minerals"
        self.productionID_Ship = "Ship"
        self.productionID_Starbase = "Starbase"
        self.productionID_Special = "Special"




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
                                "productionID": TestProductionQ.productionID_Mines
                                }, 
                            "entryID2" : {
                                "quantity": 5, 
                                "productionID": TestProductionQ.productionID_Factories} }
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
                                "productionID": TestProductionQ.productionID_Mines
                                }, 
                            "entryID2" : 
                                {
                                "quantity": 10, 
                                "productionID": TestProductionQ.productionID_Factories
                                },
                            "entryID4" : 
                                {
                                "quantity": 455, 
                                "productionID": TestProductionQ.productionID_Mines
                                }                 
                            }
                    }

                }
            }
        
        # set a number of variables to the same value - so they can be reused
        self.surfaceMinerals1 = [100, 20, 31]
        self.population1 = 150000
        self.popEfficiency = 1000

        # ----- Set Colony 2 items
        #self.colony2_object.planet.addSurfaceMinerals(surfaceMinerals1)
        self.colony2_object.planet.surfaceIron = self.surfaceMinerals1[0]
        self.colony2_object.planet.surfaceBor = self.surfaceMinerals1[1]
        self.colony2_object.planet.surfaceGerm = self.surfaceMinerals1[2]

        self.colony2_object.population = self.population1
        self.colony2_object.calcTotalResources(self.popEfficiency)



        # ---- set HW items
        self.target_colony_obj.planet.surfaceIron = self.surfaceMinerals1[0]
        self.target_colony_obj.planet.surfaceBor = self.surfaceMinerals1[1]
        self.target_colony_obj.planet.surfaceGerm = self.surfaceMinerals1[2]

        self.target_colony_obj.population = self.population1
        self.target_colony_obj.calcTotalResources(self.popEfficiency)

        


        # ----------  set / reset target_colony productionQ --------
        self.target_colony_obj.productionQ.productionOrder = []
        self.target_colony_obj.productionQ.productionItems = {}
        #self.target_colony_obj.productionQ.test_ResourcesConsumed = 0




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
        self.target_colony_obj.planet.mines = 0
        self.target_colony_obj.planet.factories = 10


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

    def test_SplitEntryIntoTwo_multi(self):
        """
        need:
            ProductionQ
            entry in Q with more then 1 entry
            entry with quantity = 2+
            entry with quantity = 2 and work done
            entry wiht quantity 1
        """
        tmpMaterials = [3, 1, 5, 4]
        targetQuantity = 3

        colonyHW = self.target_colony_obj.productionQ
        assert_true(colonyHW)

        # 2nd colony - sanity check Pre-first call
        assert_equal(colonyHW.productionOrder, [])
        assert_equal(colonyHW.productionItems, {}) 

        processProductionQ(self.testQ, self.player)

        assert_equal(len(colonyHW.productionOrder), 3)
        assert_equal(len(colonyHW.productionItems), 3)

        currentEntry = colonyHW.productionOrder[0]
        
        colonyHW.productionItems[currentEntry]["quantity"] = targetQuantity
        colonyHW.productionItems[currentEntry]["materialsUsed"] = tmpMaterials

        colonyHW.splitEntryIntoTwo(currentEntry)

        assert_equal(len(colonyHW.productionOrder), 4)
        assert_equal(len(colonyHW.productionItems), 4)
        #print(colonyHW.productionOrder)

        assert_equal(currentEntry, colonyHW.productionOrder[1])

        splitEntry_name = colonyHW.productionOrder[0]
        splitEntry_obj = colonyHW.productionItems[splitEntry_name]
        assert_equal(splitEntry_obj["quantity"], 1)
        assert_equal(splitEntry_obj["materialsUsed"], tmpMaterials)

        # print("currentEntry(%s)(q:%d):%s :: splitEntry_obj(%s)(q:%d): %s" % (currentEntry, colonyHW.productionItems[currentEntry]["quantity"], 
        #                                                                 colonyHW.productionItems[currentEntry]["materialsUsed"],
        #                                                                  splitEntry_name, colonyHW.productionItems[splitEntry_name]["quantity"],
        #                                                                  colonyHW.productionItems[splitEntry_name]["materialsUsed"]))

        assert_equal(colonyHW.productionItems[currentEntry]["quantity"], targetQuantity - 1)
        assert_equal(colonyHW.productionItems[currentEntry]["materialsUsed"], [0, 0, 0, 0])

    def test_SplitEntryIntoTwo_one(self):
        """
        need:
            ProductionQ
            entry in Q with more then 1 entry
            entry with quantity = 2+
            entry with quantity = 2 and work done
            entry wiht quantity 1
        """
        tmpMaterials = [3, 1, 5, 4]
        targetQuantity = 1

        colonyHW = self.target_colony_obj.productionQ
        assert_true(colonyHW)

        # 2nd colony - sanity check Pre-first call
        assert_equal(colonyHW.productionOrder, [])
        assert_equal(colonyHW.productionItems, {}) 

        processProductionQ(self.testQ, self.player)
        assert_equal(len(colonyHW.productionOrder), 3)
        assert_equal(len(colonyHW.productionItems), 3)

        currentEntry = colonyHW.productionOrder[0]
        
        colonyHW.productionItems[currentEntry]["quantity"] = targetQuantity
        colonyHW.productionItems[currentEntry]["materialsUsed"] = tmpMaterials

        colonyHW.splitEntryIntoTwo(currentEntry)

        assert_equal(len(colonyHW.productionOrder), 3)
        assert_equal(len(colonyHW.productionItems), 3)
        #print(colonyHW.productionOrder)

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



    """ 
        EntryController Tests:

        Correct
            +quantity = 1,  correct resources consumed, correct BuildEntry & correct consumeMaterials
            +quantity = 1 w/ partially produced entry. complete using remaining resources & same as above

            +quantity = 150, produce all

            +quantity = 150(147), same as above --> with remainder quantity = 3
            quantity = 2+ w/ a partially produced entry --> produce only 1 & reset materialsUsed + reduce quantity

            quantity = 1 cannot complete entry but can partially production
            quantity = 2+ cannot complete entry but can partially production

            only partially produce an item (no complete item produced) (not a test of proportional method)


        Error
            quantity = 0 ==> nothing produced, no materials updated, entry finishedForTurn = True



    """

    def test_entryController_quantity1(self):
        """
        entryController:
            +quantity = 1,  correct resources consumed, correct BuildEntry & correct consumeMaterials

        """
        tmpQuantityA = 1
        tmpQuantityB = 5
        tmpID = "Defenses"

        tmpItemType = "Defenses" 

        testQ1 = {"ProductionQ" : 
                {
                self.target_colony_name : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { 
                            "entryID1" : {
                                "quantity": tmpQuantityA, 
                                "productionID": tmpID
                                }, 
                            "entryID2" : {
                                "quantity": tmpQuantityB, 
                                "productionID": tmpID} }
                    }

                }
            }

        targetItemCosts = [8, 11, 1, 30]
        #colonyResources = 100


        colonyHW = self.target_colony_obj.productionQ
        #colonyHW.resources = colonyResources


        assert_true(colonyHW)


        #   sanity check 
        assert_equal(colonyHW.productionOrder, [])
        assert_equal(colonyHW.productionItems, {}) 

        # sanity check on world surface minerals and production
        colonySurfaceMinerals = colonyHW.colony.planet.getSurfaceMinerals()
        assert_equal(colonySurfaceMinerals, self.surfaceMinerals1)

        # ---- adds testQ1 to colonyHW's productionQ - imitates an xfile --- 
        processProductionQ(testQ1, self.player)
        assert_equal(len(colonyHW.productionOrder), 2)
        assert_equal(len(colonyHW.productionItems), 2)

        currentEntry = colonyHW.productionOrder[0]

        colonyHW.updateProductionQResources() # typically handled in productionController()



        colonyHW.entryController(currentEntry, targetItemCosts)



        print("entryController - test: itemType is using hardcoded values and requires update")
        print("entryController - test: buildEntry is using hardcoded values and requires update")

        print("%s: %d pop; %d resources %s" % (colonyHW.colony.planet.name, colonyHW.colony.population, colonyHW.colony.totalResources, colonyHW.colony.planet.getSurfaceMinerals() ))

        assert_equal(colonyHW.entrybuildtype, tmpItemType)
        assert_equal(colonyHW.entrybuildquantity, tmpQuantityA)

        surfaceMineralsAfterProduction = colonyHW.colony.planet.getSurfaceMinerals()
        assert_not_equal(colonySurfaceMinerals, surfaceMineralsAfterProduction)

        for i in range(0, len(surfaceMineralsAfterProduction)):
            tmpRemainingMin = colonySurfaceMinerals[i] - targetItemCosts[i]

            assert_equal(surfaceMineralsAfterProduction[i], tmpRemainingMin)

    def test_entryController_quantity150(self):
        """
        entryController:

        Correct
            quantity = 150, produce all

        """
        tmpQuantityA = 150
        tmpQuantityB = 5
        tmpID = "Factories"

        

        testQ1 = {"ProductionQ" : 
                {
                self.target_colony_name : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { 
                            "entryID1" : {
                                "quantity": tmpQuantityA, 
                                "productionID": tmpID
                                }, 
                            "entryID2" : {
                                "quantity": tmpQuantityB, 
                                "productionID": tmpID} }
                    }

                }
            }

        targetItemCosts = [2, 4, 0, 5]

        #Surface Minerals to produce 150
        # [300, 600, 0, 750] added to existing test target minerals [100, 20, 31]
        additionalSurfaceMinerals = [300, 600, 0]

        # colony Setup
        colonyHW = self.target_colony_obj.productionQ
        colonyHW.colony.planet.addSurfaceMinerals(additionalSurfaceMinerals)
        colonyHW.colony.population = colonyHW.colony.planetMaxPopulation    # for max population
        colonyHW.colony.calcTotalResources(self.popEfficiency)
        colonyHW.ExcludedFromResearch = True    # max number of resources for production

        assert_true(colonyHW)


        #   sanity check 
        assert_equal(colonyHW.productionOrder, [])
        assert_equal(colonyHW.productionItems, {}) 

        # sanity check on world surface minerals and production
        colonySurfaceMinerals = colonyHW.colony.planet.getSurfaceMinerals()

        for i in range(0, len(colonySurfaceMinerals)):
            
            tmpTotal = self.surfaceMinerals1[i] + additionalSurfaceMinerals[i]
            assert_equal(colonySurfaceMinerals[i], tmpTotal)



        # ---- adds testQ1 to colonyHW's productionQ - imitates an xfile --- 
        processProductionQ(testQ1, self.player)

        assert_equal(len(colonyHW.productionOrder), 2)
        assert_equal(len(colonyHW.productionItems), 2)


        currentEntry = colonyHW.productionOrder[0]
        
        colonyHW.updateProductionQResources() # typically handled in productionController()
        print(colonyHW.resources)
        assert_true(colonyHW.resources >= targetItemCosts[-1] * tmpQuantityA)   #resources should be more then suffiecient to cover all   


        colonyHW.entryController(currentEntry, targetItemCosts)



        # print("entryController - test: itemType is using hardcoded values and requires update")
        # print("entryController - test: buildEntry is using hardcoded values and requires update")

        print("%s: %d pop; %d resources %s" % (colonyHW.colony.planet.name, colonyHW.colony.population, colonyHW.colony.totalResources, colonyHW.colony.planet.getSurfaceMinerals() ))

        assert_equal(colonyHW.entrybuildtype, TestProductionQ.productionID_Factories)
        assert_equal(colonyHW.entrybuildquantity, tmpQuantityA)

        surfaceMineralsAfterProduction = colonyHW.colony.planet.getSurfaceMinerals()
        assert_not_equal(colonySurfaceMinerals, surfaceMineralsAfterProduction)


        for i in range(0, len(surfaceMineralsAfterProduction)):


            tmpRemainingMin = colonySurfaceMinerals[i] - (tmpQuantityA * targetItemCosts[i])
            assert_equal(surfaceMineralsAfterProduction[i], tmpRemainingMin)

    def test_entryController_quantityPartial1(self):
        """
        entryController:
            complete a partially produced entry. 
            quantity = 1 w/ partially produced entry. complete using remaining resources & same as above

        """

        tmpQuantityA = 1
        tmpQuantityB = 5
        tmpID = "Defenses"

        entry1 = "entryID1"

        #tmpItemType = "Default ItemType" 

        testQ1 = {"ProductionQ" : 
                {
                self.target_colony_name : 
                    {
                        "productionOrder" : [entry1, "entryID2" ],
                        "productionItems" : { 
                            entry1 : {
                                "quantity": tmpQuantityA, 
                                "productionID": tmpID
                                }, 
                            "entryID2" : {
                                "quantity": tmpQuantityB, 
                                "productionID": tmpID} }
                    }

                }
            }

        targetPartialMaterialsUsed = [15, 135, 4, 129]

        targetItemCosts = [40, 492, 30, 510]
        additionalSurfaceMinerals = [300, 600, 0]

        # colony Setup
        colonyHW = self.target_colony_obj.productionQ
        colonyHW.colony.planet.addSurfaceMinerals(additionalSurfaceMinerals)
        colonyHW.colony.population = colonyHW.colony.planetMaxPopulation    # for max population
        colonyHW.colony.calcTotalResources(self.popEfficiency)
        colonyHW.ExcludedFromResearch = True    # max number of resources for production

        assert_true(colonyHW)


        #   sanity check 
        assert_equal(colonyHW.productionOrder, [])
        assert_equal(colonyHW.productionItems, {}) 

        # sanity check on world surface minerals and production
        colonySurfaceMinerals = colonyHW.colony.planet.getSurfaceMinerals()

        for i in range(0, len(colonySurfaceMinerals)):
            
            tmpTotal = self.surfaceMinerals1[i] + additionalSurfaceMinerals[i]
            assert_equal(colonySurfaceMinerals[i], tmpTotal)



        # ---- adds testQ1 to colonyHW's productionQ - imitates an xfile --- 
        processProductionQ(testQ1, self.player)

        assert_equal(len(colonyHW.productionOrder), 2)
        assert_equal(len(colonyHW.productionItems), 2)

        colonyHW.productionItems[entry1]["materialsUsed"] = targetPartialMaterialsUsed
        assert_equal(colonyHW.productionItems[entry1]["materialsUsed"], targetPartialMaterialsUsed)


        currentEntry = entry1
        
        colonyHW.updateProductionQResources() # typically handled in productionController()
        print(colonyHW.resources)
        assert_true(colonyHW.resources >= targetItemCosts[-1] * tmpQuantityA)   #resources should be more then suffiecient to cover all   


        colonyHW.entryController(currentEntry, targetItemCosts)



        # print("entryController - test: itemType is using hardcoded values and requires update")
        # print("entryController - test: buildEntry is using hardcoded values and requires update")

        print("%s: %d pop; %d resources %s" % (colonyHW.colony.planet.name, colonyHW.colony.population, colonyHW.colony.totalResources, colonyHW.colony.planet.getSurfaceMinerals() ))

        assert_equal(colonyHW.entrybuildtype, TestProductionQ.productionID_Defenses)
        assert_equal(colonyHW.entrybuildquantity, tmpQuantityA)

        surfaceMineralsAfterProduction = colonyHW.colony.planet.getSurfaceMinerals()
        assert_not_equal(colonySurfaceMinerals, surfaceMineralsAfterProduction)

        # check that the correct ammount of resources were removed.
        for i in range(0, len(surfaceMineralsAfterProduction)):

            tmpRemainingMin = colonySurfaceMinerals[i] - ((tmpQuantityA * targetItemCosts[i]) -targetPartialMaterialsUsed[i])
            assert_equal(surfaceMineralsAfterProduction[i], tmpRemainingMin)

    def test_entryController_quantityPartial2(self):
        """
        entryController:
            complete a partially produced entry. 
            quantity = 2 w/ partially produced entry. complete quantity 1 using remaining resources & same as above

        """

        tmpQuantityA = 2
        tmpQuantityB = 5
        tmpID = "Factories"

        entry1 = "entryID1"

        #tmpItemType = "Default ItemType"

        testQ1 = {"ProductionQ" : 
                {
                self.target_colony_name : 
                    {
                        "productionOrder" : [entry1, "entryID2" ],
                        "productionItems" : { 
                            entry1 : {
                                "quantity": tmpQuantityA, 
                                "productionID": tmpID
                                }, 
                            "entryID2" : {
                                "quantity": tmpQuantityB, 
                                "productionID": tmpID} }
                    }

                }
            }

        expectedBuildQuantity = 1
        targetItemCosts = [72, 35, 12, 50]
        targetPartialMaterialsUsed = [10, 15, 4, 10]
        expectedUsedMaterials = [((targetItemCosts[i] - targetPartialMaterialsUsed[i]) * expectedBuildQuantity) for i in range(0, len(targetItemCosts))]


        #Surface Minerals to produce 147
        # [1617, 588, 147, 735] added to existing test target minerals [100, 20, 31]
        additionalSurfaceMinerals = [0, 0, 0]
        

        # colony Setup
        colonyHW = self.target_colony_obj.productionQ
        colonyHW.colony.planet.addSurfaceMinerals(additionalSurfaceMinerals)
        colonyHW.colony.population = colonyHW.colony.planetMaxPopulation    # for max population
        colonyHW.colony.calcTotalResources(self.popEfficiency)
        colonyHW.ExcludedFromResearch = True    # max number of resources for production

        assert_true(colonyHW)


        #   sanity check 
        assert_equal(colonyHW.productionOrder, [])
        assert_equal(colonyHW.productionItems, {}) 

        # sanity check on world surface minerals and production
        colonySurfaceMinerals = colonyHW.colony.planet.getSurfaceMinerals()
        print("Beginning Surface Materials: %s" % colonySurfaceMinerals)

        for i in range(0, len(colonySurfaceMinerals)):
            
            tmpTotal = self.surfaceMinerals1[i] + additionalSurfaceMinerals[i]
            assert_equal(colonySurfaceMinerals[i], tmpTotal)




        # ---- adds testQ1 to colonyHW's productionQ - imitates an xfile --- 
        processProductionQ(testQ1, self.player)

        assert_equal(len(colonyHW.productionOrder), 2)
        assert_equal(len(colonyHW.productionItems), 2)

        colonyHW.productionItems[entry1]["materialsUsed"] = targetPartialMaterialsUsed
        assert_equal(colonyHW.productionItems[entry1]["materialsUsed"], targetPartialMaterialsUsed)


        currentEntry = entry1
        
        colonyHW.updateProductionQResources() # typically handled in productionController()
        print(colonyHW.resources)
        assert_true(colonyHW.resources >= targetItemCosts[-1] * tmpQuantityA)   #resources should be more then suffiecient to cover all   


        colonyHW.entryController(currentEntry, targetItemCosts)



        # print("entryController - test: itemType is using hardcoded values and requires update")
        # print("entryController - test: buildEntry is using hardcoded values and requires update")

        print("%s: %d pop; %d resources %s" % (colonyHW.colony.planet.name, colonyHW.colony.population, colonyHW.colony.totalResources, colonyHW.colony.planet.getSurfaceMinerals() ))

        assert_equal(colonyHW.entrybuildtype, TestProductionQ.productionID_Factories)
        assert_equal(colonyHW.entrybuildquantity, expectedBuildQuantity)

        surfaceMineralsAfterProduction = colonyHW.colony.planet.getSurfaceMinerals()
        assert_not_equal(colonySurfaceMinerals, surfaceMineralsAfterProduction)

        # check that the correct ammount of resources were removed.
        for i in range(0, len(surfaceMineralsAfterProduction)):

            tmpRemainingMin = colonySurfaceMinerals[i] - expectedUsedMaterials[i]          
            assert_equal(surfaceMineralsAfterProduction[i], tmpRemainingMin)


 
        assert_equal(len(colonyHW.productionOrder), 2)
        assert_equal(len(colonyHW.productionItems), 2) 

        assert_equal(colonyHW.productionItems[entry1]["quantity"], tmpQuantityA - expectedBuildQuantity)
        assert_equal(colonyHW.productionItems[entry1]["materialsUsed"], [0, 0, 0, 0])
        # print("%s" % colonyHW.productionItems[entry1]["materialsUsed"])
        # assert_true(False)





    def test_entryController_remainder_quantity_147of150(self):
        """
        entryController:

        Correct
            quantity = 147, same as above --> with remainder ( entryController does not provide a remainder)

        """
        tmpQuantityA = 150
        tmpQuantityB = 5
        tmpID = "Defenses"

        entry1 = "entryID1"

        # tmpItemType = "Default ItemType" 

        testQ1 = {"ProductionQ" : 
                {
                self.target_colony_name : 
                    {
                        "productionOrder" : [entry1, "entryID2" ],
                        "productionItems" : { 
                            entry1 : {
                                "quantity": tmpQuantityA, 
                                "productionID": tmpID
                                }, 
                            "entryID2" : {
                                "quantity": tmpQuantityB, 
                                "productionID": tmpID} }
                    }

                }
            }

        targetItemCosts = [11, 4, 1, 5]

        #Surface Minerals to produce 147
        # [1617, 588, 147, 735] added to existing test target minerals [100, 20, 31]
        additionalSurfaceMinerals = [1517, 568, 116]
        expectedBuildQuantity = 147

        # colony Setup
        colonyHW = self.target_colony_obj.productionQ
        colonyHW.colony.planet.addSurfaceMinerals(additionalSurfaceMinerals)
        colonyHW.colony.population = colonyHW.colony.planetMaxPopulation    # for max population
        colonyHW.colony.calcTotalResources(self.popEfficiency)
        colonyHW.ExcludedFromResearch = True    # max number of resources for production

        assert_true(colonyHW)


        #   sanity check 
        assert_equal(colonyHW.productionOrder, [])
        assert_equal(colonyHW.productionItems, {}) 

        # sanity check on world surface minerals and production
        colonySurfaceMinerals = colonyHW.colony.planet.getSurfaceMinerals()

        for i in range(0, len(colonySurfaceMinerals)):
            
            tmpTotal = self.surfaceMinerals1[i] + additionalSurfaceMinerals[i]
            assert_equal(colonySurfaceMinerals[i], tmpTotal)



        # ---- adds testQ1 to colonyHW's productionQ - imitates an xfile --- 
        processProductionQ(testQ1, self.player)

        assert_equal(len(colonyHW.productionOrder), 2)
        assert_equal(len(colonyHW.productionItems), 2)


        currentEntry = entry1
        
        colonyHW.updateProductionQResources() # typically handled in productionController()
        print(colonyHW.resources)
        assert_true(colonyHW.resources >= targetItemCosts[-1] * tmpQuantityA)   #resources should be more then suffiecient to cover all   


        colonyHW.entryController(currentEntry, targetItemCosts)



        # print("entryController - test: itemType is using hardcoded values and requires update")
        # print("entryController - test: buildEntry is using hardcoded values and requires update")

        print("%s: %d pop; %d resources %s" % (colonyHW.colony.planet.name, colonyHW.colony.population, colonyHW.colony.totalResources, colonyHW.colony.planet.getSurfaceMinerals() ))

        assert_equal(colonyHW.entrybuildtype, TestProductionQ.productionID_Defenses)
        assert_equal(colonyHW.entrybuildquantity, expectedBuildQuantity)

        surfaceMineralsAfterProduction = colonyHW.colony.planet.getSurfaceMinerals()
        assert_not_equal(colonySurfaceMinerals, surfaceMineralsAfterProduction)


        for i in range(0, len(surfaceMineralsAfterProduction)):


            tmpRemainingMin = colonySurfaceMinerals[i] - (expectedBuildQuantity * targetItemCosts[i])
            assert_equal(surfaceMineralsAfterProduction[i], tmpRemainingMin)

 
        assert_equal(len(colonyHW.productionOrder), 2)
        assert_equal(len(colonyHW.productionItems), 2) 

        assert_equal(colonyHW.productionItems[entry1]["quantity"], tmpQuantityA - expectedBuildQuantity)
        # print("%s" % colonyHW.productionItems[entry1]["materialsUsed"])
        # assert_true(False)

    def test_productionObjectVariables(self):
        print(self.target_colony_obj.planet.ID)
        print("%s:%s" % (self.target_colony_obj.planet.owner, self.target_colony_obj.planet.name))
        print(self.player.designs.currentShips.keys())
        #assert_true(False)



    def test_Add_RemoveItemFromQ(self):
        #assert_true(False)
        pass

    def test_controller(self):
        """ 
        beginning test. ProductionController goes through each item and 

        """


        #assert_true(False)
        pass

    def test_validateTargetPlayerSetup(self):
        """
        Tests that target player used for all other tests has the correct inital
        values. That all the pieces needed to test is captured and correct. 
        Individual tests may alter the standard but this should be the standard.

        """

        #assert_true(False)
        pass




    def test_entryController_produce_Mine_one(self):
        """
        entry controller should result in 1 mine value from entry controller due
        to user requesting the value.

        """

        entry1 = "entryID1"
        entryType1 = TestProductionQ.productionID_Mines
        

        testQ1 = {"ProductionQ" : 
                {
                self.target_colony_name:
                    {
                        "productionOrder" : ["entryID4", entry1, "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { entry1 : {"quantity": 1, "productionID": entryType1 }, 
                                            "entryID2" : {"quantity": 10, "productionID": "Factories"},
                                            "entryID4" : {"quantity": 455, "productionID": "Mines"},
                                            "entryID5" : {"quantity": 1, "productionID": "Factories"},
                                            "entryID6" : {"quantity": 4, "productionID": "Mines"}                                              
                                            }

                    }

                }
            }
        targetItemCosts = [0, 0, 0, int(self.player.raceData.mineCost)]

        colonyHW = self.target_colony_obj.productionQ

        assert_equal(len(colonyHW.productionOrder), 0)
        assert_equal(len(colonyHW.productionItems), 0)

        processProductionQ(testQ1, self.player)

        assert_equal(len(colonyHW.productionOrder), 5)
        assert_equal(len(colonyHW.productionItems), 5)


        currentEntry = entry1
        
        colonyHW.updateProductionQResources() # typically handled in productionController()

        colonyHW.entryController(currentEntry, targetItemCosts)


        assert_equal(colonyHW.entrybuildtype, entryType1)
        assert_equal(colonyHW.entrybuildquantity, 1)


    def test_producePlanetUpgrades_Mine_one(self):
        """
        producePlanetUpgrades should be prompted to produce 1 mine on the 
        appropriate colony. 
        """
        entry1 = "entryID1"
        entryType1 = TestProductionQ.productionID_Mines
        produceOne = 1

        testQ1 = {"ProductionQ" : 
                {
                self.target_colony_name:
                    {
                        "productionOrder" : [ entry1 ],
                        "productionItems" : { entry1 : {"quantity": produceOne, "productionID": entryType1 }                                             
                                            }

                    }

                }
            }


        mineResourceCost = int(self.player.raceData.mineCost)
        targetItemCosts = [0, 0, 0, mineResourceCost]

        colonyHW = self.target_colony_obj.productionQ
        assert_equal(len(colonyHW.productionItems), 0)
        print("ProductionQ.test_ResourcesConsumed: %d" %  colonyHW.test_ResourcesConsumed)

        # test the original state of mines
        minesOnHW = self.target_colony_obj.planet.mines
        
        print("TestProductionQ.test_producePlanetUpgrades_Mine_one() HARDCODED expects HW has 0 mines. Will need to change to be dynamic, current number of mines: %d" % minesOnHW)
        assert_true(self.target_colony_obj.planet.mines == 0)  # should not be any mines on HW


        processProductionQ(testQ1, self.player)

        assert_equal(len(colonyHW.productionOrder), 1)
        assert_equal(len(colonyHW.productionItems), 1)


        # colony has produced items in productionQ
        colonyHW.productionController()


        # what was produced on the colony
        assert_true(self.target_colony_obj.planet.mines == (minesOnHW + 1)) #only one additional mine should be built


        # did the appropriate resources be removed?

        assert_equal(mineResourceCost, colonyHW.test_ResourcesConsumed)



    def test_producePlanetUpgrades_Factory_one(self):
        """
        test_producePlanetUpgrades_Factory_one should be prompted to produce 1 factory on the 
        appropriate colony. 
        """
        entry1 = "entryID1"
        entryType1 = TestProductionQ.productionID_Factories
        produceOne = 1

        testQ1 = {"ProductionQ" : 
                {
                self.target_colony_name:
                    {
                        "productionOrder" : [ entry1 ],
                        "productionItems" : { entry1 : {"quantity": produceOne, "productionID": entryType1 }                                             
                                            }

                    }

                }
            }

        itemResourceCosts = int(self.player.raceData.factoryCost)
        germCosts = 4 if not self.player.raceData.factoryGermCost else 3 
        targetItemCosts = [0, 0, germCosts, itemResourceCosts]

        colonyHW = self.target_colony_obj.productionQ
        assert_equal(len(colonyHW.productionItems), 0)

        print("ProductionQ.test_ResourcesConsumed: %d" %  colonyHW.test_ResourcesConsumed)

        itemsOnHW = self.target_colony_obj.planet.factories
        print("factories on planet: %d" % (itemsOnHW))
        assert_true(self.target_colony_obj.planet.factories == 10) 

        processProductionQ(testQ1, self.player)

        assert_equal(len(colonyHW.productionOrder), 1)
        assert_equal(len(colonyHW.productionItems), 1)

        colonyHW.productionController()

        assert_true(self.target_colony_obj.planet.factories == (itemsOnHW + 1))

        assert_equal(itemResourceCosts, colonyHW.test_ResourcesConsumed)


    def test_produce_Mine_Max_Per_Turn(self):
        """
        the most mines that can be produced should be limited by resources. 
        (another function should test for planetary max)

        """
        entry1 = "entryID1"
        entryType1 = TestProductionQ.productionID_Mines
        produceOne = 700
        minesProducedInTest = 16 #expected number of mines produced due to resources available: 160 and mineCost: 10

        testQ1 = {"ProductionQ" : 
                {
                self.target_colony_name:
                    {
                        "productionOrder" : [ entry1 ],
                        "productionItems" : { entry1 : {"quantity": produceOne, "productionID": entryType1 }                                             
                                            }

                    }

                }
            }


        mineResourceCost = int(self.player.raceData.mineCost)
        targetItemCosts = [0, 0, 0, mineResourceCost]

        colonyHW = self.target_colony_obj.productionQ
        assert_equal(len(colonyHW.productionItems), 0)
        print("ProductionQ.test_ResourcesConsumed: %d" %  colonyHW.test_ResourcesConsumed)

        # test the original state of mines
        minesOnHW = self.target_colony_obj.planet.mines
        
        print("TestProductionQ.test_producePlanetUpgrades_Mine_one() HARDCODED expects HW has 0 mines. Will need to change to be dynamic, current number of mines: %d" % minesOnHW)
        assert_true(self.target_colony_obj.planet.mines == 0)  # should not be any mines on HW


        processProductionQ(testQ1, self.player)

        assert_equal(len(colonyHW.productionOrder), 1)
        assert_equal(len(colonyHW.productionItems), 1)


        # colony has produced items in productionQ
        colonyHW.productionController()



        # what was produced on the colony
        assert_true(self.target_colony_obj.planet.mines == (minesOnHW + minesProducedInTest)) #only one additional mine should be built


        # did the appropriate resources be removed?

        assert_equal(mineResourceCost * minesProducedInTest, colonyHW.test_ResourcesConsumed)

    def test_producePlanetUpgrades_Mine_Max(self):
        """
        producePlanetUpgrades the max planetary mines should be produced. Max = maximum mines that a 
        player can place on a planet.
        """
        #assert_true(False)
        pass

    def test_entryController_produce_Mine_TooMany(self):
        """
        The entry controller should handle the case of Too Many mines being requested.
        More then the player Mine cap on the planet

        """
        #assert_true(False)
        pass

    def test_producePlanetUpgrades_Mine_TooMany(self):
        """
        producePlanetUpgrades should produce the number of mines sent to it. The 
        Entry Controller should handle the problem of too many mines.
        """
        #assert_true(False)
        pass


    def test_targetItemCosts_Mines(self):

        player0 = TestProductionQ.player
        targetItem = self.target_colony_obj.productionQ.targetItemCosts(TestProductionQ.productionID_Mines)
        
        expectedItemCosts = [0, 0, 0, player0.raceData.mineCost]
        assert_equal(targetItem, expectedItemCosts)


    def test_targetItemCosts_Factories(self):

        player0 = TestProductionQ.player
        targetItem = self.target_colony_obj.productionQ.targetItemCosts(TestProductionQ.productionID_Factories)
        
        germCost = 4 if not player0.raceData.factoryGermCost else 3  # germ cost for building a factory
        expectedItemCosts = [0, 0, germCost, player0.raceData.factoryCost] # total cost for a factory

        assert_equal(targetItem, expectedItemCosts)

    def test_targetItemCosts_Defenses(self):
        print("--TODO-- test_targetItemCosts_Defenses Resource Cost does not account for PRT/LRT")
        
        #account for PRT
        techItem = TestProductionQ.techTree["SDI"]
        # print("Defenses- iron: %d, bor: %d, germ: %d, resources:%d"%(techItem.iron, techItem.bor, techItem.germ, techItem.resources))
        expectedDefensesCosts = [techItem.iron, techItem.bor, techItem.germ, techItem.resources]

        targetItem = self.target_colony_obj.productionQ.targetItemCosts(TestProductionQ.productionID_Defenses)

        assert_equal(targetItem, expectedDefensesCosts)



    def test_targetItemCosts_Minerals(self):
        print("--TODO-- test_targetItemCosts_Minerals Mineral Resource Cost HARDCODED to 100 resources only")
        expectedItemCosts = [0, 0, 0, 100]
        
        targetItem = self.target_colony_obj.productionQ.targetItemCosts(TestProductionQ.productionID_Minerals)

        assert_equal(targetItem, expectedItemCosts)


    def test_targetItemCosts_Ship(self):
        print("--TODO-- test_targetItemCosts_Ship Ship Resource Cost HARDCODED -[41, 12, 34, 138]- This one is dynamic and requires extra effort")

        expectedItemCosts = [41, 12, 34, 138]
        
        targetItem = self.target_colony_obj.productionQ.targetItemCosts(TestProductionQ.productionID_Ship)

        assert_equal(targetItem, expectedItemCosts)



    def test_targetItemCosts_Starbase(self):
        print("--TODO-- test_targetItemCosts_Starbase Starbase Resource Cost HARDCODED -[71, 48, 34, 338]- This one is dynamic and requires extra effort")

        expectedItemCosts = [71, 48, 34, 338]
        
        targetItem = self.target_colony_obj.productionQ.targetItemCosts(TestProductionQ.productionID_Starbase)

        assert_equal(targetItem, expectedItemCosts)

        
    def test_targetItemCosts_Scanner(self):
        print("--TODO-- test_targetItemCosts_Scanner Resource Cost does not account for PRT/LRT")
        
        techItem = TestProductionQ.techTree["Viewer 50"]
        expectedItemCosts = [techItem.iron, techItem.bor, techItem.germ, techItem.resources]

        itemCosts = self.target_colony_obj.productionQ.targetItemCosts(TestProductionQ.productionID_Scanner)

        assert_equal(expectedItemCosts, itemCosts)


    def test_targetItemCosts_Terraform(self):
        print("--TODO-- test_targetItemCosts_Terraform Resource Cost does not account for PRT/LRT")

        #account for LRT 
        techItem = TestProductionQ.techTree["Gravity Terraform 7"]
        itemIron = 0 if techItem.iron == None else techItem.iron
        itemBor = 0 if techItem.bor == None else techItem.bor
        itemGerm = 0 if techItem.germ == None else techItem.germ
        expectedItemCosts = [itemIron, itemBor, itemGerm, techItem.resources]
        # print("test_itemCosts_Terraform - expectedItemCosts: %s" % expectedItemCosts)

        itemCosts = self.target_colony_obj.productionQ.targetItemCosts(TestProductionQ.productionID_Terraform)
        assert_equal(expectedItemCosts, itemCosts)



    def test_itemCosts_Mines(self):
        player0 = TestProductionQ.player
        expectedMineCosts = [0, 0, 0, player0.raceData.mineCost] # total cost for a mine

        # assert_equal(player0.raceData.mineCost, 10)

        # function in productionQ.py that calculates mine costs
        mineCosts = self.target_colony_obj.productionQ.itemCostsMines()
        assert_equal(mineCosts, expectedMineCosts)

        
    def test_itemCosts_Factory(self):
        player0 = TestProductionQ.player

        
        germCost = 4 if not player0.raceData.factoryGermCost else 3  # germ cost for building a factory
        expectedFactoryCosts = [0, 0, germCost, player0.raceData.factoryCost] # total cost for a factory

        #fuction in productionQ.py that calculates factory costs
        factoryCosts = self.target_colony_obj.productionQ.itemCostsFactories()

        assert_equal(factoryCosts, expectedFactoryCosts)


    def test_itemCosts_Defenses(self):
        print("--TODO-- test_itemCosts_Defenses Resource Cost does not account for PRT/LRT")

        #account for PRT
        techItem = TestProductionQ.techTree["SDI"]
        # print("Defenses- iron: %d, bor: %d, germ: %d, resources:%d"%(techItem.iron, techItem.bor, techItem.germ, techItem.resources))
        expectedDefensesCosts = [techItem.iron, techItem.bor, techItem.germ, techItem.resources]

        itemCosts = self.target_colony_obj.productionQ.itemCostsDefenses()

        assert_equal(expectedDefensesCosts, itemCosts)


    def test_itemCosts_Terraform(self):
        print("--TODO-- test_itemCosts_Terraform Resource Cost does not account for PRT/LRT")

        #account for LRT 
        techItem = TestProductionQ.techTree["Gravity Terraform 7"]
        itemIron = 0 if techItem.iron == None else techItem.iron
        itemBor = 0 if techItem.bor == None else techItem.bor
        itemGerm = 0 if techItem.germ == None else techItem.germ
        expectedItemCosts = [itemIron, itemBor, itemGerm, techItem.resources]
        # print("test_itemCosts_Terraform - expectedItemCosts: %s" % expectedItemCosts)

        itemCosts = self.target_colony_obj.productionQ.itemCostsTerraform()
        assert_equal(expectedItemCosts, itemCosts)


    def test_itemCosts_Scanner(self):
        print("--TODO-- test_itemCosts_Scanner Resource Cost does not account for PRT/LRT")
       
        #account for PRT
        techItem = TestProductionQ.techTree["Viewer 50"]
        expectedItemCosts = [techItem.iron, techItem.bor, techItem.germ, techItem.resources]

        itemCosts = self.target_colony_obj.productionQ.itemCostsScanner()

        assert_equal(expectedItemCosts, itemCosts)



    def test_raceData_MaxMines_100GreenWorld(self):
        # Mine cap on a planet is a ratio of mines per 10,000 pop 
        expectedColonyValue = 100
        colonyValue = self.target_colony_obj.planetValue
        assert_equal(expectedColonyValue, colonyValue)


        maxMines = self.target_colony_obj.maxMinesOnColony()
        #colonyPopulation = self.target_colony_obj.population
        maxPopulation = 1000000
        print("test_raceData_MaxMines_100GreenWorld: HARDCODED maxPopulation: %d" % maxPopulation)
        minesOperatePer10000 = TestProductionQ.player.raceData.mineOperate
        
        calculatedMines = int((maxPopulation/10000) * minesOperatePer10000)
        assert_equal(maxMines, calculatedMines)
        

