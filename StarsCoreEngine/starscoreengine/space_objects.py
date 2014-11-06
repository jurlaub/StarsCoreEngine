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
    may want to always return:
    (objectID, (x,y), speed, destinationID, (destinationX, destinationY)) 
    if immobile 
        destination relevant items set to None

""" 


class SpaceObjects(object):
    """
    SpaceObjects is the parent class of all objects in the universe. 
    (x,y) = current location
    speed = current speed (note for some this will always be '0' - unless there is a mod! :) ) 
    (destinationX, destinationY) = next targeted location
    newSpeed = new speed coming from orders (this speed will become 'speed'). 

    """

    def __init__(self, xy, ID):
        self.ID = ID
        self.xy = xy   # tuple (x,y)
        self.speed = 0
        self.destinationXY = self.xy  # tuple (x,y)
        self.newSpeed = self.speed


    def getID(self):
        return self.ID

    def getCurrentCoord(self):
        """ returns a tuple  """ 
        return self.xy

    def setCurrentCoord(self, xy):
        self.xy = xy

    def printCurrentCoord(self):
        print ("(x = %, y = %)" % (self.xy))

    def getDestinationCoord(self):
        """ returns a tuple """
        return self.destinationXY







class Minefields(SpaceObjects):
    """
        Minefield information here
    """
    pass




class PacketsAndSalvage(SpaceObjects):
    """ Salvage in Standard Stars are minerals that can be retrieved by any who are co-located. Velocity is 0.
        Packets in Standard Stars minerals combined at a base with a Mass Driver (see tech tree) with a velocity(~5-14) 
        that typically has a planet destination. 
    """
    def __init__(self, arg):
        super(PacketsAndSalvage, self).__init__()
        self.arg = arg
        


class WhereAmI(SpaceObjects):
    pass




class UniverseObject(object):

    def __init__(self, ID):
        self.ID = ID 
        self.planets = {}
        self.fleets = {}
        


