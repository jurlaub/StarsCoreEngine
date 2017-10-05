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

from .fleets import FleetObject
from .fleet_orders import FleetOrders


DEBUG = True
DEBUG2 = False


class FleetCommand(object):
    """
    Includes xFile processing, Fleet Orders, Fleet Logistics.

    """

    def __init__(self, player, multiverse):
        self.multiverse = multiverse # fleets are objects in a given universe
        self.player = player
        self.nextFleetID = 0    

        self.fleets = {}  # ? fleetID : fleetObj





    def generateFleetID(self):
        """
        precondition:   fleetIDs do not have a universe ID prefixed to nextFleetID -which should be unique across all universes

        postcondition:  fleetID should not exceed fleet number ceiling
                        fleetID should not have a duplicate
                        self.nextFleetID should provide the next open fleetID

        Note: 20161228 ju - do not like this way of generating ID's


        """

        #fleetID = self.nextFleetID
        
        # if nextFleetID has been used, then advance to the next open fleet id
        # if self.nextFleetID in self.fleets:
            
        #     # fleetID = self._nextFleetID()
            
        #     self.nextFleetID = self._nextFleetID()

        #     # if DEBUG: print("generateFleetID - %s in self.fleets  nextFleetID: %s" % (self.nextFleetID, fleetID))
        #     if DEBUG: print("generateFleetID - %s in self.fleets  nextFleetID: %s" % (self.nextFleetID, self._nextFleetID()))
        #     #--TODO-- test that fleetID does not exceed fleet cap
        #     # return fleetID




        # # find next open FleetID in sequence, starting from nextFleetID
        # else:
        #     # fleetID uses current fleetID

        #     #find the next fleetID
        #     #self.nextFleetID = self._nextFleetID(self.nextFleetID)
        #     self.nextFleetID = self._nextFleetID()
            
        #     if DEBUG: print("generateFleetID - %s " % self.nextFleetID)

        #     return self.nextFleetID

        # fleetID = str(self.player.playerNumber) + "_" + self.nextFleetID
        
        #return fleetID
        # return self.nextFleetID
        return self._nextFleetID()

    def _nextFleetID(self, startingID = 0):
        """
        search through the dictionary to find the next open fleet number.

        postcondition:  should return next open fleetID ( 0...n )


        """

        fleetKeys = 0
        valueInRange = True

        for i in range(startingID, len(self.fleets)):
            print("_nextFleetID: %s  fleet len(%s)" % (i, len(self.fleets)))
            

            if i not in self.fleets:
                print("_nextFleetID: False %s is not in self.fleets" % i)
                fleetKeys = i
                valueInRange = False
                break

        if valueInRange:
            fleetKeys = len(self.fleets)
            print("_nextFleetID: valueInRange is True %s is not in self.fleets" % (fleetKeys))

        if DEBUG: print("[p%s]_nextFleetID: fleetKeys:%s" % (self.player.playerNumber, fleetKeys) ) 
        return fleetKeys




    def removeFleet(self, fleetID):
        """
        precondition:   fleetID is a valid fleetID


        """

        if fleetID in self.fleets:
            
            #
            if fleetID < self.nextFleetID and fleetID > -1:
                self.nextFleetID = fleetID

            del self.fleets[fleetID]


    def addFleetOrders(self, newFleetID, newFleetOrders):
        """

        """

        self.fleets[newFleetID] = newFleetOrders   



    def addFleet(self, newFleetID, newFleet):

        if newFleetID not in self.fleets:
            self.fleets[newFleetID] = newFleet
            self.nextFleetID = self._nextFleetID()
        
        else:
            print("error - duplicate fleet ID: new fleet not added")

        
        
