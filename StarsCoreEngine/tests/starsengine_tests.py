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
from ..starscoreengine import *


#old - for reference -  use test classes
def test_spaceobjects():

    t1 = space_objects.SpaceObjects((5,7), 4433)
    
    
    print ("id=%s" % (t1.getCurrentCoord(),))
    assert t1.getCurrentCoord() == (5, 7)

#old - for reference -  use test classes
def test_planet():
    po1 = planet.Planet((43, 2001), 333, "Saratoga", (100,50,32), (55, 30, 10))
    xy = (43, 2001)

    assert_equal("Saratoga", po1.getName())
    assert_equal((100,50,32), po1.getOrigHab())
    assert_equal(333, po1.getID())
    assert_equal((43,2001), po1.getCurrentCoord())
    assert_equal(xy, po1.getDestinationCoord())



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
        assert_equal(4433, self.t1.getID())


class TestGameTemplate(object):

    def setup(self):
        print("TestGameTemplate: Setup")
        self.gameTemplate = game.StandardGameTemplate()

    def teardown(self):
        print("TestGameTemplate: Teardown")

    def test_SGT_Contains_UniverseData(self):
        assert_in("UniverseSizeXY", self.gameTemplate.universe_data[0])
        assert_in("UniverseName", self.gameTemplate.universe_data[0])
        u_name = self.gameTemplate.universe_data[0]["UniverseName"]
        assert_true(u_name)

    def test_SGT_GetUniverseSize(self):
        tmp = self.gameTemplate.getUniverseSize()
        assert_true(len(tmp) == 1)
        assert_true(tmp[0] == (200,200))


    
class TestMultiGameTemplate(object):
    '''
    Test multiuniverse games
    '''
    def setup(self):
        print("TestMultiGameTemplate: Setup")
        self.universe_count = 5
        self.universe_player = 3
        self.gameTemplate = game.StandardGameTemplate({}, self.universe_count, self.universe_player)

    def teardown(self):
        print("TestMultiGameTemplate: Teardown")

    
    def test_SGT_Multiverse(self):
        tmp = self.gameTemplate.universe_data
        #tmp.universe_data = tmp.multiUniverse()
        x = self.universe_count - 1
        assert_true(len(tmp) > 1)
        assert_true(len(tmp) == self.universe_count)
        assert_true(x == int(tmp[x]['UniverseNumber']))
        print("UniverseNumber = %d" % (tmp[x]['UniverseNumber'],))

    def test_SGT_GetMultiverseSizes(self):
        tmp = self.gameTemplate.getUniverseSize()
        assert_true(len(tmp) == self.universe_count)
        print("test_SGT_GetMultiverseSizes is a list: %s || and || %s" % (isinstance(tmp, tuple), tmp))
        assert_true(tmp[0] == (200,200))  
        assert_true(isinstance(tmp, tuple))


class TestGameSetup(object):
    
    def setup(self):
        print("TestGameSetup: Setup")
        self.gameTemplate = game.StandardGameTemplate()
        self.universe_data = self.gameTemplate.universe_data
        self.game = game.GameSetup(self.gameTemplate)
        print("TestGameSetup: self.universe_data uses a HARDCODED list")
        self.numbPlanets = self.universe_data[0]["UniversePlanets"]   # HARDCODED!!!

    def teardown(self):
        print("TestGameSetup: Teardown")

    def test_Planet_Objects(self):
        tmpPlanet = self.game.planets 
        #print("%s" % tmpPlanet.keys())
        assert_true(isinstance(tmpPlanet, dict))
        #print("%s,%s,%s"% tmpPlanet["01"].currConc)
        assert(len(tmpPlanet) == self.numbPlanets)
        tmpItem = tmpPlanet["03"]
        assert_in(tmpItem.name, self.gameTemplate.planetNameTemplate())
        assert_false(tmpItem.HW)


class TestPickling(object):
    
    def setup(self):
        print("TestPickling: Setup ... (pickling a test game)")
        self.cwd = os.getcwd()
        print("cwd: %s" % self.cwd)
        self.tmpGameTemplate = game.StandardGameTemplate()
        self.tmpGame = game.GameSetup(self.tmpGameTemplate)




    def teardown(self):
        print("TestPickling: Teardown")
        try:
            os.remove(r"%s/%s"% (self.cwd, self.tmpPickleName))
        except IOError as e:
            print("Unable to remove file: %s%s" % (self.cwd, self.tmpPickleName))

    def test_Pickle(self):
        self.tmpGame.planets['01'].name = "Starbuck_Straw"
        self.tmpPickleName = 'tmp_pickle.tmp'
        pickleTest = (self.tmpGameTemplate, self.tmpGame)
        game.GamePickle.makePickle(self.tmpPickleName, pickleTest)

        tmpTemplate, tmpGame = game.GamePickle.unPickle(self.tmpPickleName)
        print("test_Pickle: has HARDCODED SpaceObjects(planets) keys: '01', '02'")
        assert_true(tmpGame.planets['01'].name == "Starbuck_Straw")
        assert_true(tmpGame.planets['02'].name == self.tmpGame.planets['02'].name)
        assert_true(len(tmpGame.planets) == len(self.tmpGame.planets))

        
        



class TestGamePlanets(object):

    def setup(self):
        print("TestGame: Setup")
        self.gameTemplate = game.StandardGameTemplate()

    def teardown(self):
        print("TestGame: Teardown")

    def test_Planet_Objects(self):
        pass





#old - for reference -  use test classes
#   t1 = None

#   def setup(self):
#       print ("SETUP!")
#       t1 = space_objects.SpaceObjects(5,7,4433)
#       po1 = planet.Planet(43, 2001, 333, "Saratoga", (100,50,32), (55, 30, 10))
#       print ("id=%s" % (t1.getCurrentCoord(),))


#       #print ("planet id=%d; name:%s" % (self.po1.getID(), self.po1.getName()))
#       #return t1

#   def teardown(self):
#       print ("TEAR DOWN!")

#   @with_setup(setup, teardown)
#   def test_basic(self):
#       assert t1.getID() == 4433
#       print ("I RAN!")

#   @with_setup(setup, teardown)
#   def test_SpaceObject(self):
#       assert t1.getCurrentCoord() == (5, 7)
#       print ("id=%s" % (t1.printCurrentCoord()))