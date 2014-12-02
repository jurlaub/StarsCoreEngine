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



# flyweight pattern?  

# is there a way to dynamically add parent classes to a class? 
# !!!! is there a way to send code along with 'JSON' data to the client? 
#   I believe so. This may not be preferred but may be something to consider.
#   answer the fuel calculation problem, the ship design update component problem. 

'''
Note: 

a composite design pattern 

would solve the problem of tech which acts like multiple components. (i.e. like 
the Mystery Trader parts. A Multi-contained Munition is a beam weapon that 
bombs planets and lays mines, etc) Such components could be added together in 
composite form. The problem with this is the StarsCoreEngine passes its data via
JSON files. Any 'fancy' composite design would be wasted when its data is 
aggregated into JSON form and passed to the client. 

Were this not the case, then the composite design pattern would be used to assemble
the components (especially the multi-type/multi-class ones). The components 
would be used by a flyweight design pattern.

Ultimately, it appears that the JeffMC approach is the simplest.  


'''


class BaseTech(object):
    
    def __init__(self, ID):
        self.itemID = ID
        self.name = None            # tech object name (game name for object)
        self.itemType = None

        # Costs
        self.iron= None
        self.bor = None
        self.germ = None
        self.resources = None

        # Some witty 'Mass' related grouping
        self.mass = None
        # Tech Requirements
        self.ener = None
        self.weap = None
        self.prop = None
        self.con = None 
        self.elec = None
        self.bio = None


        self.raceRequirement = None
        self.special = None
        self.restrictions = None


        self.initative = None
        self.cloaking = None
        self.battleMovement = None
        self.cargo = None
        self.fuelGeneration = None




class Engines(BaseTech):

    def __init__(self):
        self.optimalSpeed = 0
        self.freeSpeed = 0
        self.safeSpeed = 0

        self.radiation = False


class Weapon(BaseTech):
    ''' Weapons - both Beam & Torpedos
    '''

    def __init__(self):
        self.range = None
        self.power = None
        self.minesSwept = 0
        self.accuracy = 0

class Bombs(BaseTech):

    def __init__(self):
        self.popKillPercent = .06
        self.minKill = 300
        self.installations = 2



class MineLayer(BaseTech):

    def __init__(self):
        self.miningRate = 0

        self.terraform = False

class Electrical(BaseTech):

    def __init__(self):
        self.tachyon = None
        self.deflection = None
        self.beamDamage = None


class Orbital(BaseTech):

    def __init__(self):
        self.safeMass = 0
        self.safeRange = 0

        self.warpSpeed = 0

class PlanetaryInstallations(BaseTech):

    def __init__(self):
        self.range = None
        self.pen = None

        self.defenses40 = 33
        self.defenses80 = 55


class Terraforming(BaseTech):
    """docstring for Terraforming"""
    def __init__(self):
        super(Terraforming, self).__init__()
        self.modGrav  = None
        self.modTemp = None
        self.modRad = None

        
        

class Mechanical(BaseTech):

    def __init__(self):
        self.beamDeflector = None
        self.movement = None
        self.extraFuel = None
        self.extraCargo = None
        self.fuel = None
        self.colonizer = None
    


class Scanner(BaseTech):
    
    def __init__(self):
        self.range = None
        self.pen = None
        self.stealFromShips = False   
        self.stealFromPlanets = False




class Armor(BaseTech):

    def __init__(self):
        self.armor = 0

class Shields(BaseTech):

    def __init__(self):
        self.shield = 0



class Hull(BaseTech):

    def __init__(self):
        self.designName = None  # user specified ship design name
        self.shipType = None    # Miner, Transport, Armed, ect.

        
        self.armor = 100
        self.fuelCapacity = 500
        
        self.mineLayerDouble = False
        self.shipsHeal = False

        self.ARPopulation = None
        self.spaceDock = None


        # slot defines the hull component composition
        self.slot = {"A":{"engine":1}, "B":{"objectType":"number_of_slots"}}  # each key == specific slot, value is

        # identify slots:
        #   slot type -> General, Engine, Weap, Mech, Elect, etc
        #   how many slots available

        # specify all ship related question?


class ShipDesign(Hull):
    ''' ShipDesign is a specific user defined design of the Hull class 
    '''

    def __init__(self, hullID):
        self.hullID = hullID # points to a Hull object. there is one for each type of ship.
        # component holds the number of items assigned to a design
        self.component = {"A":["itemID", "itemID"], "B":["itemID", "itemID", "itemID"]}  # capacity



    def componentDict(self, key, value):

        '''
        if key is electrical:
            update the ship designs electrical object values?
            update BaseTech values + objects values?
        '''
        pass








