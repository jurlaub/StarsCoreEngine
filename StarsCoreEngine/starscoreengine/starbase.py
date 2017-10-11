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
from .fleets import FleetObject

class Starbase(FleetObject):
    """
    postcondition:  ID sent to space_objects super must prepend "playernumber_" to currentFleetID
                    Starbases must register with UniverseObject.objectsAtXY
                    Starbases must be connected to Planet (not Colony) object

    """

    def __init__(self, player, spaceObjectID, xy, universeID, planetID):
        super(Starbase, self).__init__(player, spaceObjectID, xy, universeID)
        # self.player = player  #owning player
        # self.currentUniverseID = universeID   # current universe,  obtained from ProductionQ location
        # self.objectID = spaceObjectID  #this is "playernumber_" + currentFleetID (i.e. FleetKey for player ) !! must change if FleetKey changes
        
        self.planetID = planetID
        self.starbase = False
        self.constructionCapacity = None # None or Mass Rating 
    

                   
    def starbaseMassRating(self):
        """
        searchs through all the tokens 
        returns maximum mass ship build rating that a starbase can build. 

        """

        #starbaseTokenIDs = [x for x.design in self.tokens.values()]
        massRating = '0'
        dockSizes = ['0', '200', 'infinite']

        for each in self.tokens:

            starbase = self.player.designs.currentStarbases[each]
            
            if starbase.spaceDockSize != None:
                massRating = str(starbase.spaceDockSize)
            # if starbase.spaceDockSize in dockSizes:
                # if dockSizes.index(massRating) < dockSizes.index(starbase.spaceDockSize):
                #     massRating = starbase.spaceDockSize
            print("fleets.starbaseMassRating - %s: spaceDockSize:%s" % (each, starbase.spaceDockSize))
            print("%s" % starbase)
            
        return massRating
                    
