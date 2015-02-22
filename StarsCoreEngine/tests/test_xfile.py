"""
    This file is part of Stars Core Engine, which provides an interface and 
    processing of Stars data. 

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



        # --------- productionQ grab planets --------
        self.target_colony = None
        for each in self.player.colonies.values():
            print("each: %s" % each.planet.ID)
            if each.planet.HW:
                self.target_colony = each.planet.ID
                break
        
        self.newColony = []
        self.universePlanets = self.game.game_universe[0].planets

        for kee, obj in self.universePlanets.items():
            if len(self.newColony) > 2:
                break

            if not obj.owner:
                self.newColony.append(kee)

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
        assert_true(p0.raceName, self.playerFileList[0])
        #print("count designs:%s" % len(p0.designs.currentShips))
        assert_equal(len(p0.designs.currentShips), 0)



        xFileController(self.game)


        # values after to xFileController being called
        assert_equal(len(p0.designs.currentShips), 2)





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
                "player.colonies.ID1" : 
                    { 
                        "productionOrder" : [ ],
                        "productionItems" : { }  
                    },
                "player.colonies.ID2" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "item1"}, "entryID2" : {"quantity": 5, "productionID": "item1"} }
                    },
                "player.colonies.ID3" : 
                    {
                        "productionOrder" : [ "entryID2" ],
                        "productionItems" : { "entryID2" : {"quantity": 5, "productionID": "item1"}}
                    }

            }
            }
        isValid = xFile_ProductionQ_StructureIsValid(tmp_xfile_ProductionQ)
        assert_true(isValid)
        
    def test_xFile_ProductionQ_StructureIsValid_ValidItemValues(self):
        tmp_xfile_ProductionQ1 = {
        "ProductionQ" : 
            {

                "correct colony Q" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "item1"}, "entryID2" : {"quantity": 34, "productionID": "item2"} }
                    }

            }
            }
        tmp_xfile_ProductionQ2 = {
        "ProductionQ" : 
            {

                "error colony Q2" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "item1"}, "entryID2" : {} }
                    }

            }
            }
        tmp_xfile_ProductionQ3 = {
        "ProductionQ" : 
            {

                "error colony Q3" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "item1"}, "entryID2" : {"quantity": 2} }
                    }

            }
            }
        tmp_xfile_ProductionQ4 = {
        "ProductionQ" : 
            {

                "error colony Q4" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "item1"}, "entryID2" : {"productionID": "item1"} }
                    }

            }
            }
        tmp_xfile_ProductionQ5 = {
        "ProductionQ" : 
            {

                "error colony Q5" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "item1", "CrazySauce" : "hello"}, "entryID2" : {"productionID": "item1"} }
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

                "correct colony Q" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "item1"}, "entryID2" : {"quantity": 34, "productionID": "item2"} }
                    }

            }
            }

        tmp_xfile_ProductionQ2 = {
        "ProductionQ" : 
            {

                "error colony Q2" : 
                    {
                        "productionOrder" : ["ERROREntry", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "item1"}, "entryID2" : {"quantity": 34, "productionID": "item2"} }
                    }

            }
            }
        tmp_xfile_ProductionQ3 = {
        "ProductionQ" : 
            {

                "error colony Q3" : 
                    {
                        "productionOrder" : ["entryID1", "entryID1" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "item1"}, "entryID2" : {"quantity": 34, "productionID": "item2"} }
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
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "mines"}, "entryID2" : {"quantity": 10, "productionID": "factories"} }
                    },
                colony2 :
                    {
                        "productionOrder" : ["entryID4", "entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "mines"}, 
                                            "entryID2" : {"quantity": 10, "productionID": "factories"},
                                            "entryID4" : {"quantity": 455, "productionID": "mines"} 
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
        assert_equal(target.productionItems["entryID1"]["productionID"], "mines")


        # 2nd colony
        assert_equal(len(target2.productionOrder), 3)
        assert_equal(target2.productionOrder[0], "entryID4")

        assert_equal(len(target2.productionItems), 3)
        assert_equal(target2.productionItems["entryID4"]["quantity"], 455)        

