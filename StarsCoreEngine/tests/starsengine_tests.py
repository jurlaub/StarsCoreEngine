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

from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_true, assert_false
#import nose
import os
import os.path
import random

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
    po1 = planet.Planet((43, 2001), 333, "Saratoga", None, (100,50,32), (55, 30, 10))
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


    def test_universe_createHWPlanet(self):
        """
        Using the game as the universe and raceData template, create a generator
        that will add N number of HW's (for the same race) and collect them in 
        a key:value dictionary. Each of the collection should have a key that 
        aligns with the value.ID & the universe key. 

        additionally the random number of new HW's should be added to the universe.planet
        (note: they will all have the same owner - this part is not a reflection of the game.)
        """
        DEBUG = True

        randtest = random.randrange(10, 30)  # random count for test

        testHW1 = {}
        testHW0 = {}
        player1 = self.game.players["player1"]
        player0 = self.game.players["player0"]
        raceData1 = player1.raceData
        raceData0 = player0.raceData

        uni = self.game.game_universe[0]

        testDetails = True

        initialPlanetCount = len(uni.planets)
        if DEBUG: print("\ninitialPlanetCount:%d; randtest:%d" % (initialPlanetCount, randtest))

        e = 0
        o = 0
        for i in range(0, randtest):

            if i%2:

                newHW = uni.createHomeworldPlanet(raceData1)
                testHW1[newHW.ID] = newHW
                o +=1
            else:
                newHW = uni.createHomeworldPlanet(raceData0)
                testHW0[newHW.ID] = newHW
                e +=1
            
            if DEBUG: print("n:%d:: e:%d o:%d\n-->  ID:%s Name:%s\n-testHW0(%d)-testHW1(%d)  \n" % (i, e, o, newHW.ID, newHW.name, len(testHW0), len(testHW1)))

        postPlanetCount = len(uni.planets)
        if DEBUG: print("\npostPlanetCount:%d; randtest:%d" % (postPlanetCount, randtest))

        assert_equal(len(uni.planets), initialPlanetCount + randtest)

        assert_equal(len(testHW1) + len(testHW0), randtest)


        # if testDetails:
        #     for kee, obj in testHW0.items():
        #         print("kee ->testHW0[%s]; obj.ID:%s;    obj.Name:%s; uni.planets.name(kee):%s; uni.planets.name(obj.ID):%s; " % (kee, obj.ID, obj.name, uni.planets[kee].name, uni.planets[obj.ID].name))
        #     for kee, obj in testHW1.items():
        #         print("kee ->testHW1[%s]; obj.ID:%s;    obj.Name:%s; uni.planets.name(kee):%s; uni.planets.name(obj.ID):%s; " % (kee, obj.ID, obj.name, uni.planets[kee].name, uni.planets[obj.ID].name))



        for kee, obj in testHW0.items():
            tplanet_obj = uni.planets[obj.ID]
            tplanet_kee = uni.planets[kee]

            assert_equal(tplanet_kee.ID, tplanet_obj.ID)
            assert_equal(tplanet_kee.ID, obj.ID )

            assert_equal(tplanet_kee.name, tplanet_obj.name)
            assert_equal(tplanet_kee.name, obj.name )

            assert_equal(kee, obj.ID)
            assert_equal(kee, uni.planets[obj.ID].ID)


        for kee, obj in testHW1.items():
            tplanet_obj = uni.planets[obj.ID]
            tplanet_kee = uni.planets[kee]

            assert_equal(tplanet_kee.ID, tplanet_obj.ID)
            assert_equal(tplanet_kee.ID, obj.ID )

            assert_equal(tplanet_kee.name, tplanet_obj.name)
            assert_equal(tplanet_kee.name, obj.name )

            assert_equal(kee, obj.ID)
            assert_equal(kee, uni.planets[obj.ID].ID)

        #assert_equal(len(uni.planets), initialPlanetCount + randtest)

        #assert_true(False)

    
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

            testPlanet = Planet((10,25), "0_1", "testPlanet", None, playerHab)
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

        self.planet1 = planet.Planet((104,300), '024', 'Abbadon', None )

    def teardown(self):
        print("TestGamePlanets: Teardown")

    def test_Planet_Objects(self):
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



