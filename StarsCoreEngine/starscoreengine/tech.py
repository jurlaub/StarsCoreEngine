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

"""
Note - musings on:

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


"""

# Note: to speed up tech consider using NamedTuples in the tech class

"""
Design: from Template to Tech Game Object.

-*- Game: ------------------------------------------

At the core of technology will be a class object that captures all 
values related to each tech item. (like JeffMC describes)


-*- Setup (Template): ------------------------------------------

Custom designs will feed this class. (this can be done smartly or naively)
naively - one large dict per tech with all questions (includes items that
    may not relate to component)
smartly - objects added to dictionary that address item + type specific
     questions. Smaller and compact description 

-*- Interface: ------------------------------------------

Basic Tech will be contained as a tech dictionary in the .xy file. This is
    the tech source for the client. The user (player) can access the tech
    tree and see component details.
    Grouped by Type: Key = "type" : Value = { 'components of that type',
                            'Key = itemName : Value = Component object'}

The user (player) can also create starbases & ships from those components,
    based on the hull's accessible at the users tech level.

Designs are stored within each player's object. Designs are communicated
    to the client via the players .m file.  Because a players fleet 
    and production need ready access to the design.  


Intel: designs revealed based on scanning and combat. Intel stored with
    each player. 


"""

"""
Alternative:




"""

''' technology & game Setup options
Template Options
1) use standard game tech Template
2) modify existing game technology components
    a) add components to standard game tech Template
    b) remove (disable) standard technology
3) use a completely different tech tree

Custom Tech Options
1) custom tech setup = save standard tech tree to file
    a) Note: in dict add a key that specifies the function of the custom file
        - use instead of the standard tech tree
        - modify existing tech tree







'''


class CoreStats(object):

    def __init__(self):
            # Costs
        self.iron= 0
        self.bor = 0
        self.germ = 0
        self.resources = 0

        # Some witty 'Mass' related grouping
        self.mass = 0
        self.initative = None
        self.cloaking = None
        self.battleMovement = None

# class TechReq(object):
#     def __init__(self):
#         # Tech Requirements
#         self.ener = 0
#         self.weap = 0
#         self.prop = 0
#         self.con = 0 
#         self.elec = 0
#         self.bio = 0 

class BaseTech(CoreStats):
    
    def __init__(self):
        super(BaseTech,self).__init__()
        self.name = None            # tech object name (game name for object)
        self.itemType = None

        # Tech Requirements
        self.ener = 0
        self.weap = 0
        self.prop = 0
        self.con = 0 
        self.elec = 0
        self.bio = 0

        self.raceRequirement = None
        self.special = None
        self.restrictions = None
        self.fuelGeneration = None

     



class Engines(object):

    def __init__(self):
        self.optimalSpeed = None
        self.freeSpeed = None
        self.safeSpeed = None
        self.radiation = False



class Weapons(object):
    ''' Weapons - both Beam & Torpedos
    '''

    def __init__(self):
        self.range = None
        self.power = None
        self.minesSwept = None
        self.accuracy = None

class Bombs(object):

    def __init__(self):
        self.popKillPercent = None
        self.minKill = None
        self.installations = None



class MineLayer(object):

    def __init__(self):
        self.miningRate = None

        self.terraform = False

class Electrical(object):

    def __init__(self):
        self.tachyon = None
        self.deflection = None
        self.capacitor = None

        self.cloaking = None       # may need to change this


class Orbital(object):

    def __init__(self):
        self.safeMass = None
        self.safeRange = None

        self.warpSpeed = None

class PlanetaryInstallations(object):

    def __init__(self):
        self.range = None
        self.pen = None

        self.defenses40 = None
        self.defenses80 = None


class Terraforming(object):
    """docstring for Terraforming"""
    def __init__(self):
        super(Terraforming, self).__init__()
        self.modGrav  = None
        self.modTemp = None
        self.modRad = None

        
        

class Mechanical(object):

    def __init__(self):
        self.beamDeflector = None
        #self.movement = None
        self.extraFuel = None
        self.extraCargo = None

        self.colonizer = None
        # self.cargo = None    


class Scanner(object):
    
    def __init__(self):
        self.normalRange = None
        self.penRange = None
        self.stealFromShips = False   
        self.stealFromPlanets = False




class Armor(object):

    def __init__(self):
        self.armor = None

class Shields(object):

    def __init__(self):
        self.shield = None





class Component(BaseTech):
    # may want to consider class type enum

    def __init__(self):
        super(Component, self).__init__()
        # self.name = None
        self.itemID = None
        self.typeDict = {}

        #engines
        self.optimalSpeed = None
        self.freeSpeed = None
        self.safeSpeed = None
        self.radiation = False

        #weapons
        self.range = None
        self.power = None
        self.minesSwept = None
        self.accuracy = None


        #bombs
        self.popKillPercent = None
        self.minKill = None
        self.installations = None

        #minelayer
        self.miningRate = None
        self.terraform = False

        #Electrical
        self.tachyon = None
        self.deflection = None
        self.capacitor = None

        #Mechanical
        self.beamDeflector = None
        #self.movement = None
        self.extraFuel = None
        self.extraCargo = None
        # self.fuel = None
        self.colonizer = None
        # self.cargo = None  

        #scanner
        self.range = None
        self.pen = None
        self.stealFromShips = False   
        self.stealFromPlanets = False

        #Armor
        self.armor = None

        #Shields
        self.shield = None


    def updateElements(self):
        extraItems = {}

        for eachKey in self.typeDict:
            each = self.typeDict[eachKey]
            
            # -- TODO -- test if each is a dictionary -> if not then should be a value

            for item in each.__dict__:
                if item in self.__dict__:
                    #print("key:%s\t self:%s; other:%s" % (item, self.__dict__[item], each.__dict__[item] ))
                    self.__dict__[item] = each.__dict__[item]
                    #print("a %s:%s" % (item, self.__dict__[item]))
                else:
                    # 
                    extraItems[item] = each.__dict__[item]

        print("Component:%s had %d items which were not added to the component" % (self.name, len(extraItems)))
        print("%s" % extraItems)

        



class Hull(BaseTech):

    def __init__(self):
        super(Hull,self).__init__()
        self.shipType = None    # Miner, Transport, Armed, ect.

        self.fuel = None        
        self.armor = 100
        # self.fuelCapacity = 500
        
        self.mineLayerDouble = False
        self.shipsHeal = False

        self.ARPopulation = None
        self.spaceDock = None


        # slot defines the hull component composition
        self.slot = {
            "A":{"objectType": "engine", "slotsAvalable":1 }, 
            "B":{"objectType":"itemType",  "slotsAvalable":2}}  # each key == specific slot

        # identify slots:
        #   slot type -> General, Engine, Weap, Mech, Elect, etc
        #   how many slots available

        # specify all ship related question?


class ShipDesign(CoreStats):
    ''' ShipDesign is a specific user defined design of the Hull class 
    '''

    def __init__(self, hullID):
        super(ShipDesign,self).__init__()
        self.designName = None  # user specified ship design name
        self.designID = None
        self.isDesignLocked = False   # once a player has built a design- it cannot change
        self.owner = None

        self.hullID = hullID # points to a Hull object.  one for each type of ship.

        # component holds the number of items assigned to a design
        #self.component = {"A":["itemID", "itemID"], "B":["itemID", "itemID", "itemID"]}  # capacity
        self.component = {  
                "A":{"itemID": None, "itemQuantity": None }, 
                "B":{"itemID": None, "itemQuantity": None}}  # capacity

        self.seen = [] #? necessary?

    def componentDict(self, key, value):

        '''
        if key is electrical:
            update the ship designs electrical object values?
            update BaseTech values + objects values?
        '''
        pass








