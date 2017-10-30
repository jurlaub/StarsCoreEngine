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

from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_true, assert_false, assert_not_in
#import nose
import os
import os.path
import random



from ..starscoreengine.order_of_events import order_of_events_fleets_move, order_of_events_population

from ..starscoreengine.game import Game
from ..starscoreengine.template import *
from ..starscoreengine.player import Player

from ..starscoreengine.productionQ import *
from ..starscoreengine.game_xfile import processDesign, processProductionQ
from ..starscoreengine.planet import Planet
from ..starscoreengine.colony import Colony
from ..starscoreengine.fleets import FleetObject
from ..starscoreengine.fleet_command import FleetCommand

from ..starscoreengine.universe import UniverseObject
from ..starscoreengine.template_race import startingDesigns, startingShipDesignsCount, startingDesignsCount, startingDesignsNames #colonyShip, scoutShip, destroyerShip, smallFrieghterShip


from .helper import findPlayerHW, PlayerTestObject, generate_fleet_orders_from_standard_offset






class TestOrderOfEvents(object):
    """
    TestOrderOfEvents - test generic game starting from turn 0

    """

    def setup(self):
        # print("TestOrderOfEvents: Setup")
        # self.playerFileList = ['playerTest1', 'playerTest2']
        # self.testGameName = 'EventsTest'

        # self.gameTemplate = game.StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        # self.universe_data = self.gameTemplate.universe_data
        # self.game = game.Game(self.gameTemplate)


        print("TestOrderOfEvents: Setup")


        self.playerFileList = ['Wolfbane', 'Bunnybane', 'Sharkbane']
        self.testGameName = 'rabidTest'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "3"}})
        self.game = Game(self.gameTemplate)

    
        self.player0 = self.game.players['player0']
        self.player1 = self.game.players['player1']
        self.player2 = self.game.players['player2']

        self.all_players = (self.player0, self.player1, self.player2)
        #self.techLevels = self.player1.research.techLevels
        

        #--------- obtain colony worlds -------------
        
        self.universePlanets = self.game.game_universe[0].planets
        self.universe = self.game.game_universe[0]


        #--------- obtain HW -------------
        self.p0_colonyHW_name, self.p0_colonyHW_obj = findPlayerHW(self.player0.colonies)        
        self.p1_colonyHW_name, self.p1_colonyHW_obj = findPlayerHW(self.player1.colonies)
        self.p2_colonyHW_name, self.p2_colonyHW_obj = findPlayerHW(self.player2.colonies)

        self.all_players_HW_obj = (self.p0_colonyHW_obj, self.p1_colonyHW_obj, self.p2_colonyHW_obj)

        #--------- end ------------------



    def teardown(self):
        print("TestOrderOfEvents: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))




    def test_Population(self):
        
        player1 = self.game.players['player0']
        colonies = player1.colonies

        assert_true(len(colonies) == 1)
        key, colony = colonies.popitem()
        tmpPop = colony.population
        # print("%s population = %d" % (colony.planet.name, tmpPop))
        assert_true(tmpPop > 0)
        colonies[key] = colony

        assert_true(len(colonies) == 1)

        order_of_events_population(self.game)

        colonyAfter = colonies[key] 
        assert_true(tmpPop < colonyAfter.population)
        assert_false(tmpPop == colonyAfter.population)
        # print("%s population = %d" % (colonyAfter.planet.name, colonyAfter.population) )


    def test_fleetsMove(self):

        hw_list = []

        #  ----  create list of HW coordinates -----
        for hw_obj in self.all_players_HW_obj:
            print(hw_obj.planet.xy)
            hw_list.append(tuple(hw_obj.planet.xy))
            print(hw_list)

        # ----- check that the players fleets are located at on of the HW coords ----
        for x in range(0, len(self.all_players)):
            for fleet in self.all_players[x].fleetCommand.fleets.values():
                assert_equal(fleet.xy, hw_list[x])

        # --- obtain orders ----
        for x in range(0, len(self.all_players)):
            

            playerOrders = generate_fleet_orders_from_standard_offset(list(self.all_players[x].fleetCommand.fleets.keys()), self.all_players_HW_obj[x].planet.xy)
            self.all_players[x].fleetCommand.addOrdersToFleetsForTurn(playerOrders)



        order_of_events_fleets_move(self.game)


        # for eachHW in hw_list:
        #     self.universe.objectsAtXY[eachHW]:


        for x in range(0, len(self.all_players)):

            for fleet in self.all_players[x].fleetCommand.fleets.values():
                print(fleet.fleetOrders)
                # assert_not_equal(fleet.xy,  hw_list[x])
                # if fleet.ID in self.universe.objectsAtXY[hw_list[x]]:
                assert_not_in(fleet.ID, self.universe.objectsAtXY[hw_list[x]])
                assert_not_equal(fleet.xy, hw_list[x])
            

        #assert_true(False)

