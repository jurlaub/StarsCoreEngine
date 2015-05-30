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



from ..starscoreengine.game_utility import *
from ..starscoreengine.game import Game
from ..starscoreengine.template import *



class TestGameUtilityItems(object):

    def setup(self):
        print("TestGameUtilityItems: Setup")


        self.playerFileList = ['Wolfbane', 'Bunnybane']
        self.testGameName = 'rabidTest'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.game = Game(self.gameTemplate)
        self.player1 = self.game.players['player1']

        self.techTree = self.game.technology


    def teardown(self):
        print("TestGameUtilityItems: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))



    def test_findMaxTechnologyComponent_weap10_Beam(self):

        techLevels = {"energy" : 0, 
                  "weapons" : 10,
                  "propulsion" : 0,
                  "construction" : 0,
                  "electronics" : 0,
                  "biotechnology" : 0
              }
        targetType = "BeamWeapons"

        tree = self.player1.techTree
        
        playerLevels = self.player1.research.techLevels


        component = findMaxTechnologyComponent(targetType, techLevels, tree)

        assert_equal(component, "Colloidal Phaser")

        playerComponent = findMaxTechnologyComponent(targetType, playerLevels, tree)

        assert_not_equal(component, playerComponent)
        assert_equal(playerComponent, "Laser")


    def test_findMaxTechnologyComponent_weap16_Torp(self):
        """


        """

        techLevels = {"energy" : 0, 
                  "weapons" : 16,
                  "propulsion" : 3,
                  "construction" : 0,
                  "electronics" : 0,
                  "biotechnology" : 0
              }
        targetType = "Torpedoes"

        tree = self.player1.techTree
        
        playerLevels = self.player1.research.techLevels


        component = findMaxTechnologyComponent(targetType, techLevels, tree)

        assert_equal(component, "Epsilon Torpedo")

        playerComponent = findMaxTechnologyComponent(targetType, playerLevels, tree)

        assert_not_equal(component, playerComponent)
        assert_equal(playerComponent, "Alpha Torpedo")


    def test_findMaxTechnologyComponent_PlanetaryScanner(self):
        """
        Ship Scanners are going to be one of the more complicated max tech to determine.

        """

        techLevels = {"energy" : 5, 
                  "weapons" : 8,
                  "propulsion" : 7,
                  "construction" : 6,
                  "electronics" : 8,
                  "biotechnology" : 5
              }
        targetType = "PlanetaryScanner"

        tree = self.player1.techTree
        
        playerLevels = self.player1.research.techLevels


        component = findMaxTechnologyComponent(targetType, techLevels, tree)


        assert_equal(component, "Scoper 280")

        playerComponent = findMaxTechnologyComponent(targetType, playerLevels, tree)

        print("PRT:%s" % (self.player1.PRT))

        assert_equal(self.player1.PRT, "SS")
        assert_equal(playerLevels["electronics"], 5)

        assert_not_equal(component, playerComponent)
        assert_equal(playerComponent, "Scoper 150")



