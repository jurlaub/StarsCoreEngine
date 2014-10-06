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

from nose.tools import with_setup, assert_equal, assert_not_equal, assert_raises, raises
#import nose
from ..starscoreengine import fleets, planet, space_objects


def test_spaceobjects():

	t1 = space_objects.SpaceObjects(5,7,4433)
	
	
	print ("id=%s" % (t1.getCurrentCoord(),))
	assert t1.getCurrentCoord() == (5, 7)


def test_planet():
	po1 = planet.Planet(43, 2001, 333, "Saratoga", (100,50,32), (55, 30, 10))
	xy = (43, 2001)

	assert_equal("Saratoga", po1.getName())
	assert_equal((100,50,32), po1.getOrigHab())
	assert_equal(333, po1.getID())
	assert_equal((43,2001), po1.getCurrentCoord())
	assert_equal(xy, po1.getDestinationCoord())



class TestSpaceObject:

	def setup(self):
		print("setup ")
		

	def teardown(self):
		print("teardown")

	@classmethod
	def setup_class(cls):
		print ("class setup")
		t1 = space_objects.SpaceObjects(5,7,4433)

	@classmethod
	def teardown_class(cls):
		print("class teardown")



	def test_spaceobject_exists(self):
		print("SpaceObjects: test exists")
		assert_equal(4433, t1.getID())


# 	t1 = None

# 	def setup(self):
# 		print ("SETUP!")
# 		t1 = space_objects.SpaceObjects(5,7,4433)
# 		po1 = planet.Planet(43, 2001, 333, "Saratoga", (100,50,32), (55, 30, 10))
# 		print ("id=%s" % (t1.getCurrentCoord(),))


# 		#print ("planet id=%d; name:%s" % (self.po1.getID(), self.po1.getName()))
# 		#return t1

# 	def teardown(self):
# 		print ("TEAR DOWN!")

# 	@with_setup(setup, teardown)
# 	def test_basic(self):
# 		assert t1.getID() == 4433
# 		print ("I RAN!")

# 	@with_setup(setup, teardown)
# 	def test_SpaceObject(self):
# 		assert t1.getCurrentCoord() == (5, 7)
# 		print ("id=%s" % (t1.printCurrentCoord()))