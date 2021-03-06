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

"""
This file collects unit tests for game_xfile.py methods. 
game_xfile.py should declare the standrd for x files.
game_xfile.py should also be called from command line to validate an x file.

This file should validate the game_xfile.py validation. Essentially act as
a means of acceptance tests.




"""

import os

from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_not_in, assert_true, assert_false


from ..starscoreengine.game_xfile import *
from ..starscoreengine.game import Game
from ..starscoreengine.template import *
from ..starscoreengine.template_race import startingDesigns, startingShipDesignsCount, startingDesignsCount



class TestXFileTemplate(object):
    """ 
    validate game_xfile.py  xfile_TEMPLATE()

    """

    def setup(self):
        print("TestXFileTemplate: Setup")
        self.xfile = xfile_TEMPLATE()



    def teardown(self):
        print("TestXFileTemplate: Teardown")

    def test_PlayerValues(self):
        pass


class TestXFileController(object):

    # create xFileTestFile for class

    # teardown xFileTestFile 

    # TODO - move this class and test cases to ProductionQ


    def setup(self):
        print("TestXFileController: Setup")

        self.playerFileList = ['Wolfbane', 'Bunnybane']
        self.testGameName = 'xFileTestFile'
        self.playerXFile0 = 'xFileTestFile.x0'
        self.playerXFile1 = 'xFileTestFile.x1'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.game = Game(self.gameTemplate)
        self.player = self.game.players["player0"]



        # for kee, player in self.game.players.items():
        #     print("kee:%s :: player:%s:" % (kee, player.speciesName))

        #     for name, colony in player.colonies.items():
        #         print("PlanetKee:%s & PlanetID:%s & PlanetName:%s" % (name, colony.planet.ID, colony.planet.name))
        #         v = self.game.game_universe[0].planets[colony.planet.ID]
        #         print("universe kee: %s, planetID:%s, planetName:%s" % (colony.planet.ID, v.ID, v.name))
        #         print("owner:%s" % (colony.planet.owner))



        # print("player colonies:\n%s:%s\n%s:%s"%(self.game.players["player0"].speciesName, str(self.game.players["player0"].colonies.keys()), self.game.players["player1"].speciesName, str(self.game.players["player1"].colonies.keys())))

        # --------- productionQ grab planets --------
        self.target_colony = None       # HW
        for kee, each in self.player.colonies.items():
            # print("kee:%s; each.planet.ID: %s; keys(%s)" % (kee, each.planet.ID, self.player.colonies.keys()))
            # print("owner:%s; player:%s (%s)" % (each.planet.owner, self.player, str(self.game.players)))
            
            if each.planet.HW:
                self.target_colony = each.planet.ID
                break
            # else:
            #     print("Planet in colonies and not a HW. %s:%s" % (kee, each.planet.ID))
        
        assert_in(self.target_colony, self.player.colonies)

        self.newColony = []
        self.universePlanets = self.game.game_universe[0].planets

        # find planets == newColonyCount in universe without an owner
        newColonyCount = 2 
        for kee, obj in self.universePlanets.items():
            if len(self.newColony) > newColonyCount:
                break

            if not obj.owner and obj.HW == False:
                self.newColony.append(kee)

        # colonize planets that are identified in self.newColony list
        for each in self.newColony:
            self.player.colonizePlanet(self.universePlanets[each], 150000)






    def teardown(self):
        print("TestXFileController: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))


    def test_testForXFile0(self):
        fileName = self.playerXFile0

        print("Need xfile test file in ../StarsCoreEngine/%s:" % (self.testGameName + '.x0'))
        assert_true(os.path.isfile(fileName))
    
    def test_testForXFile1(self):
        fileName = self.playerXFile1

        print("xfile test file .x1 should not exist ../StarsCoreEngine/%s:" % (self.testGameName + '.x1'))
        assert_false(os.path.isfile(fileName))      






    def test_xfileController(self):
        """ tests overall method - unit tests for PlayerDesign etc. are in test_player.

        """

        self.game.year  = 2402        # match year specified in xFileTestFile.x0
        p0Key = 'player0'
        p0 = self.game.players[p0Key]


        # values prior to xFileController being called  = Baseline
        assert_true(p0.speciesName, self.playerFileList[0])
        #print("count designs:%s" % len(p0.designs.currentShips))
        beginningDesignsCount_withStarbases = startingDesignsCount()
        beginningDesignsCount = startingShipDesignsCount()
        assert_equal(len(p0.designs.currentShips), beginningDesignsCount)

        assert_true(beginningDesignsCount_withStarbases - beginningDesignsCount == 1) # one starbase design

        # uses values found in xfile_TEMPLATE
        xFileController(self.game)


        # values after to xFileController being called, 2 extra ship designs added
        assert_equal(len(p0.designs.currentShips), beginningDesignsCount + 2)





    def test_xfileController_Handles_IncorrectYear(self):
        self.game.year  = 2499

        xFileController(self.game)

        for player in self.game.players.values():
            m = player.xfilestatus

            assert_equal(len(m), 1)
            msg = m.pop()
            print("test: %s" % msg)
            assert_in(str(self.game.year), msg)
            # assert_in('Not current year', msg)      # omitted -> only .x0 file
            

    def test_xfileController_Handles_False_xfileName(self):
        falseGameName = 'ChillyOnWrongMountain'
        self.game.game_name = falseGameName

        xFileController(self.game)

        for player in self.game.players.values():
            m = player.xfilestatus

            assert_equal(len(m), 1)
            msg = m.pop()
            #print("test: %s" % msg)
            assert_in('file unable to load', msg)       

    def test_xfile_HasCorrectProductionQFormat(self):


        tmp_xfile = xfile_TEMPLATE()

        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile)

        assert_true(isValid)

    def test_xFile_ProductionQ_StructureIsValid_CorrectNumber(self):
        tmp_xfile_ProductionQ = {
        "ProductionQ" : 
            {
                "player.colonies.ID1" : 
                    { 
                        "productionOrder" : ["key1", "key2", "key3"],
                        "productionItems" : { }  
                    }

            }
            }

        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile_ProductionQ)
        assert_false(isValid)
        
    def test_xFile_ProductionQ_StructureIsValid_EmptyPlusContentsInQ(self):
        """
        test a mix of empty colony ProductionQ and Q with entries

        """
        tmp_xfile_ProductionQ = {
        "ProductionQ" : 
            {
                "test player.colonies.empty" : 
                    { 
                        "productionOrder" : [ ],
                        "productionItems" : { }  
                    },
                "test player.colonies.twoEntries" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "item1"}, "entryID2" : {"quantity": 5, "itemType": "item1"} }
                    },
                "test player.colonies.oneEntry" : 
                    {
                        "productionOrder" : [ "entryID2" ],
                        "productionItems" : { "entryID2" : {"quantity": 5, "itemType": "item1"}}
                    }

            }
            }
        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile_ProductionQ)
        assert_true(isValid)
        
    def test_xFile_ProductionQ_StructureIsValid_ValidItemValues(self):
        tmp_xfile_ProductionQ1 = {
        "ProductionQ" : 
            {

                "test correct colony Q" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "item1"}, "entryID2" : {"quantity": 34, "itemType": "item2"} }
                    }

            }
            }
        tmp_xfile_ProductionQ2 = {
        "ProductionQ" : 
            {

                "test error colony Q2" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "item1"}, "entryID2" : {} }
                    }

            }
            }
        tmp_xfile_ProductionQ3 = {
        "ProductionQ" : 
            {

                "test error colony Q3" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "item1"}, "entryID2" : {"quantity": 2} }
                    }

            }
            }
        tmp_xfile_ProductionQ4 = {
        "ProductionQ" : 
            {

                "test error colony Q4" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "item1"}, "entryID2" : {"itemType": "item1"} }
                    }

            }
            }
        tmp_xfile_ProductionQ5 = {
        "ProductionQ" : 
            {

                "test error colony Q5" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "item1", "CrazySauce" : "hello"}, "entryID2" : {"itemType": "item1"} }
                    }

            }
            }

        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile_ProductionQ1)
        assert_true(isValid) 

        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile_ProductionQ2) 
        assert_false(isValid)   

        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile_ProductionQ3) 
        assert_false(isValid) 

        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile_ProductionQ4) 
        assert_false(isValid) 

        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile_ProductionQ5) 
        assert_false(isValid) 

    def test_xFile_ProductionQ_StructureIsValid_ValidOrderItemEntries(self):
        tmp_xfile_ProductionQ1 = {
        "ProductionQ" : 
            {

                "test 'correct' tmp_xfile_ProductionQ1" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "item1"}, "entryID2" : {"quantity": 34, "itemType": "item2"} }
                    }

            }
            }

        tmp_xfile_ProductionQ2 = {
        "ProductionQ" : 
            {

                "test 'error' tmp_xfile_ProductionQ2" : 
                    {
                        "productionOrder" : ["ERROREntry", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "item1"}, "entryID2" : {"quantity": 34, "itemType": "item2"} }
                    }

            }
            }
        tmp_xfile_ProductionQ3 = {
        "ProductionQ" : 
            {

                "test 'error' tmp_xfile_ProductionQ3" : 
                    {
                        "productionOrder" : ["entryID1", "entryID1" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "item1"}, "entryID2" : {"quantity": 34, "itemType": "item2"} }
                    }

            }
            }
        
        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile_ProductionQ1)
        assert_true(isValid) 

        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile_ProductionQ2)
        assert_false(isValid) 

        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile_ProductionQ3)
        assert_false(isValid) 


    def test_xfileController_ProcessProductionQ_Correctly(self):
        """
        Input: xfile, playerObj
        Output: the player colonies ProductionQ's are updated with values.
        """
        #_____ setup _________________________
        # self.target_colony = None
        # for each in self.player.colonies.values():
        #     print("each: %s" % each.planet.ID)
        #     if each.planet.HW:
        #         self.target_colony = each.planet.ID
        #         break
        colony2 = self.newColony[0]

        xfileSetup_PQ = {"ProductionQ" : 
                {
                self.target_colony : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, "entryID2" : {"quantity": 10, "itemType": "factories"} }
                    },
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"} 
                                            }
                    }

                }
            }
        #______________________________

        assert_true(self.target_colony)
        target = self.player.colonies[self.target_colony].productionQ
        target2 = self.player.colonies[colony2].productionQ

        # HW
        assert_equal(target.productionOrder, [])
        assert_equal(target.productionItems, {}) 


        # 2nd colony
        assert_equal(target2.productionOrder, [])
        assert_equal(target2.productionItems, {}) 


        # only need to call 1 time
        processProductionQ(xfileSetup_PQ, self.player)      # process the ProductionQ


        # HW
        assert_equal(len(target.productionOrder), 2)
        assert_equal(target.productionOrder[1], "entryID2")

        assert_equal(len(target.productionItems), 2)
        assert_equal(target.productionItems["entryID1"]["itemType"], "mines")


        # 2nd colony
        assert_equal(len(target2.productionOrder), 3)
        assert_equal(target2.productionOrder[0], "entryID4")

        assert_equal(len(target2.productionItems), 3)
        assert_equal(target2.productionItems["entryID4"]["quantity"], 455)        



    def test_xfileController_ProcessProductionQ_CorrectlyDeleteItemsSetToZero(self):
        """
        Input: xfile, playerObj
        Output: Items with a quantity of zero are removed from the 
                productionOrder & productionItems
        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"} 
                                            }

                    }

                }
            }
        xfileSetup_PQ_v2 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : [ "entryID1", "entryID2" ],
                        "productionItems" : {  
                                            "entryID2" : {"quantity": 0, "itemType": "factories"}
                                            }
                    }

                }
            }
        xfileSetup_PQ_zero = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : [],
                        "productionItems" : {  }
                    }

                }
            }


        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # 2nd colony - sanity check Pre-first call
        assert_equal(target2.productionOrder, [])
        assert_equal(target2.productionItems, {}) 

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 3)
        assert_equal(len(target2.productionItems), len(target2.productionOrder))

        processProductionQ(xfileSetup_PQ_zero, self.player)

        assert_equal(len(target2.productionItems), 0)
        assert_equal(len(target2.productionOrder), 0)    

        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ  

        assert_equal(len(target2.productionItems), 3)
        assert_equal(len(target2.productionItems), len(target2.productionOrder))  

        assert_equal(target2.productionOrder[0], "entryID4")
        assert_equal(target2.productionOrder[1], "entryID1")
        assert_equal(target2.productionOrder[2], "entryID2")


        assert_equal(target2.productionItems["entryID4"]["quantity"], 455)
        assert_equal(target2.productionItems["entryID1"]["quantity"], 5)
        assert_equal(target2.productionItems["entryID2"]["quantity"], 10)


        # second call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_v2, self.player)      # process the ProductionQ      

        assert_equal(len(target2.productionItems), 1)
        assert_equal(len(target2.productionItems), len(target2.productionOrder)) 


        assert_equal(target2.productionOrder[0], "entryID1")
        assert_equal(target2.productionItems["entryID1"]["quantity"], 5)

        

    def test_xfileController_ProcessProductionQ_CorrectlySetItemsToZero(self):
        """
        Input: xfile, playerObj
        Output: existing items whose new quantity is Zero are set to Zero
                (i.e. user intentionally sets items to Zero)
        """

        colony2 = self.newColony[0] # name of a non-HW colony in player.colonies

        # start values
        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "DeleteME" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "DeleteME" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"} 
                                            }

                    }

                }
            }
        # "DeleteME" to be set to zero
        xfileSetup_PQ_v2 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "DeleteME" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "DeleteME" : {"quantity": 0, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"} 
                                            }

                    }

                }
            }

        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # 2nd colony - sanity check Pre-first call
        assert_equal(target2.productionOrder, [])
        assert_equal(target2.productionItems, {}) 

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 3)
        assert_equal(target2.productionOrder[2], "DeleteME")
        assert_equal(target2.productionItems["DeleteME"]["quantity"], 10)

        # second call -> to correctly set the values to zero
        processProductionQ(xfileSetup_PQ_v2, self.player)      # process the ProductionQ       
        
        # 2nd colony - test
        assert_equal(len(target2.productionItems), 2)
        assert_equal(len(target2.productionItems), len(target2.productionOrder))
        assert_not_in("DeleteME", target2.productionOrder)
        assert_not_in("DeleteME", target2.productionItems)
        #assert_equal(target2.productionOrder[2], "DeleteME")
        #assert_equal(target2.productionItems["DeleteME"]["quantity"], 0)

    

    def test_xfileController_ProcessProductionQ_CorrectlyDeleteItemsMissingFromOrder(self):
        """
        Input: xfile, playerObj
        Output: Items missing from productionOrder are set to Zero
        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }
        xfileSetup_PQ_v2 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID2", "entryID4", "entryID1" ],
                        "productionItems" : {  
                                            "entryID2" : {"quantity": 0, "itemType": "factories"}
                                            }
                    }

                }
            }

        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # 2nd colony - sanity check Pre-first call
        assert_equal(target2.productionOrder, [])
        assert_equal(target2.productionItems, {}) 

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(len(target2.productionItems), len(target2.productionOrder))

        assert_equal(target2.productionOrder[3], "entryID5")
        assert_equal(target2.productionOrder[4], "entryID6")
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionOrder[1], "entryID1")
        assert_equal(target2.productionOrder[0], "entryID4")
        assert_equal(target2.productionItems["entryID4"]["quantity"], 455)
        assert_equal(target2.productionItems["entryID5"]["quantity"], 1)
        assert_equal(target2.productionItems["entryID6"]["quantity"], 4)
        assert_equal(target2.productionItems["entryID1"]["quantity"], 5)

        # second call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_v2, self.player)      # process the ProductionQ       
        
        # 2nd colony - test
        assert_equal(len(target2.productionOrder), 2)
        assert_equal(len(target2.productionItems), 2)

        assert_not_in("entryID2", target2.productionOrder )
        assert_not_in("entryID2", target2.productionItems )

        assert_not_in("entryID5", target2.productionOrder )
        assert_not_in("entryID5", target2.productionItems )

        assert_not_in("entryID6", target2.productionOrder )
        assert_not_in("entryID6", target2.productionItems )



        assert_equal(target2.productionOrder[1], "entryID1")
        assert_equal(target2.productionOrder[0], "entryID4")


        assert_equal(target2.productionItems["entryID4"]["quantity"], 455)
        assert_equal(target2.productionItems["entryID1"]["quantity"], 5)

        #assert_true(False)



    def test_xfileController_ProcessProductionQ_CorrectlyDeleteItemsMissingFromOrder_complex(self):
        """
        Input: xfile, playerObj
        Output: Items missing from productionOrder are set to Zero
                need to test what happens if 2nd queue orders have removed items 
                from the original productionOrder but have added more

        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }
        xfileSetup_PQ_v2 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID12", "entryID4", \
                        "entryID13", "entryID14", "entryID15", "entryID16", \
                        "entryID17", "entryID18" ],
                        
                        "productionItems" : { "entryID12" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID13" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 300, "itemType": "mines"},
                                            "entryID14" : {"quantity": 2, "itemType": "factories"},
                                            "entryID15" : {"quantity": 3, "itemType": "mines"},
                                            "entryID16" : {"quantity": 5, "itemType": "mines"},
                                            "entryID17" : {"quantity": 8, "itemType": "factories"},
                                            "entryID18" : {"quantity": 13, "itemType": "mines"}                                               
                                            }
                    }

                }
            }

        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # 2nd colony - sanity check Pre-first call
        assert_equal(target2.productionOrder, [])
        assert_equal(target2.productionItems, {}) 

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(len(target2.productionItems), len(target2.productionOrder))


        assert_equal(target2.productionOrder[3], "entryID5")
        assert_equal(target2.productionOrder[4], "entryID6")
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionOrder[1], "entryID1")
        assert_equal(target2.productionOrder[0], "entryID4")
        assert_equal(target2.productionItems["entryID4"]["quantity"], 455)
        assert_equal(target2.productionItems["entryID5"]["quantity"], 1)
        assert_equal(target2.productionItems["entryID6"]["quantity"], 4)
        assert_equal(target2.productionItems["entryID1"]["quantity"], 5)




        # second call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_v2, self.player)      # process the ProductionQ       
        
        # 2nd colony - test
        assert_equal(len(target2.productionOrder), 8)
        assert_equal(len(target2.productionItems), 8)


        assert_equal(target2.productionOrder[0], "entryID12")
        assert_equal(target2.productionOrder[1], "entryID4")
        assert_equal(target2.productionOrder[2], "entryID13")
        assert_equal(target2.productionOrder[5], "entryID16")
        assert_equal(target2.productionOrder[7], "entryID18")
        assert_equal(target2.productionItems["entryID4"]["quantity"], 300)
        assert_equal(target2.productionItems["entryID18"]["quantity"], 13)
        assert_equal(target2.productionItems["entryID15"]["quantity"], 3)
        assert_equal(target2.productionItems["entryID17"]["quantity"], 8)

        assert_not_in("entryID5", target2.productionItems )
        assert_not_in("entryID6", target2.productionItems )
        assert_not_in("entryID1", target2.productionItems )
        assert_not_in("entryID2", target2.productionItems )



    def test_xfileController_ProcessProductionQ_CorrectlyReshuffleOrderItems(self):
        """
        Input: xfile, playerObj
        Output: Items in productionOrder are correctly readjusted
        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }
        xfileSetup_PQ_v2 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID1", "entryID2", "entryID4", "entryID6", "entryID5" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 23, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }
                    }

                }
            }

        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # 2nd colony - sanity check Pre-first call
        assert_equal(target2.productionOrder, [])
        assert_equal(target2.productionItems, {}) 

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(len(target2.productionItems), len(target2.productionOrder))

        assert_equal(target2.productionOrder[0], "entryID4")
        assert_equal(target2.productionOrder[1], "entryID1")
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionOrder[3], "entryID5")
        assert_equal(target2.productionOrder[4], "entryID6")

        assert_equal(target2.productionItems["entryID4"]["quantity"], 455)
        assert_equal(target2.productionItems["entryID5"]["quantity"], 1)
        assert_equal(target2.productionItems["entryID6"]["quantity"], 4)
        assert_equal(target2.productionItems["entryID1"]["quantity"], 5)

        # second call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_v2, self.player)      # process the ProductionQ      

        assert_equal(target2.productionOrder[0], "entryID1")
        assert_equal(target2.productionOrder[1], "entryID2")
        assert_equal(target2.productionOrder[2], "entryID4")
        assert_equal(target2.productionOrder[3], "entryID6")
        assert_equal(target2.productionOrder[4], "entryID5")

        assert_equal(target2.productionItems["entryID4"]["quantity"], 23)
        assert_equal(target2.productionItems["entryID5"]["quantity"], 1)
        assert_equal(target2.productionItems["entryID6"]["quantity"], 4)
        assert_equal(target2.productionItems["entryID1"]["quantity"], 5)


    def test_xfileController_ProcessProductionQ_CorrectlyAddItemsToQ(self):
        """
        Input: xfile, playerObj
        Output: Items are added correctly. 1 to end, 1 to middle
        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID2", "entryID5"  ],
                        "productionItems" : {  
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"}                                             
                                            }

                    }

                }
            }
        xfileSetup_PQ_v2 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }
                    }

                }
            }

        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # 2nd colony - sanity check Pre-first call
        assert_equal(target2.productionOrder, [])
        assert_equal(target2.productionItems, {}) 

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 3)
        assert_equal(len(target2.productionItems), len(target2.productionOrder))

        assert_equal(target2.productionOrder[0], "entryID4")
        assert_equal(target2.productionOrder[1], "entryID2")
        assert_equal(target2.productionOrder[2], "entryID5")


        assert_equal(target2.productionItems["entryID4"]["quantity"], 455)
        assert_equal(target2.productionItems["entryID2"]["quantity"], 10)
        assert_equal(target2.productionItems["entryID5"]["quantity"], 1)


        # second call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_v2, self.player)      # process the ProductionQ   

        assert_equal(len(target2.productionItems), 5)
        assert_equal(len(target2.productionItems), len(target2.productionOrder))

        assert_equal(target2.productionOrder[0], "entryID4")
        assert_equal(target2.productionOrder[1], "entryID1")
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionOrder[3], "entryID5")
        assert_equal(target2.productionOrder[4], "entryID6")

        assert_equal(target2.productionItems["entryID4"]["quantity"], 455)
        assert_equal(target2.productionItems["entryID2"]["quantity"], 10)
        assert_equal(target2.productionItems["entryID5"]["quantity"], 1)

        assert_equal(target2.productionItems["entryID6"]["quantity"], 4)
        assert_equal(target2.productionItems["entryID1"]["quantity"], 5)

 
    
    def test_xfileController_ProcessProductionQ_CorrectlyHandleUnexpected_Negative(self):
        """
        Input: xfile, playerObj
        Output: Items with negative values in XFile are correctly handled
                (i.e. set to 0)

        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }
        xfileSetup_PQ_negative = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : {  
                                            "entryID2" : {"quantity": -55, "itemType": "factories"}
                                            }
                    }

                }
            }
        


        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionItems["entryID2"]["quantity"], 10)

        # second call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_negative, self.player)      # process the ProductionQ  

        assert_equal(len(target2.productionItems), 4)
        assert_not_in("entryID2", target2.productionItems )
        assert_not_in("entryID2", target2.productionOrder)

    
    def test_xfileController_ProcessProductionQ_CorrectlyHandleUnexpected_Text(self):
        """
        Input: xfile, playerObj
        Output: Items with text values in Q are handled
                (ValueError)


        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }

        xfileSetup_PQ_text = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : {  
                                            "entryID2" : {"quantity": "ERROR", "itemType": "factories"}
                                            }
                    }

                }
            }


        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionItems["entryID2"]["quantity"], 10)

        # second call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_text, self.player)      # process the ProductionQ  

        #assert_equal(target2.productionItems["entryID2"]["quantity"], 0)
        #assert_raises(ValueError, processProductionQ, xfileSetup_PQ_text, self.player)

        # an entry with an invalid reference should not change?
        assert_equal(len(target2.productionItems), 5)
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionItems["entryID2"]["quantity"], 10)

    
    def test_xfileController_ProcessProductionQ_CorrectlyHandleUnexpected_ItemKey(self):
        """
        Input: xfile, playerObj
        Output: Items with an item key that is not in productionOrder is ignored


        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }

        xfileSetup_PQ_ItemKey= {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : {  
                                            "ERRORVAL" : {"quantity": 42353, "itemType": "factories"}
                                            }
                    }

                }
            }


        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # 2nd colony - sanity check Pre-first call
        assert_equal(target2.productionOrder, [])
        assert_equal(target2.productionItems, {}) 

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(len(target2.productionItems), len(target2.productionOrder))

        assert_equal(target2.productionOrder[0], "entryID4")
        assert_equal(target2.productionOrder[1], "entryID1")
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionOrder[3], "entryID5")
        assert_equal(target2.productionOrder[4], "entryID6")

        assert_equal(target2.productionItems["entryID4"]["quantity"], 455)
        assert_equal(target2.productionItems["entryID5"]["quantity"], 1)
        assert_equal(target2.productionItems["entryID6"]["quantity"], 4)
        assert_equal(target2.productionItems["entryID1"]["quantity"], 5)

        # second call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_ItemKey, self.player)      # process the ProductionQ      

        assert_equal(target2.productionOrder[0], "entryID4")
        assert_equal(target2.productionOrder[1], "entryID1")
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionOrder[3], "entryID5")
        assert_equal(target2.productionOrder[4], "entryID6")

        assert_equal(target2.productionItems["entryID4"]["quantity"], 455)
        assert_equal(target2.productionItems["entryID5"]["quantity"], 1)
        assert_equal(target2.productionItems["entryID6"]["quantity"], 4)
        assert_equal(target2.productionItems["entryID1"]["quantity"], 5)

    
    def test_xfileController_ProcessProductionQ_CorrectlyHandleUnexpected_OrderKey(self):
        """
        Input: xfile, playerObj
        Output: OrderKey that does not have a match in the Items


        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }


        xfileSetup_PQ_OrderKey= {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "ERRORVAL" ],
                        "productionItems" : {  
                                            "entryID6" : {"quantity": 42353, "itemType": "factories"}
                                            }
                    }

                }
            }


        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionItems["entryID2"]["quantity"], 10)

        # second call -> to adjust the Q order
        # processProductionQ(xfileSetup_PQ_OrderKey, self.player)      # process the ProductionQ  

        #assert_equal(target2.productionItems["entryID2"]["quantity"], 0)
        assert_raises(ValueError, processProductionQ, xfileSetup_PQ_OrderKey, self.player)

    
    def test_xfileController_ProcessProductionQ_CorrectlyHandleUnexpected_BlankOrderKey(self):
        """
        Input: xfile, playerObj
        Output: A "" OrderKey should be a ValueError



        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }


        xfileSetup_PQ_blankkeyOrder= {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "" ],
                        "productionItems" : {  
                                            "entryID6" : {"quantity": 42353, "itemType": "factories"}
                                            }
                    }

                }
            }

        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionItems["entryID2"]["quantity"], 10)

        # second call -> to adjust the Q order
        #processProductionQ(xfileSetup_PQ_blankkeyOrder, self.player)      # process the ProductionQ  

        #assert_equal(target2.productionItems["entryID2"]["quantity"], 0)
        assert_raises(ValueError, processProductionQ, xfileSetup_PQ_blankkeyOrder, self.player)

    
    def test_xfileController_ProcessProductionQ_CorrectlyHandleUnexpected_BlankQuantity(self):
        """
        Input: xfile, playerObj
        Output: quantity == "" should raise a ValueError



        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }


        xfileSetup_PQ_blankQuantity= {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "" ],
                        "productionItems" : {  
                                            "entryID6" : {"quantity": "", "itemType": "factories"}
                                            }
                    }

                }
            }

        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionItems["entryID2"]["quantity"], 10)

        # second call -> to adjust the Q order
        # processProductionQ(xfileSetup_PQ_blankQuantity, self.player)      # process the ProductionQ  

        #assert_equal(target2.productionItems["entryID2"]["quantity"], 0)
        assert_raises(ValueError, processProductionQ, xfileSetup_PQ_blankQuantity, self.player)

    
    def test_xfileController_ProcessProductionQ_CorrectlyHandleUnexpected_BlankProductionID(self):
        """
        Input: xfile, playerObj
        Output: Items with negative or odd values in XFile are correctly test_xfileController_ProcessProductionQ_CorrectlyHandleUnexpectedQuantityValues




        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }
        xfileSetup_PQ_v = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID77", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : {  
                                            "entryID77" : {"quantity": 5, "itemType": ""}
                                            }
                    }

                }
            }
        

        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionItems["entryID2"]["quantity"], 10)

        # second call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_v, self.player)      # process the ProductionQ  

        #assert_equal(target2.productionItems["entryID2"]["quantity"], 0)
        assert_raises(ValueError)

    



    def test_xfileController_ProcessProductionQ_CorrectlyIncreaseItemQuantityWOWork(self):
        """
        Input: xfile, playerObj
        Output: Items quantity is correctly increased if the item has had no work done on it
        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }
        xfileSetup_PQ_v2 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6"  ],
                        "productionItems" : {  
                                            "entryID2" : {"quantity": 15, "itemType": "factories"}
                                            }
                    }

                }
            }
        xfileSetup_PQ_v3 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6"  ],
                        "productionItems" : {  
                                            "entryID5" : {"quantity": 30, "itemType": "factories"}
                                            }
                    }

                }
            }

        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # 2nd colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionItems["entryID2"]["quantity"], 10)
        assert_equal(target2.productionOrder[3], "entryID5")
        assert_equal(target2.productionItems["entryID5"]["quantity"], 1)


        # second call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_v2, self.player)      # process the ProductionQ  

        # 2nd colony - after update _v2
        assert_equal(len(target2.productionItems), 5)
        assert_equal(target2.productionOrder[2], "entryID2")
        assert_equal(target2.productionItems["entryID2"]["quantity"], 15)
        

        # Third call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_v3, self.player)      # process the ProductionQ  

        # 2nd colony - after update _v2
        assert_equal(len(target2.productionItems), 5)
        assert_equal(target2.productionOrder[3], "entryID5")
        assert_equal(target2.productionItems["entryID5"]["quantity"], 30)



    def test_xfileController_ProcessProductionQ_CorrectlyHandleQuantityIncreaseWWorkDone(self):
        """
        Input: xfile, playerObj
        Output: Items that have work done need to add a new entry when the quantity is increased.
        """

        colony2 = self.newColony[0]

        xfileSetup_PQ_v1 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "itemType": "mines"}, 
                                            "entryID2" : {"quantity": 10, "itemType": "factories"},
                                            "entryID4" : {"quantity": 455, "itemType": "mines"},
                                            "entryID5" : {"quantity": 1, "itemType": "factories"},
                                            "entryID6" : {"quantity": 4, "itemType": "mines"}                                              
                                            }

                    }

                }
            }
        xfileSetup_PQ_v2 = {"ProductionQ" : 
                {
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2", "entryID5", "entryID6" ],
                        "productionItems" : {  
                                            "entryID5" : {"quantity": 5, "itemType": "factories"}
                                            }
                    }

                }
            }

        assert_true(colony2)
        target2 = self.player.colonies[colony2].productionQ

        # first call -> to set up the values
        processProductionQ(xfileSetup_PQ_v1, self.player)      # process the ProductionQ

        # colony - sanity check Post-first call
        assert_equal(len(target2.productionItems), 5)
        assert_equal(target2.productionOrder[3], "entryID5")
        assert_equal(target2.productionItems["entryID5"]["quantity"], 1)
        print(target2.productionItems["entryID5"]["materialsUsed"])
        assert_equal(target2.productionItems["entryID5"]["materialsUsed"], [0, 0, 0, 0])

        # adjust work done on entryID5
        target2.productionItems["entryID5"]["materialsUsed"] = [11, 23, 5, 813]
        print(target2.productionItems["entryID5"]["materialsUsed"])

        # second call -> to adjust the Q order
        processProductionQ(xfileSetup_PQ_v2, self.player)      # process the ProductionQ  

        # 2nd colony - after update 
        assert_equal(len(target2.productionItems), 6)

        # existing should remain 
        assert_equal(target2.productionOrder[3], "entryID5")
        assert_equal(target2.productionItems["entryID5"]["quantity"], 1)
        assert_equal(target2.productionItems["entryID5"]["materialsUsed"], [11, 23, 5, 813])
        print("Order: %s" % target2.productionOrder)
        assert_equal(target2.productionOrder[4], "entryID51")
        assert_equal(target2.productionItems["entryID51"]["quantity"], 4)
        assert_equal(target2.productionItems["entryID51"]["materialsUsed"], [0, 0, 0, 0])


