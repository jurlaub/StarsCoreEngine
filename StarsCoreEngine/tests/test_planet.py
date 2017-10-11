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



from ..starscoreengine.planet import Planet
from ..starscoreengine.colony import Colony
from ..starscoreengine.game import Game
from ..starscoreengine.template import *




class TestColonyPlanets(object):

    def setup(self):
        print("TestColonyPlanets: Setup")

        self.playerFileList = ['Wolfbane', 'Bunnybane']
        self.testGameName = 'xFileTestFile'

        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.game = Game(self.gameTemplate)
        self.player = self.game.players["player0"]
        self.universe = self.game.game_universe[0]


        self.SpeciesData = self.player.speciesData

        
        self.playerCenterHab = (self.SpeciesData.habGravityCenter, 
                                self.SpeciesData.habTempCenter, 
                                self.SpeciesData.habRadCenter)


        self.population = 25000
        self.SO_ID = '024'
        self.planetName = 'Abbadon'

        self.planetOne = Planet((104,300), self.SO_ID, self.planetName, 
                                            self.playerCenterHab )
        self.player.colonizePlanet(self.planetOne, self.population)







    def teardown(self):
        print("TestColonyPlanets: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))



    def test_Colony_PlanetValues(self):
        planet = self.planetOne
        colony = self.player.colonies[self.SO_ID]

        assert_true(planet.name == self.planetName)
        assert_true(planet.ID == self.SO_ID)
        assert_true(colony.population == self.population)
        
        assert_true(colony.planet.name == self.planetName)
        assert_true(colony.planet.ID == self.SO_ID)

    def test_Colony_Planet(self):
        assert_in(self.SO_ID, self.player.colonies)
        colony = self.player.colonies[self.SO_ID]
        assert_true(colony.planet.owner == self.player.speciesName)
        assert_true(colony.growthRate == self.player.speciesData.growthRate)

    def test_ColonyHW_Growth_Low(self):
        """ _Low tests growth for a planet with pop below the 25'%' point

        """
        planet = self.planetOne
        colony = self.player.colonies[self.SO_ID]

        assert_true(colony.population == self.population)

        colony.populationGrowth()
        assert_true(colony.population > self.population)

        habVal = colony.planetValue / 100
        growRate = colony.growthRate
        tmpGrowth = self.population * habVal * growRate

        print("%d population this year" % tmpGrowth)
        assert_true(colony.population == self.population + tmpGrowth)

    def test_ColonyHW_Growth_Mid(self):
        """ _Mid tests pop growth for a planet with population at the 50'%' 
        capacity value @ 100% value

        """
        #planet = self.planetOne
        colony = self.player.colonies[self.SO_ID]
        
        # change the pop to 'half-full' for non- JOAT & HE & AR
        popmid = 500000
        capacity = (popmid * 1.0) / colony.planetMaxPopulation
        colony.population = popmid


        colony.populationGrowth()
        assert_true(colony.population > popmid)

        habVal = colony.planetValue / 100
        print("habvalue: %s" % habVal)
        growRate = colony.growthRate
        tmpGrowth = popmid * habVal * growRate
        tmpGrowth *= 16.0/9
        tmpGrowth *= (1.0 - capacity) * (1.0 - capacity)

        print("%d population this year" % tmpGrowth)
        assert_true(colony.population == popmid + tmpGrowth)

    def test_Colony_Resources(self):
        planet = self.planetOne
        colony = self.player.colonies[self.SO_ID]
        popEfficiency = 1000
        totalResources = self.population / popEfficiency
        

        colony.calcTotalResources(popEfficiency)

        assert_true(colony.totalResources == totalResources)



    def test_Colony_PlanetValueRange(self):
        """
        Planet value must be a range between 100 and 0. 
        The negative values may be reduced to 0 to (-15), -20, -30, -45? 
        (cannot remember negative range)


        """
        print("After player.planetValue() is complete, assess the values for the universe planets - make sure the planet value is correct")
        #assert_true(False)
        pass




    def test_Planet_Resources(self):
        pass




