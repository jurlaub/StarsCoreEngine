"""
    This file is part of Stars Core Engine, which provides an interface and 
    processing of Game data. 

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
Purpose:    To test the Standard Technology Tree. 


"""

import os
import os.path

#import unittest
from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_true, assert_false
from math import fabs



from ..starscoreengine import *
from ..starscoreengine.template import *
from ..starscoreengine.template_tech import *
# from ..starscoreengine.player_designs import PlayerDesigns



def test_order():


    tech = order_tech()
    assert_equal(tech["Shield"]["Croby Sharmor"], {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 4, 
                                                        "electronics" : 0, "biotechnology" : 0, "mass" : 10, "resources" : 15, 
                                                        "iron" : 7, "bor" : 0, "germ" : 4, "shieldDP" : 60, "hasPRT" : ["IS"], "hasLRT" : [], "notLRT" : [],
                                                        "itemType": "Shield"})
    assert_not_equal(tech["Shield"]["Croby Sharmor"], {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 4, 
                                                        "electronics" : 0, "biotechnology" : 0, "mass" : 10, "resources" : 15, 
                                                        "iron" : 7, "bor" : 0, "germ" : 4, "shieldDP" : 60, "hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : [],
                                                        "itemType": "Shield"})

def test_hulls():

        tmp =  {"Battleship" : {"Armor" : [6],
                        "Armor Scanner Elect Mech" : [],
                        "Bomb" : [],
                        "Elect" : [3, 3],
                        "Engine" : [4],
                        "GeneralPurpose" : [],
                        "Mech" : [],
                        "Mine" : [],
                        "Mine Elect Mech" : [],
                        "Mining" : [],
                        "Scanner" : [],
                        "Scanner Elect Mech" : [1],
                        "Shield" : [8],
                        "Shield Elect Mech": [],
                        "Shield Armor" : [],
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


# Test_CustomTechTree ?






class Test_StandardTechnologyTemplate(object):
    """Test_StandardTechnologyTemplate examines the StandardGameTemplate.Technology
    to certify that the standard components are valid.  


    """


    def setup_class():
        """
        Generating 1 tech tree for all tests by making the techTree a class 
        level dictionary. (due to python namespace, the class tree will be found)

        """


        self = Test_StandardTechnologyTemplate

        print("Test_StandardTechnologyTemplate: Setup")


        self.playerFileList = ['Wolfbane', 'Bunnybane']
        self.testGameName = 'rabidTest'
        #self.testCustomSetup = {"UniverseNumber0": { "Players": "2"}}

        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {"UniverseNumber0": { "Players": "2"}})
        self.techTree = self.gameTemplate.technology


    def teardown_class():
        self = Test_StandardTechnologyTemplate
        

        print("Test_StandardTechnologyTemplate: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))



    def test_weap_xray(self):
        x = self.techTree["X-Ray Laser"]
        assert_equal(x["weapons"], 3)
        assert_equal(x["beamPower"], 16)


        assert_equal(x["resources"], 6)
        assert_equal(x["iron"], 0)
        assert_equal(x["bor"], 6)
        assert_equal(x["germ"], 0)
        assert_equal(x["range"], 1)
        assert_equal(x["energy"], 0)
        assert_equal(x["electronics"], 0)
        assert_equal(x["hasPRT"], [])
        assert_equal(x["mass"], 1)
        assert_equal(x["initiative"], 9)
        assert_in("itemType", x)
        assert_equal(x["itemType"], 'BeamWeapons')

        # assert_equal(x["itemType"], "Weapon")


    # def test_weap_xray2(self):
    #     x = self.techTree["X-Ray Laser"]
    #     assert_equal(x["beamPower"], 16)
        

    def test_engine_fuelMizer(self):
        x = self.techTree["Fuel Mizer"]

        assert_equal(x["weapons"], 0)
        assert_equal(x["propulsion"], 2)
        assert_equal(x["energy"], 0)
        assert_equal(x["electronics"], 0)
        assert_equal(x["construction"], 0)
        assert_equal(x["biotechnology"], 0)


        assert_equal(x["resources"], 11)
        assert_equal(x["iron"], 8)
        assert_equal(x["bor"], 0)
        assert_equal(x["germ"], 0)

        assert_equal(x["hasPRT"], [])
        assert_equal(x["hasLRT"], ["IFE"])
        assert_equal(x["mass"], 6)
        assert_in("itemType", x)
        assert_equal(x["itemType"], 'Engine')


    def test_shield_cowhide(self):
        x = self.techTree["Cow-hide Shield"]

        assert_equal(x["weapons"], 0)
        assert_equal(x["propulsion"], 0)
        assert_equal(x["energy"], 3)
        assert_equal(x["electronics"], 0)
        assert_equal(x["construction"], 0)
        assert_equal(x["biotechnology"], 0)


        assert_equal(x["resources"], 5)
        assert_equal(x["iron"], 2)
        assert_equal(x["bor"], 0)
        assert_equal(x["germ"], 2)

        assert_equal(x["hasPRT"], [])
        assert_equal(x["shieldDP"], 40)
        assert_equal(x["mass"], 1)
        assert_in("itemType", x)
        assert_equal(x["itemType"], 'Shield')

    def test_weap_jihad(self):
        x = self.techTree["Jihad Missile"]

        assert_equal(x["weapons"], 12)
        assert_equal(x["propulsion"], 6)
        assert_equal(x["energy"], 0)
        assert_equal(x["electronics"], 0)
        assert_equal(x["construction"], 0)
        assert_equal(x["biotechnology"], 0)


        assert_equal(x["resources"], 13)
        assert_equal(x["iron"], 37)
        assert_equal(x["bor"], 13)
        assert_equal(x["germ"], 9)

        assert_equal(x["hasPRT"], [])
        assert_equal(x["missilePower"], 85)
        assert_equal(x["hitChance"], 20)
        assert_equal(x["initiative"], 0)
        assert_equal(x["range"], 5)
        assert_equal(x["doubleDamageUnshielded"], True)
        assert_equal(x["mass"], 35)
        assert_in("itemType", x)
        assert_equal(x["itemType"], 'Torpedoes')

    def test_hull_rogue(self):
        pass

    def test_armor_Valanium(self):

        x = self.techTree["Valanium"]

        assert_equal(x["weapons"], 0)
        assert_equal(x["propulsion"], 0)
        assert_equal(x["energy"], 0)
        assert_equal(x["electronics"], 0)
        assert_equal(x["construction"], 16)
        assert_equal(x["biotechnology"], 0)


        assert_equal(x["resources"], 50)
        assert_equal(x["iron"], 15)
        assert_equal(x["bor"], 0)
        assert_equal(x["germ"], 0)

        assert_equal(x["hasPRT"], [])
        assert_equal(x["armorDP"], 500)
        assert_equal(x["mass"], 40)
        assert_in("itemType", x)
        assert_equal(x["itemType"], 'Armor')

    def test_elec_caps(self):
        x = self.techTree["Energy Capacitor"]

        assert_equal(x["weapons"], 0)
        assert_equal(x["propulsion"], 0)
        assert_equal(x["energy"], 7)
        assert_equal(x["electronics"], 4)
        assert_equal(x["construction"], 0)
        assert_equal(x["biotechnology"], 0)


        assert_equal(x["resources"], 5)
        assert_equal(x["iron"], 0)
        assert_equal(x["bor"], 0)
        assert_equal(x["germ"], 8)

        assert_equal(x["hasPRT"], [])
        assert_equal(x["hasLRT"], [])
        assert_equal(x["notLRT"], [])
        assert_equal(x["mass"], 1)

        assert_in("capacitor", x)
        assert_in("itemType", x)
        assert_equal(x["itemType"], 'Elect')

    def test_scanner_ferret(self):
        x = self.techTree["Ferret Scanner"]

        assert_equal(x["weapons"], 0)
        assert_equal(x["propulsion"], 0)
        assert_equal(x["energy"], 3)
        assert_equal(x["electronics"], 7)
        assert_equal(x["construction"], 0)
        assert_equal(x["biotechnology"], 2)


        assert_equal(x["resources"], 36)
        assert_equal(x["iron"], 2)
        assert_equal(x["bor"], 0)
        assert_equal(x["germ"], 8)

        assert_equal(x["hasPRT"], [])
        assert_equal(x["hasLRT"], [])
        assert_equal(x["notLRT"], ["NAS"])
        assert_equal(x["penScanRange"], 50)
        assert_equal(x["normalScanRange"], 185)
        assert_equal(x["mass"], 2)
        assert_in("itemType", x)
        assert_equal(x["itemType"], 'Scanner')

    def test_scanner_RobberBarron(self):
        x = self.techTree["Robber Baron Scanner"]

        assert_equal(x["weapons"], 0)
        assert_equal(x["propulsion"], 0)
        assert_equal(x["energy"], 10)
        assert_equal(x["electronics"], 15)
        assert_equal(x["construction"], 0)
        assert_equal(x["biotechnology"], 10)


        assert_equal(x["resources"], 90)
        assert_equal(x["iron"], 10)
        assert_equal(x["bor"], 10)
        assert_equal(x["germ"], 10)

        assert_equal(x["hasPRT"], ["SS"])
        assert_equal(x["hasLRT"], [])
        assert_equal(x["notLRT"], [])
        assert_equal(x["penScanRange"], 120)
        assert_equal(x["normalScanRange"], 220)
        assert_equal(x["mass"], 20)

        assert_in("stealFromShips", x)
        assert_in("stealFromPlanets", x)

        assert_equal(x["stealFromShips"], True)
        assert_equal(x["stealFromPlanets"], True)
        assert_in("itemType", x)
        assert_equal(x["itemType"], 'Scanner')

    def test_miner_RoboMiner(self):
        x = self.techTree["Robo-Miner"]

        assert_equal(x["weapons"], 0)
        assert_equal(x["propulsion"], 0)
        assert_equal(x["energy"], 0)
        assert_equal(x["electronics"], 2)
        assert_equal(x["construction"], 4)
        assert_equal(x["biotechnology"], 0)


        assert_equal(x["resources"], 100)
        assert_equal(x["iron"], 30)
        assert_equal(x["bor"], 0)
        assert_equal(x["germ"], 7)

        assert_equal(x["hasPRT"], [])
        assert_equal(x["hasLRT"], [])
        assert_equal(x["notLRT"], ["OBRM"])
        assert_equal(x["mass"], 240)

        assert_equal(x["mineralKTPerYear"], 12)
        assert_in("itemType", x)
        assert_equal(x["itemType"], 'Mining')



    def test_bombs_ladyFinger(self):
        x = self.techTree["Lady Finger Bomb"]

        assert_equal(x["weapons"], 2)
        assert_equal(x["propulsion"], 0)
        assert_equal(x["energy"], 0)
        assert_equal(x["electronics"], 0)
        assert_equal(x["construction"], 0)
        assert_equal(x["biotechnology"], 0)


        assert_equal(x["resources"], 5)
        assert_equal(x["iron"], 1)
        assert_equal(x["bor"], 20)
        assert_equal(x["germ"], 0)

        assert_equal(x["hasPRT"], [])
        assert_equal(x["hasLRT"], [])
        assert_equal(x["notLRT"], [])
        assert_equal(x["mass"], 40)

        assert_in("popKillPercent", x)
        assert_equal(x["popKillPercent"], 0.6)
        assert_in("itemType", x)
        assert_equal(x["itemType"], 'Bomb')

    def test_orbital_gate100_250(self):
        x = self.techTree["Stargate 100_250"]

        assert_equal(x["weapons"], 0)
        assert_equal(x["propulsion"], 5)
        assert_equal(x["energy"], 0)
        assert_equal(x["electronics"], 0)
        assert_equal(x["construction"], 5)
        assert_equal(x["biotechnology"], 0)


        assert_equal(x["resources"], 200)
        assert_equal(x["iron"], 50)
        assert_equal(x["bor"], 20)
        assert_equal(x["germ"], 20)

        assert_equal(x["hasPRT"], [ "SS", "WM", "CA", "IS", "SD", "PP", "IT", "AR", "JOAT"])
        assert_equal(x["hasLRT"], [])
        assert_equal(x["notLRT"], [])

        assert_in("safeGateableRange", x)
        assert_equal(x["safeGateableMass"], 100)
        assert_equal(x["safeGateableRange"], 250)
        assert_in("itemType", x)
        assert_equal(x["itemType"], 'Orbital')

    def test_orbital_massDriver(self):
        x = self.techTree["Ultra Driver 11"]

        assert_equal(x["weapons"], 0)
        assert_equal(x["propulsion"], 0)
        assert_equal(x["energy"], 17)
        assert_equal(x["electronics"], 0)
        assert_equal(x["construction"], 0)
        assert_equal(x["biotechnology"], 0)


        assert_equal(x["resources"], 484)
        assert_equal(x["iron"], 24)
        assert_equal(x["bor"], 20)
        assert_equal(x["germ"], 20)

        assert_equal(x["hasPRT"], ["PP"])
        assert_equal(x["hasLRT"], [])
        assert_equal(x["notLRT"], [])

        assert_in("itemType", x)
        assert_equal(x["itemType"], 'Orbital')
        assert_in("warpDriverSpeed", x)
        assert_equal(x["warpDriverSpeed"], 11)


    # more tech componets need to be tested.


