"""
    This file is part of Stars Core Engine, which provides an interface and processing of Game data.
    Copyright (C) 2017  <Joshua Urlaub + Contributors>

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

from .space_objects import SpaceObjects

import random


DEBUG_1 = False
DEBUG_2 = False

class Planet(SpaceObjects):
    """ 
        Planet is the template that provides all the data available for a planet. 


    """
    def __init__(self, xy, ID, name, universe,  origHab = (1.1, 90, 45), origConc = None):
        super(Planet, self).__init__(xy, ID)
        self.name = name    
        self.origHab = origHab              #depreciate
        self.origGrav = origHab[0]
        self.origTemp = origHab[1]
        self.origRad = origHab[2]

        self.currHab = self.origHab         # depreciate
        self.currentTemp = self.origTemp
        self.currentGrav = self.origGrav
        self.currentRad = self.origRad

        self.universe = universe

        #detail current Concentration, random by default
        if not origConc: 
            self.concIron = random.randint(1,135)
            self.concBor = random.randint(1,135)
            self.concGerm = random.randint(1,135)
        else:
            self.concIron = origConc[0]
            self.concBor = origConc[1]
            self.concGerm = origConc[2]
        


        self.currSurfaceMinerals = 0  # depreciate  (should be  3 values in a list)
        self.surfaceIron = 0
        self.surfaceBor = 0
        self.surfaceGerm = 0


        self.HW = False
        self.owner = None       

        #--TODO-- planetary population needs to be here.
        self.orbitalStarbase = None     # Starbase object

        self.factories = 0
        self.mines = 0
        self.defenseValue = 0





    def changeHab(self):
        pass

    def changeConc(self, concIron, concBor, concGerm):
        #set concentrations to new values, perhaps best to let the mines\mining fleets decide how much and have them set the values?
        self.concIron = concIron
        self.concBor = concBor
        self.concGerm = concGerm


    def addSurfaceMinerals(self, minerals):
        self.surfaceIron += minerals[0]
        self.surfaceBor += minerals[1]
        self.surfaceGerm += minerals[2]

    def removeSurfaceMinerals(self, minerals):
        """
        Removes the specified number of minerals from currSurfaceMinerals

        precondition: minerals exist on the surface, the amount specified will 
                    not cause the surface minerals to go negative.
                    assumes minerals is a valid amount to be removed 

        input: [minerals]
        output: self.surfaceminerals is updated


        """
        self.surfaceIron -= minerals[0]
        self.surfaceBor -= minerals[1]
        self.surfaceGerm -= minerals[2]

    def getSurfaceMinerals(self):      
        return [self.surfaceIron, self.surfaceBor, self.surfaceGerm]

    def getPrefex(self):

        return int(self.ID[0])


