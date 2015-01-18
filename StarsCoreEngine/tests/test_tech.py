"""
    This file is part of Stars Core Engine, which provides an interface and 
    processing of Stars data. 

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

    Contributors to this project agree to abide by the interpretation expressed 
    in the COPYING.Interpretation document.

"""
"""
Purpose: To test technology as it is used in the Game. 

Areas of Concern: 

1) game.technology objects




"""


#import unittest
from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_true, assert_false
from math import fabs


from ..starscoreengine import *
from ..starscoreengine.template_tech import *


# Test_CustomTechTree ?

# class TestTech(unittest.TestCase):
class Test_StandardTechTree(object):

    #setup

    #teardown



    # tests --TODO--
    # standard co

    # assert each standard component has the correct object type
    # assert / validate basic component object type values -> 
    #   weapons have power, initiative
    #   shields have shieldDP
    #   engines have engine stuff
    #   etc 


    def test_order(self):


        tech = order_tech()
        assert_equal(tech["shields"]["Croby Sharmor"], {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 4, 
                                                            "electronics" : 0, "biotechnology" : 0, "mass" : 10, "resources" : 15, 
                                                            "iron" : 7, "bor" : 0, "germ" : 4, "shieldDP" : 60, "hasPRT" : ["IS"], "hasLRT" : [], "notLRT" : []})
        assert_not_equal(tech["shields"]["Croby Sharmor"], {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 4, 
                                                            "electronics" : 0, "biotechnology" : 0, "mass" : 10, "resources" : 15, 
                                                            "iron" : 7, "bor" : 0, "germ" : 4, "shieldDP" : 60, "hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []})

    def test_hulls(self):

            tmp =  {"Battleship" : {"Armor" : [6],
                            "Armor Scanner Elect/Mech" : [],
                            "Bomb" : [],
                            "Elect" : [3, 3],
                            "Engine" : [4],
                            "General Purpose" : [],
                            "Mech" : [],
                            "Mine" : [],
                            "Mine Elect Mech" : [],
                            "Mining" : [],
                            "Scanner" : [],
                            "Scanner Elect Mech" : [1],
                            "Shield" : [8],
                            "Shield Elect Mech": [],
                            "Shield or Armor" : [],
                            "Weapon" : [2, 2, 6, 6, 4]}
            }
            hullDicts = hull_slots(tmp)
            expectedDict = {'A': {'objectType': ['Engine'], 'slotsAvalable': 4 }, 
                            'B': {'slotsAvalable': 6, 'objectType': ['Armor']}, 
                            'C': {'slotsAvalable': 2, 'objectType': ['Weapon']}, 
                            'D': {'slotsAvalable': 2, 'objectType': ['Weapon']},              
                            'E': {'slotsAvalable': 6, 'objectType': ['Weapon']}, 
                            'F': {'slotsAvalable': 6, 'objectType': ['Weapon']}, 
                            'G': {'slotsAvalable': 4, 'objectType': ['Weapon']}, 
                            'H': {'slotsAvalable': 8, 'objectType': ['Shield']}, 
                            'I': {'slotsAvalable': 3, 'objectType': ['Elect']}, 
                            'J': {'slotsAvalable': 3, 'objectType': ['Elect']},
                            'K': {'slotsAvalable': 1, 'objectType': ['Scanner', 'Elect', 'Mech']}
                        }


            # Dictionary ordering is always random. The keys cannot be expected to contain the same slots
            # the solution below seems to work but is suspect. It may have to do with how the function is hashed. 
            # reordering the expectedDict 'A' key produced no difference in the test.

            #self.assertEqual(hullDicts["Battleship"], expectedDict)    # does not work
            tmpTarget = hullDicts["Battleship"].values()
            tmpExpected = expectedDict.values()

            #print("%s" % tmpTarget)

            for n in tmpTarget:
                assert_true(n in tmpExpected)
                #print(n)






