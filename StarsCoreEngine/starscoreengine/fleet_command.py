"""
    This file is part of Stars Core Engine, which provides an interface and processing of Game data.
    Copyright (C) 2016  <Joshua Urlaub + Contributors>

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

from .fleets import Fleets


DEBUG = True
DEBUG2 = False


class FleetCommand(object):
    """
    Includes xFile processing, Fleet Orders, Fleet Logistics.

    """

    def __init__(self, player, multiverse):
        self.multiverse = multiverse #fleets are objects in a given universe
        self.player = player
        self.currentFleetID = 0    

        self.fleets = {}  # ? fleetID : fleetObj





    def generateFleetID(self):
        """
        precondition:   fleetIDs do not have a universe ID prefixed to currentFleetID -which should be unique across all universes

        postcondition:  fleetID should not exceed fleet number ceiling
                        fleetID should not have a duplicate
                        self.currentFleetID should provide the next open fleetID

        Note: 20161228 ju - do not like this way of generating ID's


        """

        fleetID = self.currentFleetID
        
        #test that fleetID is not in self.fleets 
        if self.currentFleetID in self.fleets:
            fleetID = self._nextFleetID()

            print("generateFleetID - %s in self.fleets  nextFleetID: %s" % (self.currentFleetID, fleetID))
            #--TODO-- test that fleetID does not exceed fleet cap


        # find next open FleetID in sequence, starting from currentFleetID
        else:
            # fleetID uses current fleetID

            #find the next fleetID
            self.currentFleetID = self._nextFleetID(self.currentFleetID)
            print("generateFleetID - %s " % self.currentFleetID)


        # fleetID = str(self.player.playerNumber) + "_" + self.currentFleetID
        
        return fleetID

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

        print("_nextFleetID: fleetKeys:%s" % fleetKeys) 
        return fleetKeys




    def removeFleet(self, fleetID):
        """
        precondition:   fleetID is a valid fleetID


        """

        if fleetID in self.fleets:
            
            #
            if fleetID < self.currentFleetID and fleetID > -1:
                self.currentFleetID = fleetID

            del self.fleets[fleetID]


    def addFleet(self, newFleetID, newFleet):
        """

        """

        self.fleets[newFleetID] = newFleet   



    def createFleet(self):
        pass
        
