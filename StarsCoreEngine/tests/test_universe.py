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
from ..starscoreengine.player_designs import PlayerDesigns
from ..starscoreengine.tech import ShipDesign 
from ..starscoreengine.productionQ import *
from ..starscoreengine.game_xfile import processDesign, processProductionQ
from ..starscoreengine.planet import Colony, Planet
from ..starscoreengine.fleets import FleetObject, Token
from ..starscoreengine.universe import UniverseObject
from ..starscoreengine.template_race import startingDesigns, startingShipDesignsCount, startingDesignsCount #colonyShip, scoutShip, destroyerShip, smallFrieghterShip



class TestUniverse(object):
    """
    Test structure for universe class

    """

    def setup_class():
        """
        Generating 1 tech tree for all tests by making the techTree a class 
        level dictionary. (due to python namespace, the class tree will be found)

        """


        self = TestUniverse

        print("TestUniverse: Setup")


        self.playerFileList = ['Wolfbane', 'Bunnybane', 'Sharkbane']
        self.testGameName = 'rabidTest'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "3"}})
        self.game = Game(self.gameTemplate)

        self.techTree = self.game.technology
        self.player0 = self.game.players['player0']
        self.player1 = self.game.players['player1']

        self.techLevels = self.player1.research.techLevels
        

        #--------- obtain colony worlds -------------
        
        self.universePlanets = self.game.game_universe[0].planets
        self.universe = self.game.game_universe[0]


        #--------- obtain HW -------------
        self.p1_colonyHW_name = None
        self.p1_colonyHW_obj = None
        for kee, each in self.player1.colonies.items():
            if each.planet.HW:
                self.p1_colonyHW_name = kee
                self.p1_colonyHW_obj = each
                break
        #--------- end ------------------

        self.p1_ship1_name = "Seer"
        self.p1_ship2_name = "Dark Star I"
        self.p1_ship3_name = "Dark Falcon"

        self.testStarbase_OF = "Orbital Fort"
        self.testStarbase_SB = "Space Station"

        #  ---------------------- test PlayerDesigns.addDesign -----------------
        self.p1_ship1_design = {'designName': self.p1_ship1_name, 
                          'designID': 4,
                          'hullID': 'Scout',
                          'component': {"B": {"itemID": "Fuel Mizer", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Mole Scanner", "itemQuantity": 1}
                            } }



        self.p1_ship2_design = {'designName': self.p1_ship2_name, 
                          'designID': 6,
                          'hullID': 'Destroyer',
                          'component': {"G": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1 },
                                        "E": {"itemID": "Energy Capacitor", "itemQuantity": 1},
                                        "D": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 1},
                                        "F": {"itemID": "Crobmnium", "itemQuantity": 1},
                                        "C": {"itemID": "Phaser Bazooka", "itemQuantity": 1},
                                        "B": {"itemID": "Phaser Bazooka", "itemQuantity": 1},
                                        "A": {"itemID": "Manoeuvring Jet", "itemQuantity": 1}
                                                                    } }
        self.p1_ship3_design = {'designName': self.p1_ship3_name, 
                          'designID': 7,
                          'hullID': "Privateer",
                          'component': {"A": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 2 },
                                        "B": {"itemID": "Colloidal Phaser", "itemQuantity": 1},
                                        "C": {"itemID": "Colloidal Phaser", "itemQuantity": 1},
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
                "Design4" : self.p1_ship1_design,
                "Design5" : self.p1_ship2_design,
                "Design6" : self.p1_ship3_design,
                "Design8" : self.testStarbase1,
                "Design9" : self.testStarbase2
            },
            "RemoveDesign" : []

        }

        # use existing method to import gamefile data
        #processDesign(self.player1_xFile, self.player1, self.game.technology)

        # used by ProductionQ for itemType
        self.productionID_Ship = "Ship"
        self.productionID_Starbase = "Starbase"


        self.p1_build_three_ships = {"ProductionQ" : 
            {
                self.p1_colonyHW_name:
                    {
                        "productionOrder" : [   self.p1_ship1_name, self.p1_ship2_name, self.p1_ship3_name ],
                        "productionItems" : {   self.p1_ship1_name : {"quantity": '3', "designID": self.p1_ship1_design, "itemType" : self.productionID_Ship },
                                                self.p1_ship2_name : {"quantity": '1', "designID": self.p1_ship2_design, "itemType" : self.productionID_Ship},
                                                self.p1_ship3_name : {"quantity": '1', "designID": self.p1_ship3_design, "itemType" : self.productionID_Ship }
                                            
                                            }

                    }

                }
            }  


        self.test_starbase1_template = {"ProductionQ" : 
            {
                self.p1_colonyHW_name:
                    {
                        "productionOrder" : [ self.testStarbase_OF ],
                        "productionItems" : { self.testStarbase_OF : {"quantity": "1", "designID": self.testStarbase_OF, "itemType" : self.productionID_Starbase }                                             
                                            }

                    }

                }
            }



    def teardown_class():
        self = TestUniverse
        

        print("TestUniverse: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))



    def setup(self):
        print("TestUniverse: Setup")

        # ------- Generate Players Starting Ships ----------
        #self.game.generatePlayersStartingShips()

        self.p1_colonyHW_obj.planet.factories = 10
        self.p1_colonyHW_obj.planet.surfaceIron = 200
        self.p1_colonyHW_obj.planet.surfaceBor = 200
        self.p1_colonyHW_obj.planet.surfaceGerm = 200
        self.p1_colonyHW_obj.population = 450000




        # print("setup: On HW pop:%d iron: %d bor: %d germ: %s" % (self.populationOnHW, self.ironOnHW, self.borOnHW, self.germOnHW))

        # ----- ship design -----
        self.player1Designs = self.player1.designs


        # print("setup: shipDesign:%d  \n%s"%(len(self.playerDesigns.currentShips), self.playerDesigns.currentShips))
        # print("setup: %s ::: %s" % (self.testShip1_name, self.design_testShip1.designName))

        self.p1_colonyPQ = self.p1_colonyHW_obj.productionQ

        self.p1_colonyPQ.test_ship = 0
        self.p1_colonyPQ.productionOrder = []     
        self.p1_colonyPQ.productionItems = {} 
        self.p1_colonyPQ.test_ResourcesConsumed = 0


        # self.player1.fleetCommand.fleets = {}
        # self.player1.fleetCommand.currentFleetID = 0
        # self.universe.fleetObjects = {} 
        # self.universe.objectsAtXY[self.p1_colonyHW_obj.planet.xy] = []    # target_colony_obj exists here

        self.player1.research.researchTax = .01    # set to 0 for production tests




        self.baseFleets = self.player1.fleetCommand.fleets #= {}
        self.baseFleetID = self.player1.fleetCommand.currentFleetID # = 0
        self.baseFleetObjects = self.universe.fleetObjects # = {} 
        self.baseObjectsAtXY = self.universe.objectsAtXY #[self.target_colony_obj.planet.xy] = []    # target_colony_obj exists here




    def teardown(self):
        print("TestShipDesign: Teardown")

        self.player1.fleetCommand.fleets = self.baseFleets
        self.player1.fleetCommand.currentFleetID = self.baseFleetID
        self.universe.fleetObjects = self.baseFleetObjects
        self.universe.objectsAtXY = self.baseObjectsAtXY

    @staticmethod
    def _getHW_XY(player):

        for colony in player.colonies.values():
            if colony.planet.HW:
                return colony.planet.xy




    def test_setupClass(self):

        assert_true(isinstance(self.player0, Player))
        assert_true(isinstance(self.player1, Player))
        assert_true(isinstance(self.p1_colonyHW_obj, Colony))
        assert_true(isinstance(self.universe, UniverseObject))
        
        for player in self.game.players.values():
            colonyXY = TestUniverse._getHW_XY(player)
            assert_true(len(player.fleetCommand.fleets) == startingShipDesignsCount())   # fleets should be starting fleet values
            assert_true(len(self.universe.objectsAtXY[colonyXY]) == startingShipDesignsCount())



