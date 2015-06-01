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



from ..starscoreengine.player_build_list import *
from ..starscoreengine.game import Game
from ..starscoreengine.template import *


class TestPlayerBuildList(object):

    def setup(self):
        print("TestPlayerBuildList: Setup")

        self.playerFileList = ['Wolfbane', 'Bunnybane']
        self.testGameName = 'xFileTestFile'
        self.playerXFile0 = 'xFileTestFile.x0'
        self.playerXFile1 = 'xFileTestFile.x1'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.game = Game(self.gameTemplate)
        self.player = self.game.players["player0"]





    def teardown(self):
        print("TestPlayerBuildList: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))


    def test_PlayerBuildList_Exists(self):

        assert_true(self.player.buildListObject)


    def test_PlayerBuildList_BaseItems(self):
        """
        Base Items: Mines, Factories, Scanner, Defenses 

        """

        buildListObj = self.player.buildListObject

        buildList = buildListObj.buildList

        assert_in("Mines", buildList)
        assert_in("Factories", buildList)

        scanner = False
        for each in buildList:
            if each["itemType"] == "PlanetaryScanner":
                scanner = True  
                break
        assert_true(scanner)


        defenses = False
        for each in buildList:
            if each["itemType"] == "PlanetaryDefenses":
                defenses = True  
                break
        assert_true(defenses)





