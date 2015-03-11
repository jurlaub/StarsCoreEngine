"""
    This file is part of Stars Core Engine, which provides an interface and processing of Game data.
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

        #needs to pull its value from self.waypoints?
        self.destinationXY = self.xy  # tuple (x,y)
        self.newSpeed = self.speed

        #need to be able to store waypoints (with speed), and then to know what the waypoints are (need to figure out howto do intercepts)
        self.waypoints = None #[((x,y), speed), (other_space_object, speed)...
        
        #perhaps sort fleets by waypoint type, if type of next waypoint (of fleet A) is static (x, y) then fleet A can move easily,
        #then a following intercept fleet (B) can move to the new location of fleet A. 
        #What to do if A is following B, B is following C and C is following A - no way to know which to resolve first - not sure how Stars! does it now
        #could do it iteratively, store the objects origional coords and then move each one 1 ly towards its target, 
        #eventually:
        #   all three will have moved as far as they can towards one another,
        #   two will meet, and the third will have a fixed target
        #   three will meet 

    def printCurrentCoord(self):
        print ("(x = %, y = %)" % (self.xy))








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




# class UniverseObject(object):

#     def __init__(self, ID):
#         self.ID = ID 
#         self.planets = {}
#         self.fleets = {}
        


