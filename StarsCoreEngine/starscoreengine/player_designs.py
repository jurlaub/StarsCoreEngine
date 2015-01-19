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
    """


    """

    def __init__(self, shipCap = 12):


        self.currentShips = {}
        self.currentStarbases = {}
        self.DesignCapacity = shipCap   # for ships. Starbases are the same?



    def addDesign(self, newDesign, techTree):
        """
        Input: dict = { shipName, hullID, components, }
        Output: instantiates a new ShipDesign (from tech) and adds to the 
        appropriate dictionary.

        Current name uses shipName. May need a Unique ID.

        Method NOT USED for a transferred design. Use transferDesign.

        """

        # check newDesign.hull for starbase or ship type
        # check that capacity has not been reached
        # check that name is not a duplicate

        # validate Technology level?  = No -> should be assessed at xFile Import level
        # validate PRT/LRT access?  = No   -> should be assessed at xFile Import level
        # ShipDesign Validates itself? = No   -> should be assessed at xFile Import level


        # Instantiate ShipDesign  
        # update values
        
        # add to appropriate currentDict

        pass

    @staticmethod
    def validDesignForProduction(newDesign, techTree, techLevel, PRT, LRT):
        """ 
        input: design (ShipDesign),techTree, techLevel, PRT, LRT
        
        
        validates: 
            Tech used is within tech Range
            Tech used is permitted per PRT
            Tech used is permitted per LRT


        output - returns:
            True = Design is valid for production 
            False = Design is not valid for production

        """
        pass



    def removeDesign(self):
        """ 
        Removing design can come in two ways.
        1) all built ships in game have been scrapped or destroyed
        2) deleting design will remove 'active' ships from gameplay

        !!!!!
        NOTE: part of the overall "remove Design" functionality will have to occur
        outside of this class - 
        !!!!!

        input: design to delete.
        output: the design is removed from the appropriate current dictionary
                any active ships are removed from the game
                    > perhaps immediately deleting active ships are not possible?
                      Deleting requires one turn?
                    > perhaps deleting active ships results in a salvage? 
                    
                    > all player's fleets are searched.
                        > any fleet with a token ShipDesign that matches design 
                          must be zeroed out. The token removed from the fleet.
                          If the fleet consists only of the token then the fleet
                          would be removed.
                    > other players' fleets may target the deleted fleet, at a 
                      minimum that order should be removed. (all orders searched
                        and all orders referencing that fleet should be removed)

                any references to active ships are removed from game



        Future: Possible that deleted design will end up in a 'history' dictionary

        """
        pass

    def transferDesign(self):
        """
        used if a design is transferred to a player. 

        This method makes sure there is no name conflict. 

        And tests to ensure that the user can build design - if not 
        ShipDesign.canOwnerBuild = False



        """
        pass




