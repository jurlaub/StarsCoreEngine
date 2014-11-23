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

from .space_objects import SpaceObjects



class Planet(SpaceObjects):
    """ 
        Planet is the template that provides all the data available for a planet. 
        origHab = Tuple  --TODO-- change to individual variables
        origConc = Tuple --TODO-- change to individual variables

    """
    def __init__(self, xy, ID, name, origHab = (90, 1.1, 65), origConc = (75, 75, 75)):
        super(Planet, self).__init__(xy, ID)
        self.name = name
        self.origHab = origHab
        self.origConc = origConc
        self.currHab = self.origHab
        self.currConc = self.origConc
        self.currSurfaceMinerals = 0  # (should be  3 values in a list)
        
        self.HW = False
        self.owner = None  # may not keep here      

        self.factories = 0
        self.mines = 0
        self.defenses = 0



    def changeHab(self):
        pass

    def changeConc(self):
        pass

    def updateCurrentSurfaceMinerals(self):
        pass


class ColonizedPlanet(object):
    """ Requires a planet object    
    """
    def __init__(self, planet, population):
        self.planet = planet
        self.scanner = False
        self.orbital = False
        self.prodQ = False   # this would be good to have as a seperate object for AR races and (future) none-planet starbase production

        self.population = population

        #calculated values
        self.resources = 0
        self.planetValue = 1.0    # percentage 

    def calcResources(self):

        self.resources = 0
        pass

    def operatingFactories(self):
        '''
        Input: 
        returns the number of factories that can be run

        '''
        pass

    def operateMines(self):
        pass

    def populationGrowth(self):
        pass

    def colonyUninhabit(self):
        # self.planet.owner = None
        # damage to infrastructure?
        # self.resources = 0
        # self.population = 0
        # self.scanner = False
        # self.orbital = False
        # self.prodQ = False

        pass



