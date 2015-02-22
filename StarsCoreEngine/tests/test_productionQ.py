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
 assert_raises, raises, assert_in, assert_not_in, assert_true, assert_false



from ..starscoreengine.productionQ import *

from ..starscoreengine.game import Game
from ..starscoreengine.template import *
from ..starscoreengine.player import Player
# from ..starscoreengine.player import RaceData as Race
from ..starscoreengine.player_designs import PlayerDesigns
# from ..starscoreengine.tech import ShipDesign 
from ..starscoreengine.game_xfile import processDesign



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

        self.target_colony = None
        for each in self.player.colonies.values():
            if each.planet.HW:
                self.target_colony = each
                break
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

        xx = {"ProductionQ" : 
                {
                self.target_colony : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "item1"}, "entryID2" : {} }
                    }

                }
            }
        
        # set a number of variables to the same value - so they can be reused

        pass






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



    def test_productionObjectVariables(self):
        print(self.target_colony.planet.ID)
        print("%s:%s" % (self.target_colony.planet.owner, self.target_colony.planet.name))
        print(self.player.designs.currentShips.keys())
        #assert_true(False)



    def test_removeItemFromQ(self):
        pass


    def test_updateQ_Miniturization(self):
        pass

    def test_controller(self):
        pass




