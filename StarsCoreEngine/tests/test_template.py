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
"""

1) Standard Game Template 
    a) Standard Technology Tree
    b) Custom Technology Trees

The Standard Game Template accepts a variety of standard and customizations. It
then translates those customizations to a form that the game will recognize and
use.

"""

import os
import os.path

from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_true, assert_false

from ..starscoreengine import *
from ..starscoreengine.template_tech import *
from ..starscoreengine.template import *





class TestTechnologyTemplate(object):
    """
    Tests the functions necessary to translate Standard and Custom Tech tree data
    into a technology dictionary useful to a game object.


    """
    def setup(self):
        print("TestTechnologyTemplate: Setup")
        self.playerFileList = ['playerTest1', 'playerTest2', 'playerTest3']
        self.testGameName = "rabidTest"
        self.gameTemplate = StandardGameTemplate(self.testGameName, self.playerFileList)

        self.StandardTree = TechTree()


    def teardown(self):
        print("TestGameTemplate: Teardown")
        try:
            tmpFileName = self.testGameName + '_TechTreeDataError'
            cwd = os.getcwd()
            tmpFileName = r"%s/%s"% (cwd, tmpFileName)
            if os.path.isfile(tmpFileName):
                os.remove(tmpFileName)
        except IOError as e:
            print("Unable to remove file: %s" % (tmpFileName))
            

    def test_Template_technology(self):

        techTree = self.gameTemplate.technology

        assert_true("Heavy Blaster" in techTree)
        assert_true("Energy Capacitor" in techTree)
    
    def test_TechTree_StandardTree(self):
        """
        Tests that the template.py TestTech() method calls template_tech.py
        standard_tech_tree() and that they are the same.

        """
        targetTree = standard_tech_tree()
        
        assert_equal(self.StandardTree, targetTree) 
        
        targetTree['testmethod'] = 34334242
        assert_not_equal(self.StandardTree, targetTree) 

    def test_IteratorOverTree(self):

        #tmpTree should contain: "Dolphin Scanner", "Rho Torpedo", "Large Monty"
        #troubleDict contains: "Rho Torpedo", "Large Monty", "Problem Entry"
        # in neither: "OnlyUseCustomTechTree"
        testTree = {"Dolphin Scanner" :{"energy" : 5, "construction" : 0, 
                                        "electronics" : 10,  "resources" : 40, 
                                        "iron" : 5, "normalScanRange" : 220, 
                                        "penScanRange" : 100}, 
                    "Rho Torpedo" : { "weapons" : 18, "propulsion" : 4,  
                                     "mass" : 25, "resources" : 12, 
                                    "iron" : 34, "bor" : 12, "germ" : 8, 
                                    "range"  : 5, "missilePower" : 90, 
                                    "INITiative" : "Should Be in troubleDict", 
                                    "hitChance" : 75, 
                                    "doubleDamageUnshielded" : False},
                    "Large Monty" : {"iron" : 34, "electronics" : 10, 
                                    "biotechnology" : 4,
                                    "KnightsOfNEE": "Should Be in troubleDict", 
                                    "ARPopulation": "From Hull",
                                    "HolyHandGrenade" : "Should Be in troubleDict"},
                    "OnlyUseCustomTechTree" : "should not be in troubleDict or testTree",
                    "Problem Entry" : "This should be in troubleDict"  
                                        }


        #tmpTree = self.gameTemplate.technology

        troubleDict, tmpTree = self.gameTemplate.iteratorOverTree(testTree)

        assert_true(len(tmpTree) == 3)
        assert_true(len(troubleDict) == 3)
        
        # ARPop = tmpTree["Large Monty"]["ARPopulation"]
        assert_true("Large Monty" in tmpTree)
        assert_equal(tmpTree["Large Monty"]["ARPopulation"], "From Hull")
        
        assert_true("Rho Torpedo" in tmpTree)
        assert_equal(tmpTree["Rho Torpedo"]["missilePower"], 90)

        assert_true("Problem Entry" in troubleDict)
        assert_false("Problem Entry" in tmpTree)

        assert_true("Dolphin Scanner" in tmpTree)

        assert_false("OnlyUseCustomTechTree" in troubleDict)
        assert_false("OnlyUseCustomTechTree" in tmpTree)

    def test_verifyTech(self):  
        targetDict = Component().__dict__

        tmpComponent = {'name': "Sir Gwain", 'iron' : 5, 'hasPRT' : ['SS'],
                        'misElement1': "should not be in component", 
                        'colonizer' : "22 Jump Street", 
                        "error3" : "should not be in component 55"}

        troubleDict, component = self.gameTemplate.verifyTech(targetDict, tmpComponent)

        assert_false("error3" in component)
        assert_true("error3" in troubleDict)
        assert_equal(troubleDict["error3"], "should not be in component 55")

        assert_true('colonizer' in component)
        assert_true(component['name'], "Sir Gwain")

        assert_equal(component['hasPRT'], ['SS'])

        assert_false('beamDeflector' in component)
        assert_false('energy' in troubleDict)

    def test_flattenStandardTree(self):
        """
        input: StandardTechTree

        """
        assert_true("beamWeapons" in self.StandardTree )
        assert_true("Heavy Blaster" in self.StandardTree["beamWeapons"] )     


        assert_false("Heavy Blaster" in self.StandardTree)
        assert_false("Energy Capacitor" in self.StandardTree)
        assert_false("M-70 Bomb" in self.StandardTree)
        assert_false("Trans-Galactic Fuel Scoop" in self.StandardTree)


        self.StandardTree = self.gameTemplate.flattenStandardTree( self.StandardTree)

        assert_true("Heavy Blaster" in self.StandardTree)
        assert_true("Energy Capacitor" in self.StandardTree)
        assert_true("M-70 Bomb" in self.StandardTree)
        assert_true("Trans-Galactic Fuel Scoop" in self.StandardTree)

    def test_CustomizeTree(self):
        # assert custom file updates standard tree
        # assert customized components update standard tree
        # "Overthruster" , "Brave Little Toaster", "Awesomeness with key errors"
        # "Nubian" - value not a dict
        """
        "Overthruster":{"energy" : 5, "weapons" : 0, "propulsion" : 12, "construction" : 0, 
                              "electronics" : 0, "biotechnology" : 0, "mass" : 5, "resources" : 20, 
                              "iron" : 10, "bor" : 0, "germ" : 8, "ability" : 2},
        """

        tmpCustomTree = { "Overthruster" : {"resources" : 500, "bor" : 55, "mass" : 66, 'ability' : 2 },
            "Brave Little Toaster" : {"energy" : 5, "weapons" : 45, "resources" : 88, 'name': "Brave Little Toaster" },
            "Awesomeness with key errors" : {"eNerEE" : 5, "weapEIO" : 45, "resour" : 88},
            "Awesomeness with errors 2" : {"electroniCS" : 44, "biotechnology" : 345, "mass" : 5,},
            "Nubian" : "Should be Trouble"
        }


        troubleDict, tmpTree = self.gameTemplate.customizeTree(self.gameTemplate.technology, tmpCustomTree)


        print(troubleDict)
        #assert_true(len(tmpTree["Awesomeness with key errors"]) == 1 )
        assert_false("Awesomeness with key errors" in tmpTree)

        assert_true("Awesomeness with errors 2" in troubleDict)
        assert_true("Nubian" in troubleDict)
        assert_equal(troubleDict["Nubian"], ["Should be Trouble", 'Obj is not a dictionary.  Not a valid component'] )

        assert_equal(tmpTree["Overthruster"]["resources"], 500)
        assert_equal(tmpTree["Overthruster"]["mass"], 66)
        assert_equal(tmpTree["Overthruster"]["propulsion"], 12) # original data still present
        assert_false("ability" in tmpTree["Overthruster"] )
        assert_true("germ" in tmpTree["Overthruster"] )


        assert_equal(tmpTree["Brave Little Toaster"]["weapons"], 45)
        assert_equal(tmpTree["Brave Little Toaster"]["resources"], 88)
        assert_equal(tmpTree["Brave Little Toaster"]['name'], "Brave Little Toaster")

        assert_true("Nubian" in tmpTree)        # original should be present

    def test_SGT_init_Custom(self):

        tmpCustomTree = {'customComponents' : 
                                {   "Overthruster" : 
                                            {"resources" : 500, "bor" : 55, 
                                            "mass" : 66, 'ability' : 2 },
                                    "Brave Little Toaster" : 
                                            {"energy" : 5, "weapons" : 45, 
                                            "resources" : 88, 
                                            'name': "Brave Little Toaster" }
                        }
                        }
        testTemplate = StandardGameTemplate(self.testGameName, self.playerFileList, {}, 1, tmpCustomTree)

        tmpTree = testTemplate.technology
        assert_true(testTemplate.game_name == self.testGameName)

        assert_true("Brave Little Toaster" in testTemplate.technology)
        assert_equal(tmpTree["Overthruster"]["resources"], 500)

    def test_technologyTree_Empty(self):
        """
        techdict = {}
        techdict = {'OnlyUseCustomTechTree' = True}
        techdict = {'OnlyUseCustomTechTree' = False}
        techdict = {not empty but missing or invalid 'OnlyUseCustomTechTree'}

        techdict = {'CustomComponent'} & standard
        techdict = {'CustomComponent'} & OUCTT

        """ 
        techDict = {}

        tmpTree = self.gameTemplate.technologyTree(techDict)

        assert_equal(tmpTree, self.gameTemplate.technology) 

    def test_technologyTree_OUCTT_True(self):
        """ 'OnlyUseCustomTechTree' == OUCTT
        """ 
        techDict = {"OnlyUseCustomTechTree": 'True',
                    "mechanical" : { "Beam Deflector": {
                                        "weapons": 6,
                                        "construction": 6,
                                        "iron": 0,
                                        "electronics": 6,
                                        "biotechnology": 0,
                                        "resources": 8,
                                        "hasLRT": [],
                                        "propulsion": 0 }, 
                                    "Overthruster": {
                                        "weapons": 0,
                                        "construction": 0,
                                        "iron": 10}
                                    },

                    "torpedoes" : {"Delta Torpedo": {
                                        "hitChance": 60,
                                        "weapons": 10,
                                        "construction": 0},
                                    "Juggernaught Missile": {
                                        "hitChance": 20,
                                        "weapons": 16}
                                    },
                    "scanner" : {"Eagle Eye Scanner": {
                                    "weapons": 0,
                                    "construction": 0,
                                    "penScanRange": 0},
                                "Ferret Scanner": {
                                    "weapons": 0,
                                    "construction": 0,
                                    "penScanRange": 50}
                    }
                }

        tmpTree = self.gameTemplate.technologyTree(techDict)

        assert_not_equal(tmpTree, self.gameTemplate.technology) 

        assert_false("Rhino Scanner" in tmpTree)
        assert_true("Eagle Eye Scanner" in tmpTree)
        assert_true(len(tmpTree) == 6)
        assert_equal(tmpTree["Ferret Scanner"]["penScanRange"], 50)

    def test_technologyTree_OUCTT_False(self):
        """ 'OnlyUseCustomTechTree' == OUCTT
        """ 
        techDict = {"OnlyUseCustomTechTree": 'False',
                    "mechanical" : { "Beam Deflector": {
                                        "weapons": 18,          # changed
                                        "construction": 6,
                                        "iron": 0,
                                        "electronics": 6,
                                        "biotechnology": 0,
                                        "resources": 548,      # changed
                                        "hasLRT": [],
                                        "propulsion": 0 }, 
                                    "Overthruster": {
                                        "weapons": 0,
                                        "construction": 0,
                                        "iron": 10}
                                    },

                    "torpedoes" : {"Delta Torpedo": {
                                        "hitChance": 60,
                                        "weapons": 20,          # changed
                                        "construction": 0},
                                    "Juggernaught Missile": {
                                        "hitChance": 80,        # changed
                                        "weapons": 16}         
                                    },
                    "scanner" : {"Eagle Eye Scanner": {
                                    "weapons": 0,
                                    "construction": 0,  
                                    "penScanRange": 500},       # changed
                                "Ferret Scanner": {
                                    "weapons": 0,
                                    "construction": 0,
                                    "penScanRange": 50}
                    }
                }

        tmpTree = self.gameTemplate.technologyTree(techDict)

        assert_true(len(tmpTree) > 6)   # should have entire standard list

        assert_not_equal(tmpTree, self.gameTemplate.technology) # some modifications

        assert_equal(tmpTree["Juggernaught Missile"]["weapons"], 16)
        assert_equal(tmpTree["Juggernaught Missile"]["hitChance"], 80)
        assert_equal(tmpTree["Beam Deflector"]["resources"], 548)
        assert_equal(tmpTree["Beam Deflector"]["weapons"], 18)
        assert_equal(tmpTree["Galaxy Scoop"]["warp10safe"], True)

    def test_technologyTree_OUCTT_Invalid(self):
        """ 'OnlyUseCustomTechTree' == invalid
        This means a standard Tech Tree value will be used.

        """ 
        techDict = {"OnlyUseCustomTechTree": 'ya da yada',
                    "mechanical" : { "Beam Deflector": {
                                        "weapons": 18,          # changed
                                        "construction": 6,
                                        "iron": 0,
                                        "electronics": 6,
                                        "biotechnology": 0,
                                        "resources": 548,      # changed
                                        "hasLRT": [],
                                        "propulsion": 0 }, 
                                    "Overthruster": {
                                        "weapons": 0,
                                        "construction": 0,
                                        "iron": 10}
                                    },

                    "torpedoes" : {"Delta Torpedo": {
                                        "hitChance": 60,
                                        "weapons": 20,          # changed
                                        "construction": 0},
                                    "Juggernaught Missile": {
                                        "hitChance": 80,        # changed
                                        "weapons": 16}          
                                    },
                    "scanner" : {"Eagle Eye Scanner": {
                                    "weapons": 0,
                                    "construction": 0,  
                                    "penScanRange": 500},       # changed
                                "Ferret Scanner": {
                                    "weapons": 0,
                                    "construction": 0,
                                    "penScanRange": 50}
                    }
                }

        tmpTree = self.gameTemplate.technologyTree(techDict)

        assert_not_equal(tmpTree["Juggernaught Missile"]["hitChance"], 80)
        assert_not_equal(tmpTree["Beam Deflector"]["resources"], 548)
        assert_not_equal(tmpTree["Beam Deflector"]["weapons"], 18)

        assert_equal(tmpTree["Juggernaught Missile"]["weapons"], 16)        
        assert_equal(tmpTree["Galaxy Scoop"]["warp10safe"], True)
  

        assert_equal(tmpTree, self.gameTemplate.technology) 

    def test_technologyTree_Custom_Standard(self):
        """
        techdict = {}
        techdict = {'OnlyUseCustomTechTree' = True}
        techdict = {'OnlyUseCustomTechTree' = False}
        techdict = {not empty but missing or invalid 'OnlyUseCustomTechTree'}

        techdict = {'CustomComponent'} & standard
        techdict = {'CustomComponent'} & OUCTT - True
        techdict = {'CustomComponent'} & OUCTT - False

        """ 
        
        techDict = {'customComponents' : 
                        {   "Overthruster" : 
                                    {"resources" : 500, "bor" : 55, 
                                    "mass" : 66, 'ability' : 2 },
                            "Brave Little Toaster" : 
                                    {"energy" : 5, "weapons" : 45, 
                                    "resources" : 88, 
                                    'name': "Brave Little Toaster" }
                }
                }

        tmpTree = self.gameTemplate.technologyTree(techDict)

        assert_not_equal(tmpTree, self.gameTemplate.technology)
        assert_true("Brave Little Toaster" in tmpTree)

        assert_equal(tmpTree["Overthruster"]["resources"], 500) 
        assert_equal(tmpTree["Overthruster"]["mass"], 66)
        assert_false('ability' in tmpTree["Overthruster"])

        assert_equal(tmpTree["Brave Little Toaster"]["weapons"], 45)

        assert_equal(tmpTree["Juggernaught Missile"]["weapons"], 16)        
        assert_equal(tmpTree["Galaxy Scoop"]["warp10safe"], True)       

    def test_technologyTree_Custom_OUCTT_True(self):
        """
        techdict = {}
        techdict = {'OnlyUseCustomTechTree' = True}
        techdict = {'OnlyUseCustomTechTree' = False}
        techdict = {not empty but missing or invalid 'OnlyUseCustomTechTree'}

        techdict = {'CustomComponent'} & standard
        techdict = {'CustomComponent'} & OUCTT - True
        techdict = {'CustomComponent'} & OUCTT - False

        """ 
        
        techDict = {'customComponents' : 
                        {   "Overthruster" : 
                                    {"resources" : 500, "bor" : 55, 
                                    "mass" : 66, 'ability' : 2 },
                            "Brave Little Toaster" : 
                                    {"energy" : 5, "weapons" : 45, 
                                    "resources" : 88, 
                                    'name': "Brave Little Toaster" }
                },

                "OnlyUseCustomTechTree": 'True',
                    "mechanical" : { "Beam Deflector": {
                                        "weapons": 6,
                                        "construction": 6,
                                        "iron": 0,
                                        "electronics": 6,
                                        "biotechnology": 0,
                                        "resources": 548,
                                        "hasLRT": [],
                                        "propulsion": 0 }, 
                                    "Overthruster": {
                                        "weapons": 0,
                                        "construction": 3,
                                        "iron": 10,
                                        "resources" : 8}
                                    },

                    "torpedoes" : {"Delta Torpedo": {
                                        "hitChance": 60,
                                        "weapons": 10,
                                        "construction": 0},
                                    "Juggernaught Missile": {
                                        "hitChance": 20,
                                        "weapons": 16}
                                    },
                    "scanner" : {"Eagle Eye Scanner": {
                                    "weapons": 0,
                                    "construction": 0,
                                    "penScanRange": 0},
                                "Ferret Scanner": {
                                    "weapons": 0,
                                    "construction": 0,
                                    "penScanRange": 50}
                    }
                }

        tmpTree = self.gameTemplate.technologyTree(techDict)

        assert_not_equal(tmpTree, self.gameTemplate.technology)
        assert_true("Brave Little Toaster" in tmpTree)

        assert_equal(tmpTree["Overthruster"]["resources"], 500) 
        assert_equal(tmpTree["Overthruster"]["mass"], 66)
        assert_equal(tmpTree["Overthruster"]["construction"], 3)
        assert_false('ability' in tmpTree["Overthruster"])
        assert_false('energy' in tmpTree["Overthruster"])


        assert_equal(tmpTree["Brave Little Toaster"]["weapons"], 45)
      
        assert_false("Galaxy Scoop" in tmpTree)    

        assert_true(len(tmpTree) == 7)   

        assert_false("Rhino Scanner" in tmpTree)
        assert_true("Eagle Eye Scanner" in tmpTree)
        assert_equal(tmpTree["Ferret Scanner"]["penScanRange"], 50)
        assert_equal(tmpTree["Beam Deflector"]["resources"], 548)

    def test_technologyTree_Custom_OUCTT_False(self):
        """
        techdict = {}
        techdict = {'OnlyUseCustomTechTree' = True}
        techdict = {'OnlyUseCustomTechTree' = False}
        techdict = {not empty but missing or invalid 'OnlyUseCustomTechTree'}

        techdict = {'CustomComponent'} & standard
        techdict = {'CustomComponent'} & OUCTT - True
        techdict = {'CustomComponent'} & OUCTT - False

        """ 
        
        techDict = {'customComponents' : 
                        {   "Overthruster" : 
                                    {"resources" : 500, "bor" : 55, 
                                    "mass" : 66, 'ability' : 2 },
                            "Brave Little Toaster" : 
                                    {"energy" : 5, "weapons" : 45, 
                                    "resources" : 88, 
                                    'name': "Brave Little Toaster" }
                },

                "OnlyUseCustomTechTree": 'False',
                    "mechanical" : { "Beam Deflector": {
                                        "weapons": 18,
                                        "construction": 6,
                                        "iron": 0,
                                        "electronics": 6,
                                        "biotechnology": 0,
                                        "resources": 548,
                                        "hasLRT": [],
                                        "propulsion": 0 }, 
                                    "Overthruster": {
                                        "weapons": 0,
                                        "construction": 3,
                                        "iron": 10,
                                        "resources" : 8}
                                    },

                    "torpedoes" : {"Delta Torpedo": {
                                        "hitChance": 60,
                                        "weapons": 10,
                                        "construction": 0},
                                    "Juggernaught Missile": {
                                        "hitChance": 80,
                                        "weapons": 16}
                                    },
                    "scanner" : {"Eagle Eye Scanner": {
                                    "weapons": 0,
                                    "construction": 0,
                                    "penScanRange": 0},
                                "Ferret Scanner": {
                                    "weapons": 0,
                                    "construction": 0,
                                    "penScanRange": 50}
                    }
                }

        tmpTree = self.gameTemplate.technologyTree(techDict)

        assert_not_equal(tmpTree, self.gameTemplate.technology)
        assert_true("Brave Little Toaster" in tmpTree)
        assert_equal(tmpTree["Brave Little Toaster"]["weapons"], 45)

        assert_equal(tmpTree["Overthruster"]["resources"], 500) 
        assert_equal(tmpTree["Overthruster"]["mass"], 66)
        assert_false('ability' in tmpTree["Overthruster"])
        
        assert_true('energy' in tmpTree["Overthruster"])
        assert_equal(tmpTree["Overthruster"]["construction"], 3)


        assert_equal(tmpTree["Juggernaught Missile"]["weapons"], 16)
        assert_equal(tmpTree["Juggernaught Missile"]["hitChance"], 80)
        assert_equal(tmpTree["Beam Deflector"]["resources"], 548)
        assert_equal(tmpTree["Beam Deflector"]["weapons"], 18)
        assert_equal(tmpTree["Galaxy Scoop"]["warp10safe"], True)

    def test_technologyTree_hull(self):

        tmpHulls = items_hulls()
        tmpHulls.update(items_starbases())

        for eachHull in tmpHulls:

            targetHull = self.gameTemplate.technology[eachHull]

            assert_true('slot' in targetHull)
            assert_true(len(targetHull['slot']) > 1)




class TestGameTemplate(object):

    def setup(self):
        print("TestGameTemplate: Setup")
        self.playerFileList = ['playerTest1', 'playerTest2', 'playerTest3']
        self.testGameName = "rabidTest"
        self.gameTemplate = game.StandardGameTemplate(self.testGameName, self.playerFileList)

    def teardown(self):
        print("TestGameTemplate: Teardown")

    def test_SGT_Contains_UniverseData(self):
        '''
        Validates the existance of specific keys in each universe dictionary. 
        The values are not validated. 

        '''

        tmpSGT = self.gameTemplate

        for uni in tmpSGT.universe_data:
            assert_in("UniverseSizeXY", uni)
            assert_in("UniverseName", uni)
            assert_in("UniverseNumber", uni)
            assert_in("UniversePlanets", uni)
            assert_in("Players", uni)

    def test_SGT_Contains_PlayerData(self):
        tmpSGT = self.gameTemplate

        players = tmpSGT.players_data

        assert_true(isinstance(players, list))
        assert(len(players) > 0)    # a game must have at least 1 player
        assert(len(players) == len(self.playerFileList))  
        






class TestGameTemplate_Multi(object):
    '''
    Test multiuniverse games


    '''
    def setup(self):
        print("TestGameTemplate_Multi: Setup")
        self.universe_count = 5
        self.universe_player = 3
        self.playerFileList = ['playerTest1', 'playerTest2', 'playerTest3']
        self.testGameName = "rabidTest"
        self.gameTemplate = game.StandardGameTemplate(self.testGameName, self.playerFileList, {}, self.universe_count)

    def teardown(self):
        print("TestGameTemplate_Multi: Teardown")

    
    def test_SGT_MultiUniverse(self):
        '''
        Tests the number of universes inside self.gameTemplate.universe_data
        the count should match. 
        '''

        tmp = self.gameTemplate.universe_data
        #tmp.universe_data = tmp.multiUniverse()
        x = self.universe_count - 1
        assert_true(len(tmp) > 1)
        assert_true(len(tmp) == self.universe_count)
        assert_true(x == int(tmp[x]['UniverseNumber']))
        print("UniverseNumber = %d" % (tmp[x]['UniverseNumber'],))
        assert_true(self.gameTemplate.universeNumber == self.universe_count)  
    
    def test_SGT_Contains_MultiUniverseData(self):
        '''
        Validates the existance of specific keys in each universe dictionary. 
        The values are not validated. 

        '''

        tmpSGT = self.gameTemplate

        for uni in tmpSGT.universe_data:
            assert_in("UniverseSizeXY", uni)
            assert_in("UniverseName", uni)
            assert_in("UniverseNumber", uni)
            assert_in("UniversePlanets", uni)
            assert_in("Players", uni)

    def test_SGT_Contains_TechTree(self):
        tech = self.gameTemplate.technology
        assert_true(isinstance(tech, dict))
        assert_true(len(tech) > 0)
  