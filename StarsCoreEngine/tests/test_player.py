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
Purpose:    To test the player object. 
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
from ..starscoreengine.tech import Hull
from ..starscoreengine.ship_design import ShipDesign 
from ..starscoreengine.template_race import startingStarbase
from ..starscoreengine.game_xfile import processDesign
from ..starscoreengine.fleets import Starbase
from ..starscoreengine.productionQ import ProductionQ









class TestPlayerDesign(object):
    """
    Tests for PlayerDesign



    """

    def setup(self):
        print("TestPlayerDesign: Setup")

        self.testShip1 = {'designName': 'doomShip1', 
                          'designID': 0,
                          'hullID': 'Scout',
                          'component': {"B": {"itemID": "Fuel Mizer", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Mole Scanner", "itemQuantity": 1}
                            } }

        self.testShip2 = {'designName': 'basic scout', 
                          'designID': 1,
                          'hullID': 'Scout',
                          'component': {"B": {"itemID": "Quick Jump 5", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Bat Scanner", "itemQuantity": 1}
                            } }


        self.testShip3 = {'designName': 'doomShip2', 
                          'designID': 2,
                          'hullID': 'Destroyer',
                          'component': {"G": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1 },
                                        "E": {"itemID": "Energy Capacitor", "itemQuantity": 1},
                                        "D": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 1},
                                        "F": {"itemID": "Crobmnium", "itemQuantity": 1},
                                        "C": {"itemID": "X-Ray Laser", "itemQuantity": 1},
                                        "B": {"itemID": "X-Ray Laser", "itemQuantity": 1},
                                        "A": {"itemID": "Manoeuvring Jet", "itemQuantity": 1}
                                                                    } }
        self.testShip4 = {'designName': 'doomShip3', 
                          'designID': 3,
                          'hullID': "Privateer",
                          'component': {"A": {"itemID": "Bear Neutrino Barrier", "itemQuantity": 2 },
                                        "B": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "D": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "E": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1},
                                                                    } }

        # need ship with 'restricted tech' so that producing it will be off
        self.starbaseHWName, self.starbaseHWObject = startingStarbase()

        self.starbaseName = 'StarBase_Awesome'

        self.starbaseObject = {  'designName': self.starbaseName, 
                                'designID': self.starbaseName,
                                'hullID': "Space Station",
                                'component': {  "A": {"itemID": "Wolverine Diffuse Shield", "itemQuantity": 2 },
                                                "B": {"itemID": "Colloidal Phaser", "itemQuantity": 5},
                                                "F": {"itemID": "Crobmnium", "itemQuantity": 1},
                                                "D": {"itemID": "Jihad Missile", "itemQuantity": 1}
                                                                    } }


        self.dockName = 'StarDock_Berry'

        self.dockObject = { 'designName': self.dockName, 
                                'designID': self.dockName,
                                'hullID': "Space Dock",
                                'component': {  "A": {"itemID": "Wolverine Diffuse Shield", "itemQuantity": 2 },
                                                "B": {"itemID": "Colloidal Phaser", "itemQuantity": 5},
                                                "F": {"itemID": "Crobmnium", "itemQuantity": 1},
                                                "D": {"itemID": "Jihad Missile", "itemQuantity": 1}
                                                                    } }                                        



        self.playerFileList = ['Wolfbane', 'Bunnybane']
        self.testGameName = 'rabidTest'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.game = Game(self.gameTemplate)
        self.player1 = self.game.players['player1']

        self.techTree = self.game.technology

        self.player1_xFile = {
            "NewDesign" : { self.starbaseName : self.starbaseObject,
                            self.dockName : self.dockObject
                             },
            "RemoveDesign" : [] }

        processDesign(self.player1_xFile, self.player1, self.techTree)

        #--------- obtain HW -------------
        self.colonyHWName = None
        self.colonyHWObject = None
        for kee, each in self.player1.colonies.items():
            if each.planet.HW:
                self.colonyHWName = kee
                self.colonyHWObject = each
                break
        #--------- end ------------------


    def teardown(self):
        print("TestPlayerDesign: Teardown")

        self.colonyHWObject.planet.orbitalStarbase = None



        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))


    def test_stardock_reports_smaller_dock_size(self):

        assert_true(self.colonyHWObject.planet.orbitalStarbase == None)

        self.colonyHWObject.productionQ.produceStarbase(1, self.dockName)

        dock = self.colonyHWObject.planet.orbitalStarbase
        assert_true(len(dock.tokens) == 1)
        massRating = dock.starbaseMassRating()
        assert_true(massRating == '200')

    def test_starbase_reports_spaceDockSize(self):

        print("colony.planet.orbitalStarbase: %s" % self.colonyHWObject.planet.orbitalStarbase )
        assert_true(self.colonyHWObject.planet.orbitalStarbase == None)

        dockSizes = (0, 200, Hull.INFINITY)
        self.colonyHWObject.productionQ.produceStarbase(1, self.starbaseName)

        starbase = self.colonyHWObject.planet.orbitalStarbase
        massRating = int(starbase.starbaseMassRating())
        assert_true(len(starbase.tokens) == 1)

        assert_true(massRating in dockSizes)
        assert_true(massRating == Hull.INFINITY)

    def test_starbase_design_has_spaceDockSize(self):
        """
        tests whether a space station includes spaceDockSize
        """
        assert_true(self.colonyHWObject.planet.orbitalStarbase == None)

        processDesign(self.player1_xFile, self.player1, self.techTree)
        assert_true(len(self.player1.designs.currentStarbases) >= 1)

        for each, obj in self.player1.designs.currentStarbases.items():
            print("test: %s:%s" % (each, obj))
            print("spaceDockSize:%s" % obj.spaceDockSize)
            assert_in('spaceDockSize', obj.__dict__)
            #assert_true(obj.__dict__['spaceDockSize'] is not None)
            assert_in(obj.spaceDockSize, [0, 200, Hull.INFINITY]) #['0', '200', 'infinite'])


        #starbaseAwesome = self.player1.designs.currentStarbases[self.starbaseName]

        #print("%s" % starbaseAwesome)
        #assert_true(isinstance(starbaseAwesome, Starbase))

        #assert_true(False)


    def test_AddDesign(self):
        """PlayerDesigns.AddDesign unit tests

        # check newDesign.hull for starbase or ship type
        # check that capacity has not been reached
        # check that name is not a duplicate

        # Instantiate ShipDesign
        # update values
        
        # add to appropriate currentDict

        """
        # design is added to correct dictionary (ship/starbase)
        #if we are at capacity, what should be done?

        #Ship Design added

        # values are correct

        for player in self.game.players.values():
            designs = player.designs
            shipCount = len(designs.currentShips)
            starbaseCount = len(designs.currentStarbases)

            assert_not_in(self.testShip1['designName'], designs.currentShips)


            designs.addDesign(self.testShip1, self.techTree)  


            assert_equal(len(designs.currentShips), shipCount + 1)
            assert_equal(len(designs.currentStarbases), starbaseCount)
            assert_in(self.testShip1["designName"], designs.currentShips) #assert ship now in design
            
            t1 = designs.currentShips[self.testShip1["designName"]]
            tmpHull = self.testShip1['hullID']       
            tmpScanner = [100]  #Mole scanner normal range is 0
            assert_not_in("NAS", player.LRT)


            assert_equal(t1.normalScanRange, tmpScanner)
            assert_equal(t1.hullID, tmpHull)
            assert_equal(t1.designName, self.testShip1["designName"])

            assert_equal(t1.owner, player.raceName)         # different then the player key. 

    def test_AddDesign_OverCapacity(self):
        """PlayerDesigns.AddDesign unit tests

        # check newDesign.hull for starbase or ship type
        # check that capacity has not been reached
        # check that name is not a duplicate

        # Instantiate ShipDesign
        # update values
        
        # add to appropriate currentDict

        """

        designs = self.player1.designs
        maxDesigns = 19

        shipCount = len(designs.currentShips)

        for i in range(0, maxDesigns):
            tmpName = self.testShip1['designName']
            tmpName = tmpName + str(i)
            self.testShip1['designName'] = tmpName

            designs.addDesign(self.testShip1, self.techTree)

        assert_equal(designs.DesignCapacity, len(designs.currentShips))


    def test_AddDesign_DuplicateEntries(self):
        """PlayerDesigns.AddDesign unit tests

        # check newDesign.hull for starbase or ship type
        # check that capacity has not been reached
        # check that name is not a duplicate

        # Instantiate ShipDesign
        # update values
        
        # add to appropriate currentDict

        """
        designs = self.player1.designs

        shipCount = len(designs.currentShips)
        starbaseCount = len(designs.currentStarbases)

        assert_not_in(self.testShip1['designName'], designs.currentShips)


        designs.addDesign(self.testShip1, self.techTree)  
        assert_in(self.testShip1['designName'], designs.currentShips)
        assert_equal(len(designs.currentShips), shipCount + 1)

        designs.addDesign(self.testShip1, self.techTree) 

        assert_equal(len(designs.currentShips), shipCount + 1)
        assert_equal(len(designs.currentStarbases), starbaseCount)


    def test_RemoveDesign(self):
        """RemoveDesign 
        Given any design - remove it from the list. (other remove parts are called elsewhere)
        if a design does not exist - return None

        """
        designs = self.player1.designs
        shipName = self.testShip1['designName']

        assert_not_in(self.testShip1['designName'], designs.currentShips)
        shipCount = len(designs.currentShips)

        designs.addDesign(self.testShip1, self.techTree) 
        secondCount = len(designs.currentShips)

        assert_equal(shipCount + 1, secondCount)
        assert_true(shipName in designs.currentShips)


        designs.removeDesign(shipName)

        
        assert_equal(shipCount,len(designs.currentShips) )
        assert_not_in(shipCount, designs.currentShips)

    def test_TransferDesign(self):
        pass

    def test_ValidDesignForProduction(self):
        pass



    def test_raceData_TerraformCosts(self):

        # player.raceData test terraformCosts
        techItem = self.techTree["Gravity Terraform 7"]
        itemIron = 0 if techItem.iron == None else techItem.iron
        itemBor = 0 if techItem.bor == None else techItem.bor
        itemGerm = 0 if techItem.germ == None else techItem.germ
        expectedItemCosts = [itemIron, itemBor, itemGerm, techItem.resources]



        assert_equal(expectedItemCosts, self.player1.raceData.terraformCosts)


    def test_raceData_DefensesCosts(self):

        # player.raceData test terraformCosts
        techItem = self.techTree["SDI"]
        itemIron = 0 if techItem.iron == None else techItem.iron
        itemBor = 0 if techItem.bor == None else techItem.bor
        itemGerm = 0 if techItem.germ == None else techItem.germ
        expectedItemCosts = [itemIron, itemBor, itemGerm, techItem.resources]



        assert_equal(expectedItemCosts, self.player1.raceData.defensesCosts)


    def test_raceData_ScannerCosts(self):

        # player.raceData test terraformCosts
        techItem = self.techTree["Viewer 50"]
        itemIron = 0 if techItem.iron == None else techItem.iron
        itemBor = 0 if techItem.bor == None else techItem.bor
        itemGerm = 0 if techItem.germ == None else techItem.germ
        expectedItemCosts = [itemIron, itemBor, itemGerm, techItem.resources]



        assert_equal(expectedItemCosts, self.player1.raceData.scannerCosts)

    def test_raceData_MineralCosts(self):

        # player.raceData test terraformCosts
        # techItem = self.techTree["Viewer 50"]
        # itemIron = 0 if techItem.iron == None else techItem.iron
        # itemBor = 0 if techItem.bor == None else techItem.bor
        # itemGerm = 0 if techItem.germ == None else techItem.germ
        # expectedItemCosts = [itemIron, itemBor, itemGerm, techItem.resources]
        print("TestPlayerDesign.test_raceData_MineralCosts HARDCODED MineralCosts")
        expectedItemCosts = [0, 0, 0, 100]


        assert_equal(expectedItemCosts, self.player1.raceData.mineralCosts)



