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

from .tech import ShipDesign, Hull, Component


class PlayerDesigns(object):

    def __init__(self):

        self.currentShips = {}
        self.currentStarbases = {}



    def addDesign(self, newDesign):
        """
        Input: dict = { shipName, hullID, components, }
        Output: instantiates a new ShipDesign (from tech) and adds to the 
        appropriate dictionary.

        Current name uses shipName. May need a Unique ID.
        """

        # check that capacity has not been reached
        # check that name is not a duplicate

        # Instantiate ShipDesign
        # update values
        # check hull for starbase or ship
        # add to appropriate currentDict

        pass

    def removeDesign(self):
        pass

    def transferredDesign(self):
        """
        used if a design is transferred to a player. This method makes sure there
        is no name conflict. 
        """
        pass

    def designMiniaturization(self):
        """
        updates component values based on the tech level of a player. 

        """

        pass


