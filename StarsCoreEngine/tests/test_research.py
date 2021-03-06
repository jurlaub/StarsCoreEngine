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
from nose.tools import with_setup, assert_equal, assert_not_equal, \
 assert_raises, raises, assert_in, assert_true, assert_false

# import unittest
from math import fabs


from ..starscoreengine import *
from ..starscoreengine.research import *



class TestResearchCosts(object):
    def test_cost_remaining(self):
        #tech level 1, no other tech, normal cost
        assert_true((fabs(cost_remaining(1, "normal", 0, 0) - 50) <= 1e-6))
        #tech level 1, no other tech, cheap cost
        assert_true((fabs(cost_remaining(1, "cheap", 0, 0) - 25) <= 1e-6))
        #tech level 1, no other tech, expensive cost
        assert_true((fabs(cost_remaining(1, "expensive", 0, 0) - 50*1.75) <= 1e-6))
        
        #tech level 1, 2 other techs, normal cost
        assert_true((fabs(cost_remaining(1, "normal", 2, 0) - 70) <= 1e-6))
        #tech level 1, 2 other techs, cheap cost
        assert_true((fabs(cost_remaining(1, "cheap", 2, 0) - 35) <= 1e-6))
        #tech level 1, 2 other techs, expensive cost
        assert_true((fabs(cost_remaining(1, "expensive", 2, 0) - 70 * 1.75) <= 1e-6))

        #tech level 2, 1 other techs, normal cost
        assert_true((fabs(cost_remaining(2, "normal", 1, 0) - 90) <= 1e-6))
        #tech level 2, 1 other techs, cheap cost
        assert_true((fabs(cost_remaining(2, "cheap", 1, 0) - 45) <= 1e-6))
        #tech level 2, 1 other techs, expensive cost
        assert_true((fabs(cost_remaining(2, "expensive", 1, 0) - 157.5) <= 1e-6))

        #tech level 2, 1 other techs, normal cost, some already spent
        assert_true((fabs(cost_remaining(2, "normal", 1, 50) - 40) <= 1e-6))
        #tech level 2, 1 other techs, cheap cost, some already spent
        assert_true((fabs(cost_remaining(2, "cheap", 1, 50) + 5) <= 1e-6))
        #tech level 2, 1 other techs, expensive cost, some already spent
        assert_true((fabs(cost_remaining(2, "expensive", 1, 50) - 107.5) <= 1e-6))

    def test_cost_remaining_error(self):
        assert_raises(ValueError, cost_remaining, 2, "fish", 1, 50)


class TestStartTech(object):
    def setUp(self):
        self.baseTechLevels = {
            "energy" : 0, 
            "weapons" : 0,
            "propulsion" : 0,
            "construction" : 0,
            "electronics" : 0,
            "biotechnology" : 0
          }


    def test_startTech_JOAT1(self):
        #JOAT - 3 in all
        JOAT_calc = Research("JOAT", [])
        for k in self.baseTechLevels.keys():
            self.baseTechLevels[k] = 3
        assert_equal(JOAT_calc.techLevels, self.baseTechLevels)

    def test_startTech_JOAT2(self):
        #JOAT - 3 in all, prop 4
        JOAT_calc = Research("JOAT", ["CE"])
        for k in self.baseTechLevels.keys():
            self.baseTechLevels[k] = 3
        self.baseTechLevels["propulsion"] = 4
        assert_equal(JOAT_calc.techLevels, self.baseTechLevels)


    def test_startTech_JOAT3(self):
        #JOAT - 3 in all, prob 4
        JOAT_calc = Research("JOAT", ["IFE"])
        for k in self.baseTechLevels.keys():
            self.baseTechLevels[k] = 3
        self.baseTechLevels["propulsion"] = 4
        assert_equal(JOAT_calc.techLevels, self.baseTechLevels)


    def test_startTech_JOAT4(self):
        #JOAT - 3 in all, prop 5
        JOAT_calc = Research("JOAT", ["IFE", "CE"])
        for k in self.baseTechLevels.keys():
            self.baseTechLevels[k] = 3
        self.baseTechLevels["propulsion"] = 5
        assert_equal(JOAT_calc.techLevels, self.baseTechLevels)
        
    # def test_startTech_wrongPTR(self):
    #     self.assertRaises(TypeError, Research())

    def test_startTech_HE1(self):
        tmpHE = Research("HE")
        assert_equal(tmpHE.techLevels, self.baseTechLevels)

    def test_startTech_HE2(self):
        self.baseTechLevels["propulsion"] = 1
        tmpHE = Research("HE", ["IFE"])
        assert_equal(tmpHE.techLevels, self.baseTechLevels)




class TestSpeciesTechFieldsCost(object):
    def test_species_editor_costs1(self):
        #all normal, box not ticked
        assert_equal(0, species_editor_tech_costs(0, 0, False))

    def test_species_editor_costs2(self):
        #all normal, box ticked
        assert_equal(-60, species_editor_tech_costs(0, 0, True))

    def test_species_editor_costs3(self):
        #3 exp, 3 cheap,  box ticked
        assert_equal(-60, species_editor_tech_costs(3, 3, True))

    def test_species_editor_costs4(self):
        #1 exp, box ticked
        assert_equal(-60 + -49, species_editor_tech_costs(1, 0, True))

    def test_species_editor_costs5(self):
        #1 cheap, box ticked
        assert_equal(-60 + 43, species_editor_tech_costs(0, 1, True))
