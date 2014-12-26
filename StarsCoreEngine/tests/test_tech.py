from ..starscoreengine import *
from ..starscoreengine.tech import *
import unittest
from math import fabs

class TestTech(unittest.TestCase):
    def test_order(self):
        tech = order_tech()
        self.assertEqual(tech["shields"]["Croby Sharmor"], {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 4, 
                                                            "electronics" : 0, "biotechnology" : 0, "mass" : 10, "resources" : 15, 
                                                            "iron" : 7, "bor" : 0, "germ" : 4, "DP" : 60, "hasPRT" : ["IS"], "hasLRT" : [], "notLRT" : []})
        self.assertNotEqual(tech["shields"]["Croby Sharmor"], {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 4, 
                                                            "electronics" : 0, "biotechnology" : 0, "mass" : 10, "resources" : 15, 
                                                            "iron" : 7, "bor" : 0, "germ" : 4, "DP" : 60, "hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []})
