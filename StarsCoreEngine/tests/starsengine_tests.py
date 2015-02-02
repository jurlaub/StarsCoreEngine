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

from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_true, assert_false
#import nose
import os
import os.path
from ..starscoreengine import *
from ..starscoreengine.universe import UniverseObject
from ..starscoreengine.player import Player
from ..starscoreengine.player import RaceData as Race
from ..starscoreengine.game_utility import GamePickle
from ..starscoreengine.order_of_events import *
from ..starscoreengine.tech import Component, Hull
from ..starscoreengine.player_designs import PlayerDesigns

#old - for reference -  use test classes
def test_spaceobjects():

    t1 = space_objects.SpaceObjects((5,7), 4433)
    
    
    print ("id=%s" % (t1.xy,))
    assert t1.xy == (5, 7)

#old - for reference -  use test classes
def test_planet():
    po1 = planet.Planet((43, 2001), 333, "Saratoga", (100,50,32), (55, 30, 10))
    xy = (43, 2001)

    assert_equal("Saratoga", po1.name)
    assert_equal((100,50,32), po1.origHab)
    assert_equal(333, po1.ID)
    assert_equal((43,2001), po1.xy)
    assert_equal(xy, po1.destinationXY)



class TestSpaceObject(object):

    #classmethods run once before the class is run
    @classmethod
    def setup_class(cls):
        #from ..starscoreengine.space_objects import SpaceObjects
        print ("class setup")

        

    @classmethod
    def teardown_class(cls):
        print("class teardown")


    # method run before each test method within the class
    def setup(self):
        print("setup ")
        self.t1 = space_objects.SpaceObjects((5,7), 4433)
        

    def teardown(self):
        print("teardown")


    def test_spaceobject_exists(self):
        print("SpaceObjects: test exists")
        assert_equal(4433, self.t1.ID)








    
      


class TestGame(object):
    '''
    This class tests game.Game() 



    '''
    
    def setup(self):
        print("TestGame: Setup")
        self.playerFileList = ['playerTest1', 'playerTest2']
        self.testGameName = 'rabidTest'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = game.StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.universe_data = self.gameTemplate.universe_data
        self.game = game.Game(self.gameTemplate)


    def teardown(self):
        print("TestGame: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))

    # def dtest_Planet_Objects(self):
    #     tmpPlanet = self.game.planets 
    #     #print("%s" % tmpPlanet.keys())
    #     assert_true(isinstance(tmpPlanet, dict))
    #     #print("%s,%s,%s"% tmpPlanet["01"].currConc)
    #     assert(len(tmpPlanet) == self.numbPlanets)
    #     tmpItem = tmpPlanet["03"]
    #     assert_in(tmpItem.name, self.gameTemplate.planetNameTemplate())
    #     assert_false(tmpItem.HW)

    def test_generateUniverses_Zero(self):

        #--- TODO --- can it handle 0 universes?
        pass

    def test_generateUniverses_Single(self):
        # can it generate 1 universe?
        tmpKey = 0      # 0 = key for 1st universe

        tmpUniverse = self.game.game_universe[tmpKey]

        assert_true(self.gameTemplate.universeNumber == 1)
        assert(len(self.gameTemplate.universe_data) == 1)
        assert_true(isinstance(self.game.game_universe, dict))
        
        assert_true(isinstance(tmpUniverse, UniverseObject))
        assert_true(isinstance(tmpUniverse.planets, dict))
        
        #one will be true
        totalPlanets = int(tmpUniverse.UniversePlanets) + int(tmpUniverse.Players)
        assert_true(len(tmpUniverse.planets) == totalPlanets)


        print("%s" % tmpUniverse.planets)
        
        planetsNonHW = 0
        planetsHW = 0

        for item in tmpUniverse.planets:
            planet = tmpUniverse.planets[item]

            if planet.HW:
                planetsHW += 1
            elif not planet.HW:
                planetsNonHW += 1
            else:
                assert_true(False)  # should not get here.

        print("Planets: %d; homeworld: %d " % (planetsNonHW, planetsHW))

        assert_true(planetsNonHW == int(self.universe_data[0]["UniversePlanets"]))
        assert_true(planetsHW == int(tmpUniverse.Players))


    
    
    def test_generateUniverses_Multiple(self):

        # --- TODO --- can it handle multiple universes
        pass

    def test_Players(self):
        players = self.game.players

        assert_true(isinstance(players, dict))
        assert_true(len(players) == len(self.playerFileList))

        # val == to dictionary key 
        for val in players:
            playerObject = players[val]         # use key to grab player object

            assert_true(isinstance(playerObject, Player))
            assert_in(playerObject.raceName, self.playerFileList)

            #test HW
            assert_true(isinstance(playerObject.colonies, dict))
            print("player colonies have %d colonies" % len(playerObject.colonies))
            assert_true(len(playerObject.colonies) == 1)
            homeworldKey, homeworld = playerObject.colonies.popitem()
            
            assert_true(homeworld.planet.HW == True)
            assert_true(homeworld.planet.owner == playerObject.raceName)
            assert_true(homeworld.scanner == True)

    def test_Players_HW(self):
        pass

    
    def test_Player_PlanetValue_Assessment(self):
        player1 = self.game.players['player1']
        rd = player1.raceData

        rd.habGravityCenter = 1.0  # 1 (centerpoint) total range = .85 to 1.15
        rd.habGravRadius = -1  # 15.0 pos range from Center. Total range doubled  
        
        rd.habTempCenter = 70 
        rd.habTempRadius = -1

        rd.habRadCenter = 50
        rd.habRadRadius = 13.0

        testPlanet = Planet((10,25), "0_1", "testPlanet", (90, 1.1, 45))

        assert_true(isinstance(player1, Player))

        print("Grav(%s, %s); Temp(%s, %s); Rad(%s, %s)" % 
            (rd.habGravityCenter, rd.habGravRadius,
                rd.habTempCenter, rd.habTempRadius,
                rd.habRadCenter, rd.habRadRadius))

        assert_equal(player1.planetValue(testPlanet), 90)

        # for kee, p in self.game.game_universe[0].planets.items():
        #     val = player1.planetValue(p)
        #     print("%s for %s has value:%d%. (planet:%s, %s, %s)" % 
        #         (rd.raceName, p.name, val, p.currentGrav, p.currentTemp, p.currentRad ))

    def test_Player_PlanetValue_AssessHW(self):
        tmpPlayers = self.game.players

        for kee, player1 in tmpPlayers.items():
            #player1 = self.game.players['player1']
            rd = player1.raceData

            playerHab = (rd.habGravityCenter, rd.habTempCenter, rd.habRadCenter)

            testPlanet = Planet((10,25), "0_1", "testPlanet", playerHab)
            testPlanetVal = player1.planetValue(testPlanet)

            assert_equal(testPlanetVal, 100)
            print("PlayerName:%s; planetVal: %s; planetStats: (%d,%d,%d)" % 
                (player1.raceName, testPlanetVal, playerHab[0], 
                playerHab[1],playerHab[2]))
        
        #assert_true(False)

    def test_Player_PlanetValue_AssessRandom(self):

        pass
        

    def test_Technology(self):
        assert_true(isinstance(self.game.technology, dict) )

    def test_GenerateTechnology(self):
        ''' send in a template and return a dictionary of tech items '''
        tmpDict = self.game.generateTechnology(self.gameTemplate)
        assert_true(isinstance(tmpDict, dict))


    def test_Game_StandardTech(self):
        tmpTech = self.game.technology

        o1 = tmpTech.pop("Scout")
        assert_true(isinstance(o1, Hull))
        assert_true('slot' in o1.__dict__)
        s = o1.slot
        assert_true(isinstance(s, dict))
        assert_true(len(s) == 3)


        o2 = tmpTech.pop("X-Ray Laser")
        assert_true(isinstance(o2, Component))
        assert_equal(o2.beamPower, 16)


    """
    PlayerDesign integration tests
    """

    def test_PlayerDesign_Exist(self):
        """
        PlayerDesign object exist
        """
        p = self.game.players

        for kee, obj in p.items():
            assert_true(isinstance(obj.designs, PlayerDesigns))
            
            ship = obj.designs.currentShips
            starbase = obj.designs.currentStarbases

            assert_true(isinstance(ship, dict))
            assert_true(isinstance(starbase, dict))
            






class TestPickling(object):
    
    def setup(self):
        print("TestPickling: Setup ... (pickling a test game)")
        self.cwd = os.getcwd()
        print("cwd: %s" % self.cwd)
        self.tmpGameTemplate = game.StandardGameTemplate()
        self.tmpGame = game.Game(self.tmpGameTemplate)
        self.tmpPickleName = 'tmp_pickle.tmp'



    def teardown(self):
        print("TestPickling: Teardown")
        try:
            os.remove(r"%s/%s"% (self.cwd, self.tmpPickleName))
        except IOError as e:
            print("Unable to remove file: %s%s" % (self.cwd, self.tmpPickleName))

    def test_Pickle(self):
        tmpUniverse = self.tmpGame.game_universe[0]

        tmpUniverse.planets['0_1'].name = "Starbuck_Straw"

        pickleTest = (self.tmpGame)
        


        GamePickle.makePickle(self.tmpPickleName, pickleTest)

        savedGame = GamePickle.unPickle(self.tmpPickleName)
        print("test_Pickle: has HARDCODED SpaceObjects(planets) keys: '0_1', '0_2'")
        savedUniverse = savedGame.game_universe[0]    

        assert_true(savedUniverse.planets['0_1'].name == "Starbuck_Straw")
        assert_true(savedUniverse.planets['0_2'].name == tmpUniverse.planets['0_2'].name)
        assert_true(len(savedUniverse.planets) == len(tmpUniverse.planets))

        
        



class TestGamePlanets(object):

    def setup(self):
        print("TestGamePlanets: Setup")
        self.planet1 = planet.Planet((104,300), '024', 'Abbadon')

    def teardown(self):
        print("TestGamePlanets: Teardown")

    def test_Planet_Objects(self):
        pass


class TestColonyPlanets(object):

    def setup(self):
        print("TestColonyPlanets: Setup")
        self.playerKey = 'player1'
        self.raceName = 'Wolfbane'
        self.RaceData = Race(self.raceName)
        self.player = Player(self.RaceData, 0, {})
        self.playerCenterHab = (self.RaceData.habGravityCenter, 
                                self.RaceData.habTempCenter, 
                                self.RaceData.habRadCenter)


        self.population = 25000
        self.SO_ID = '024'
        self.planetName = 'Abbadon'

        self.planetOne = planet.Planet((104,300), self.SO_ID, self.planetName, 
                                            self.playerCenterHab )
        self.player.colonizePlanet(self.planetOne, self.population)



    def teardown(self):
        print("TestColonyPlanets: Teardown")

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
        assert_true(colony.planet.owner == self.raceName)
        assert_true(colony.growthRate == self.player.raceData.growthRate)

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
        assert_true(False)




    def test_Planet_Resources(self):
        pass




class TestOrderOfEvents(object):

    def setup(self):
        print("TestOrderOfEvents: Setup")
        self.playerFileList = ['playerTest1', 'playerTest2']
        self.testGameName = 'EventsTest'

        self.gameTemplate = game.StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.universe_data = self.gameTemplate.universe_data
        self.game = game.Game(self.gameTemplate)


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

        population(self.game)

        colonyAfter = colonies[key] 
        assert_true(tmpPop < colonyAfter.population)
        assert_false(tmpPop == colonyAfter.population)
        # print("%s population = %d" % (colonyAfter.planet.name, colonyAfter.population) )



