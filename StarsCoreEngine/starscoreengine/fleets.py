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

    use a dictionary of (x,y,z) coords along with space object id's to collect locations and other data

    d = {}
    l = d.setdefault((25,45), [])   # it returns the list associated with the first value or a new list
    l.append(355)
    l.append(655)

    
    Removing a fleet occurs at the level above Fleet. Typically a player, but also a universe?




"""


from .space_objects import SpaceObjects




class Token:
    """Ships of the same design in a fleet form a single token, contains everything needed
    for the battles, needs to persist after battles to keep damage"""

    def __init__(self, shipDesign, numbers, damage = 0):
        self.design = shipDesign
        self.number = numbers
        #list of [[number, damage (%)], ..., so [100, 0.5], [100, 0] is a token of 200 ships, 100 of which have 50% damage
        self.damage = damage  
       
        #used in battle
        self.armor = None
        self.shields = None
        #modified every turn in battle
        self.mass = None


    





class FleetObject(SpaceObjects): #  additionally subclass Component? 
    """
        Fleets -    can exist as a single ship. 
                

        postcondition:  ID sent to space_objects super must prepend "playernumber_" to currentFleetID
                        objectID must change if player FleetKey changes


        FleetObjects extend SpaceObjects. They exist in an UniverseObject. A player owns a FleetObject 
        and a Players FleetCommand controls via FleetOrders. (The FleetOrders step may be unnecessary)


    """

    def __init__(self, player,  spaceObjectID, xy, universeID):
        super(FleetObject, self).__init__(xy, spaceObjectID)
        self.player = player  #owning player
        self.currentUniverseID = universeID   # current universe,  obtained from ProductionQ location
        # self.objectID = spaceObjectID  #this is "playernumber_" + currentFleetID (i.e. FleetKey for player ) !! must change if FleetKey changes

        self.fleetOrderNumber = None

        #self.tokens = {}
        self.fuel_capacity = 0
        self.fuel_availiable = 0
        self.cargo_mass = 0
        self.cargo_capacity = 0
        self.cloaking = 0
        self.raceFuelEfficiency = self.player.raceData.fuelEfficiency

    def setCapacities(self):
        self.fuel_capacity = 0
        self.cargo_capacity = 0
        for t in self.tokens:
            self.fuel_capacity += t.design.fuel_capacity * t.number
            self.cargo_capacity += t.design.cargo_capacity * t.number
        
    def move(self):
        pos = self.xy
        tgtPos = self.destinationXY
        distance = math.sqrt((tgtPos[0] - pos[0]) **2 + (tgtPos[0] - pos[0]) **2)
        #can make it in one year
        if self.speed ** 2 <= math.ceil(distance):
            return distance
        else:
            return self.speed ** 2

    def calculateFuelUsePerLY(self):
        fuelUsed = 0
        mg_coeff = 0.0005
        #no cargo, just use design mass
        if self.cargoMass == 0:
            for t in self.tokens:
                fuelUsed += t.mass * t.design.fuelEfficiency[self.speed] * self.raceFuelEfficiency * mg_coeff 
        #full of cargo, use design mass + cargo capacity for every ship
        elif self.cargoMass == self.cargoCapacity:
            for t in self.tokens:
                fuelUsed += (t.cargo_capacity + t.mass) * t.design.fuelEfficiency[self.speed] * self.raceFuelEfficiency * mg_coeff
        #partially loaded, arrange cargo between ships to use the least fuel, so fill the most efficient ships first
        else:
            def _sortByFuelEff(self, token):
                return token.design.fuelEfficiency[self.speed]

            #should sort tokens by fuel efficiency at this speed, so that cargo is distributed over the most fuel efficient ships
            self.tokens = sorted(self.tokens, key=_sortByFuelEff)
            for t in self.tokens:
                #no cargo capacity or no cargo left
                if t.cargo_capacity == 0 or self.cargoMass == 0:
                    fuelUsed = t.mass * t.design.fuelEfficiency[self.speed] * self.raceFuelEfficiency * mg_coeff 

                #more cargo than will fit in this token, fill it up
                elif self.cargoMass > t.cargo_capacity:
                    self.cargoMass -= t.cargo_capcacity
                    fuelUsed += (t.cargo_capacity + t.mass) * t.design.fuelEfficiency[self.speed] * self.raceFuelEfficiency * mg_coeff

                #cargo will fit in token - partially or completely fill it
                elif self.cargoMass > 0:
                    fuelUsed += (self.cargoMass + t.mass) * t.design.fuelEfficiency[self.speed] * self.raceFuelEfficiency * mg_coeff
                    self.cargoMass = 0



    # def updateTokens(self, quantity, designID):

    #     for each in self.token:


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
    

                    
                    
