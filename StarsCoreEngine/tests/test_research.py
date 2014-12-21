
from ..starscoreengine import *
from ..starscoreengine.research import *
import unittest
from math import fabs

class TestResearch(unittest.TestCase):
    def setUp(self):
        pass


    def test_cost_remaining(self):
        #tech level 1, no other tech, normal cost
        self.assertTrue((fabs(cost_remaining(1, "normal", 0, 0) - 50) <= 1e-6))
        #tech level 1, no other tech, cheap cost
        self.assertTrue((fabs(cost_remaining(1, "cheap", 0, 0) - 25) <= 1e-6))
        #tech level 1, no other tech, expensive cost
        self.assertTrue((fabs(cost_remaining(1, "expensive", 0, 0) - 50*1.75) <= 1e-6))
        
        #tech level 1, 2 other techs, normal cost
        self.assertTrue((fabs(cost_remaining(1, "normal", 2, 0) - 70) <= 1e-6))
        #tech level 1, 2 other techs, cheap cost
        self.assertTrue((fabs(cost_remaining(1, "cheap", 2, 0) - 35) <= 1e-6))
        #tech level 1, 2 other techs, expensive cost
        self.assertTrue((fabs(cost_remaining(1, "expensive", 2, 0) - 70 * 1.75) <= 1e-6))

        #tech level 2, 1 other techs, normal cost
        self.assertTrue((fabs(cost_remaining(2, "normal", 1, 0) - 90) <= 1e-6))
        #tech level 2, 1 other techs, cheap cost
        self.assertTrue((fabs(cost_remaining(2, "cheap", 1, 0) - 45) <= 1e-6))
        #tech level 2, 1 other techs, expensive cost
        self.assertTrue((fabs(cost_remaining(2, "expensive", 1, 0) - 157.5) <= 1e-6))

        #tech level 2, 1 other techs, normal cost, some already spent
        self.assertTrue((fabs(cost_remaining(2, "normal", 1, 50) - 40) <= 1e-6))
        #tech level 2, 1 other techs, cheap cost, some already spent
        self.assertTrue((fabs(cost_remaining(2, "cheap", 1, 50) + 5) <= 1e-6))
        #tech level 2, 1 other techs, expensive cost, some already spent
        self.assertTrue((fabs(cost_remaining(2, "expensive", 1, 50) - 107.5) <= 1e-6))

    def test_cost_remaining_error(self):
        self.assertRaises(ValueError, cost_remaining, 2, "fish", 1, 50)
