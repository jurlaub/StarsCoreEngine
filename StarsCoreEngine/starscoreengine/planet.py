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
        origHab = Tuple
        origConc = Tuple

    """
    def __init__(self, xy, ID, name, origHab = (90, 1.1, 65), origConc = (75, 75, 75)):
        super(Planet, self).__init__(xy, ID)
        self.name = name
        self.origHab = origHab
        self.origConc = origConc
        self.currHab = self.origHab
        self.currConc = self.origConc
        self.currSurfaceMinerals = 0  # (should be  3 values in a list)

        self.owner = None
        self.HW = False
        self.defenses = False
        self.scanner = False
        self.orbital = False
        self.prodQ = False   # this would be good to have as a seperate object for AR races and (future) none-planet starbase production
        self.population = 0




    def getOrigHab(self):
        #print ("%s" % (self.origHab))
        return self.origHab

    def getName(self):

        #print ("%s" % (self.name))
        return self.name

    def changeHab(self):
        pass

    def changeConc(self):
        pass

    def updateCurrentSurfaceMinerals(self):
        pass


class HabitablePlanet(Planet):
    """
        A seperate class for Habitable Planet seems helpful but at this point may be too complicated
    """
    pass    
