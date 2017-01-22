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

from .tech import ShipDesign, Hull, Component


class PlayerDesigns(object):
    """


    """

    def __init__(self, raceName, techLevels, LRT, shipCap = 12):

        self.DesignCapacity = shipCap   # for ships. Starbases are the same?
        self.raceName = raceName
        self.techLevels = techLevels
        self.LRT = LRT


        self.currentShips = {}
        self.currentStarbases = {}
        




    def addDesign(self, newDesign, techTree):
        """
        Input: newDesign = { shipName, hullID, components, }
        Output: 
            > instantiates a new ShipDesign (from tech) and adds to the 
            appropriate dictionary. 
            > if name already exists, existing design stays and method returns None
            > if itemType is not 'Ships' or 'Starbases' method returns None
            > if capacity is > DesignCapacity, method returns None

        Starbase and Ship names must be Unique 

        Current name uses shipName. May need a Unique ID.

        Method NOT USED for a transferred design. Use transferDesign.

        """

        
        tmpName = newDesign['designName']

        tmpHull = newDesign['hullID']
        tmpType = techTree[tmpHull].itemType    # should be Ships or Starbases


        if tmpType not in ('Ships', 'Starbases'):
            # raise TypeError("Attempted to add a design, but the design did not specify 'Ships' or 'Starbases'")
            return None

        elif newDesign['designName'] in self.currentShips:          #designName must be unique in both ships and starbases
            # Log message
            return None

        elif newDesign['designName'] in self.currentStarbases:      #designName must be unique in both ships and starbases
            # Log message
            return None

        elif tmpType == 'Ships':
            if len(self.currentShips) >= int(self.DesignCapacity):
                # Log message
                return None

            x = self.currentShips


        elif tmpType == 'Starbases':
            if len(self.currentStarbases) >= int(self.DesignCapacity):
                # Log message
                return None


            x = self.currentStarbases


        else:                # don't expect this to be reached
            print("Error in PlayerDesigns.addDesign()")
            return None


        
        newObject = ShipDesign(newDesign, techTree, self.techLevels, self.LRT) 
        newObject.owner = self.raceName      
        
        x[tmpName] = newObject  # x == self.currentShips or self.currentStarbases  

        
    # --------------- method should be in the tech file -----------
    # @staticmethod
    # def validDesignForProduction(newDesign, techTree, techLevel, PRT, LRT):
    #     """ 
    #     input: design (ShipDesign),techTree, techLevel, PRT, LRT
        
        
    #     validates: 
    #         Tech used is within tech Range
    #         Tech used is permitted per PRT
    #         Tech used is permitted per LRT


    #     output - returns:
    #         True = Design is valid for production 
    #         False = Design is not valid for production

    #     """
    #     pass



    def removeDesign(self, designName):
        """ 
        Removing design can come in two ways.
        1) all built ships in game have been scrapped or destroyed & user deletes entry
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
        if designName in self.currentShips:
            self.currentShips.pop(designName)
        elif designName in self.currentStarbases:
            self.currentStarbases.pop(designName)
        
        else:
            print("Design not present")




    def transferDesign(self):
        """
        used if a design is transferred to a player. 

        This method makes sure there is no name conflict. 

        And tests to ensure that the user can build design - if not 
        ShipDesign.canOwnerBuild = False



        """
        pass


    def buildList_Ship(self):

        # call buildList_PlayerDesign
      

        pass

    def buildList_Starbase(self):



        pass


    def buildList_PlayerDesign(self, currentDesign, listType):
        """ 
        staticmethod?

        input:
            currentDesign ==> dictionary of {shipNames: ShipDesign_objects}; 
            listType ==> Ships or Starbases

        output: 
            buildList of ships or starbases that are valid to produce
                key = name
                value = {costs, mass}

        """

        #iterate through the dictionary
        ## is it a valid design to build?
        ### if not skip
        ## obtain the current costs
        ## assemble and return

        buildList = {}


        for designName, designObj in currentDesign.items():
            
            # validate capability - are tech levels now sufficient to build? if so update designValidFor Production 

            if not designObj.designValidForProduction: # cannot build, so do not add to BuildList
                continue


            # current costs for design
            currentCosts = None  # from ShipDesign



            # add to dictionary
            # add list type


        return buildList




