# -*- coding: utf-8 -*-
#added to use plus\minus symbol in terraforming tech

from template import get_PRT_list

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










def items_armor():
    return {"Tritanium" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0,
                           "electronics" : 0, "biotechnology" : 0, "mass" : 60, "resources" : 10,
                           "iron" : 5, "bor" : 0, "ger" : 0, "DP" : 50},
            "Crobmnium" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 3,
                           "electronics" : 0, "biotechnology" : 0, "mass" : 56, "resources" : 13,
                           "iron" : 6, "bor" : 0, "ger" : 0, "DP" : 75},
            "Carbonic Armor" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0,
                                "electronics" : 0, "biotechnology" : 4, "mass" : 25, "resources" : 15,
                                "iron" : 0, "bor" : 0, "ger" : 5, "DP" : 100},
            "Strobnium" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 6,
                           "electronics" : 0, "biotechnology" : 0, "mass" : 54, "resources" : 18,
                           "iron" : 8, "bor" : 0, "ger" : 0, "DP" : 120},
            "Organic Armor" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0,
                               "electronics" : 0, "biotechnology" : 7, "mass" : 15, "resources" : 20,
                               "iron" : 0, "bor" : 0, "ger" : 6, "DP" : 175},
            "Kelarium" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 9,
                          "electronics" : 0, "biotechnology" : 0, "mass" : 50, "resources" : 25,
                          "iron" : 9, "bor" : 1, "ger" : 0, "DP" : 180},
            "Fielded Kelarium" : {"energy" : 4, "weapons" : 0, "propulsion" : 0, "construction" : 10,
                                  "electronics" : 0, "biotechnology" : 0, "mass" : 50, "resources" : 28,
                                  "iron" : 10, "bor" : 0, "ger" : 2, "DP" : 175},
            "Depleted Neutronium" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 10,
                                     "electronics" : 3, "biotechnology" : 0, "mass" : 50, "resources" : 28,
                                     "iron" : 10, "bor" : 0, "ger" : 2, "DP" : 200},
            "Neutronium" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 12,
                            "electronics" : 0, "biotechnology" : 0, "mass" : 45, "resources" : 30,
                            "iron" : 11, "bor" : 2, "ger" : 1, "DP" : 275},
            "Valanium" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 16,
                          "electronics" : 0, "biotechnology" : 0, "mass" : 40, "resources" : 50,
                          "iron" : 15, "bor" : 0, "ger" : 0, "DP" : 500},
            "Superlatanium" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 24,
                               "electronics" : 0, "biotechnology" : 0, "mass" : 30, "resources" : 100,
                               "iron" : 25, "bor" : 0, "ger" : 0, "DP" : 1500}}


def items_beams():
    return {"Laser" : {"energy" : 0, "weapons" : 0, "propulsion" : 0,
                       "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                       "mass" : 1, "resources" : 5, "iron" : 0, "bor" : 6, "ger" : 0,
                       "range" : 1, "DP" : 10, "init" : 9},
            "X-Ray Laser" : {"energy" : 0, "weapons" : 3, "propulsion" : 0,
                             "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                             "mass" : 1, "resources" : 6, "iron" : 0, "bor" : 6, "ger" : 0,
                             "range" : 1, "DP" : 16, "init" : 9},
            "Mini Gun" : {"energy" : 0, "weapons" : 5, "propulsion" : 0,
                          "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                          "mass" : 3, "resources" : 10, "iron" : 0, "bor" : 16, "ger" : 0,
                          "range" : 2, "DP" : 13, "init" : 12},
            "Yakimora Light Phaser" : {"energy" : 0, "weapons" : 6, "propulsion" : 0,
                                       "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                       "mass" : 1, "resources" : 7, "iron" : 0, "bor" : 8, "ger" : 0,
                                       "range" : 1, "DP" : 26, "init" : 9},
            "Blackjack" : {"energy" : 0, "weapons" : 7, "propulsion" : 0,
                           "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                           "mass" : 10, "resources" : 7, "iron" : 0, "bor" : 16, "ger" : 0,
                           "range" : 0, "DP" : 90, "init" : 10},
            "Phaser Bazooka" : {"energy" : 0, "weapons" : 8, "propulsion" : 0,
                                "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                "mass" : 2, "resources" : 11, "iron" : 0, "bor" : 8, "ger" : 0,
                                "range" : 2, "DP" : 26, "init" : 7},
            "Pulsed Sapper" : {"energy" : 5, "weapons" : 9, "propulsion" : 0,
                               "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                               "mass" : 1, "resources" : 12, "iron" : 0, "bor" : 0, "ger" : 4,
                               "range" : 3, "DP" : 82, "init" : 14},
            "Colloidal Phaser" : {"energy" :0, "weapons" : 10, "propulsion" : 0,
                                "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                "mass" : 2, "resources" : 18, "iron" : 0, "bor" : 14, "ger" :  0,
                                "range" : 3, "DP" : 26, "initiative" : 5},
            "Gatling Gun" : { "energy" : 0, "weapons" : 11, "propulsion" : 0,
                              "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                              "mass" : 3, "resources" : 13, "iron" : 0, "bor" : 20, "ger" : 0,
                              "range" : 2, "DP" : 31, "initiative" : 12},
            "Mini Blaster" : { "energy" : 0, "weapons" : 12, "propulsion" : 0,
                               "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                               "mass" : 1, "resources" : 9, "iron" : 0, "bor" : 10, "ger" : 0,
                               "range" : 1, "DP" : 66, "initiative" : 9},
            "Bludgeon" : { "energy" : 0, "weapons" : 13, "propulsion" : 0,
                           "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                           "mass" : 10, "resources" : 9, "iron" : 0, "bor" : 22, "ger" : 0,
                           "range" : 0, "DP" : 231, "initiative" : 10},
            "Mark IV Blaster" : { "energy" : 0, "weapons" : 14, "propulsion" : 0,
                                  "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                  "mass" : 2, "resources" : 15, "iron" : 0, "bor" : 12, "ger" : 0,
                                  "range" : 2, "DP" : 66, "initiative" : 7},
            "Phased Sapper" : { "energy" : 8, "weapons" : 15, "propulsion" : 0,
                                "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                "mass" : 1, "resources" : 16, "iron" : 0, "bor" : 0, "ger" : 6,
                                "range" : 3, "DP" : 211, "initiative" : 14},
            "Heavy Blaster" : { "energy" : 0, "weapons" : 16, "propulsion" : 0,
                                "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                "mass" : 2, "resources" : 25, "iron" : 0, "bor" : 20, "ger" : 0,
                                "range" : 3, "DP" : 66, "initiative" : 5},
            "Gatling Neutrino Cannon" : { "energy" : 0, "weapons" : 17, "propulsion" : 0,
                                          "construction" : 0, "electronics" : 0, "biotechnology" : 0        ,
                                          "mass" : 3, "resources" : 17, "iron" : 0, "bor" : 28, "ger" : 0,
                                          "range" : 2, "DP" : 80, "initiative" : 13},
            "Myopic Disrupter" : { "energy" : 0, "weapons" : 18, "propulsion" : 0,
                                   "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                   "mass" : 1, "resources" : 12, "iron" : 0, "bor" : 14, "ger" : 0,
                                   "range" : 1, "DP" : 169, "initiative" : 9},
            "Blunderbuss" : { "energy" : 0, "weapons" : 19, "propulsion" : 0,
                              "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                              "mass" : 10, "resources" : 13, "iron" : 0, "bor" : 30, "ger" : 0,
                              "range" : 0, "DP" : 592, "initiative" : 11},
            "Disruptor" : { "energy" : 0, "weapons" : 20, "propulsion" : 0,
                            "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                            "mass" : 2, "resources" : 20, "iron" : 0, "bor" : 16, "ger" : 0,
                            "range" : 2, "DP" : 169, "initiative" : 8},
            "Syncro Sapper" : { "energy" : 11, "weapons" : 21, "propulsion" : 0,
                                "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                "mass" : 1, "resources" : 21, "iron" : 0, "bor" : 0, "ger" : 8,
                                "range" : 3, "DP" : 541, "initiative" : 14},
            "Mega Disruptor" : { "energy" : 0, "weapons" : 22, "propulsion" : 0,
                                 "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                 "mass" : 2, "resources" : 33, "iron" : 0, "bor" : 30, "ger" : 0,
                                 "range" : 3, "DP" : 169, "initiative" : 6},
            "Big Mutha Cannon" : { "energy" : 0, "weapons" : 23, "propulsion" : 0,
                                   "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                   "mass" : 3, "resources" : 23, "iron" : 0, "bor" : 36, "ger" : 0,
                                   "range" : 2, "DP" : 204, "initiative" : 13},
            "Streaming Pulverizer" : { "energy" : 0, "weapons" : 24, "propulsion" : 0,
                                       "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                       "mass" : 1, "resources" : 16, "iron" : 0, "bor" : 20, "ger" : 0,
                                       "range" : 1, "DP" : 433, "initiative" : 9},
            "Anti-Matter Pulverizer" : { "energy" : 0, "weapons" : 26, "propulsion" : 0,
                                         "construction" : 0, "electronics" : 0, "biotechnology" : 0,
                                         "mass" : 2, "resources" : 27, "iron" : 0, "bor" : 22, "ger" : 0,
                                         "range" : 2, "DP" : 433, "initiative" : 8}
    }



def items_bombs():
    return {"Lady Finger Bomb" : {"energy" : 0, "weapons" : 2, "propulsion" : 0, "construction" : 0, 
                                  "electronics" : 0, "biotechnology" : 0, "mass" : 40, "resources" : 5, 
                                  "iron" : 1, "bor" : 20, "ger" : 0, "kill" : 0.6, "density" : 0.2},
            "Black Cat Bomb" : {"energy" : 0, "weapons" : 5, "propulsion" : 0, "construction" : 0, 
                                "electronics" : 0, "biotechnology" : 0, "mass" : 45, "resources" : 7, 
                                "iron" : 1, "bor" : 22, "ger" : 0, "kill" : 0.9, "density" : 0.4},
            "M-70 Bomb" : {"energy" : 0, "weapons" : 8, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 0, "biotechnology" : 0, "mass" : 50, "resources" : 9, 
                           "iron" : 1, "bor" : 24, "ger" : 0, "kill" : 1.2, "density" : 0.6},
            "M-80 Bomb" : {"energy" : 0, "weapons" : 11, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 0, "biotechnology" : 0, "mass" : 55, "resources" : 12, 
                           "iron" : 1, "bor" : 25, "ger" : 0, "kill" : 1.7, "density" : 0.7},
            "Cherry Bomb" : {"energy" : 0, "weapons" : 14, "propulsion" : 0, "construction" : 0, 
                             "electronics" : 0, "biotechnology" : 0, "mass" : 52, "resources" : 11, 
                             "iron" : 1, "bor" : 25, "ger" : 0, "kill" : 2.5, "density" : 1},
            "LBU-17 Bomb" : {"energy" : 0, "weapons" : 5, "propulsion" : 0, "construction" : 0, 
                             "electronics" : 8, "biotechnology" : 0, "mass" : 30, "resources" : 7, 
                             "iron" : 1, "bor" : 15, "ger" : 15, "kill" : 0.2, "density" : 1.6},
            "LBU-32 Bomb" : {"energy" : 0, "weapons" : 10, "propulsion" : 0, "construction" : 0, 
                             "electronics" : 10, "biotechnology" : 0, "mass" : 35, "resources" : 10, 
                             "iron" : 1, "bor" : 24, "ger" : 15, "kill" : 0.3, "density" : 2.8},
            "LBU-74 Bomb" : {"energy" : 0, "weapons" : 15, "propulsion" : 0, "construction" : 0, 
                             "electronics" : 12, "biotechnology" : 0, "mass" : 45, "resources" : 14, 
                             "iron" : 1, "bor" : 33, "ger" : 12, "kill" : 0.4, "density" : 4.5},
            "Retro Bomb" : {"energy" : 0, "weapons" : 10, "propulsion" : 0, "construction" : 0, 
                            "electronics" : 0, "biotechnology" : 12, "mass" : 45, "resources" : 50, 
                            "iron" : 15, "bor" : 15, "ger" : 10, "kill" : 0, "density" : 0},
            "Smart Bomb" : {"energy" : 0, "weapons" : 5, "propulsion" : 0, "construction" : 0, 
                            "electronics" : 0, "biotechnology" : 7, "mass" : 50, "resources" : 27, 
                            "iron" : 1, "bor" : 22, "ger" : 0, "kill" : 1.3, "density" : 0},
            "Neutron Bomb" : {"energy" : 0, "weapons" : 10, "propulsion" : 0, "construction" : 0, 
                              "electronics" : 0, "biotechnology" : 10, "mass" : 57, "resources" : 30, 
                              "iron" : 1, "bor" : 30, "ger" : 0, "kill" : 2.2, "density" : 0},
            "Enriched Neutron Bomb" : {"energy" : 0, "weapons" : 15, "propulsion" : 0, "construction" : 0, 
                                       "electronics" : 0, "biotechnology" : 12, "mass" : 64, "resources" : 25, 
                                       "iron" : 1, "bor" : 36, "ger" : 0, "kill" : 3.5, "density" : 0},
            "Peerless Bomb" : {"energy" : 0, "weapons" : 22, "propulsion" : 0, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 15, "mass" : 55, "resources" : 32, 
                               "iron" : 1, "bor" : 33, "ger" : 0, "kill" : 5, "density" : 0},
            "Annihilator Bomb" : {"energy" : 0, "weapons" : 26, "propulsion" : 0, "construction" : 0, 
                                  "electronics" : 0, "biotechnology" : 17, "mass" : 50, "resources" : 28, 
                                  "iron" : 1, "bor" : 30, "ger" : 0, "kill" : 7, "density" : 0}}

def items_electrical():
    return {"Transport Cloaking" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                    "electronics" : 0, "biotechnology" : 0, "mass" : 1, "resources" : 3, 
                                    "iron" : 2, "bor" : 0, "ger" : 2, "ability" : 300},
            "Stealth Cloak" : {"energy" : 2, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                               "electronics" : 5, "biotechnology" : 0, "mass" : 2, "resources" : 5, 
                               "iron" : 2, "bor" : 0, "ger" : 2, "ability" : 70},
            "Super-Stealth Cloak" : {"energy" : 4, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                     "electronics" : 10, "biotechnology" : 0, "mass" : 3, "resources" : 15, 
                                     "iron" : 8, "bor" : 0, "ger" : 8, "ability" : 140},
            "Ultra-Stealth Cloak" : {"energy" : 10, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                     "electronics" : 12, "biotechnology" : 0, "mass" : 5, "resources" : 25, 
                                     "iron" : 10, "bor" : 0, "ger" : 10, "ability" : 540},
            "Battle Computer" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 1, "resources" : 6, 
                                 "iron" : 0, "bor" : 0, "ger" : 15, "ability" : 20},
            "Battle Super Computer" : {"energy" : 5, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                       "electronics" : 11, "biotechnology" : 0, "mass" : 1, "resources" : 14, 
                                       "iron" : 0, "bor" : 0, "ger" : 25, "ability" : 30},
            "Battle Nexus" : {"energy" : 10, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                              "electronics" : 19, "biotechnology" : 0, "mass" : 1, "resources" : 15, 
                              "iron" : 0, "bor" : 0, "ger" : 30, "ability" : 50},
            "Jammer 10" : {"energy" : 2, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 6, "biotechnology" : 0, "mass" : 1, "resources" : 6, 
                           "iron" : 0, "bor" : 0, "ger" : 2, "ability" : 10},
            "Jammer 20" : {"energy" : 4, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 10, "biotechnology" : 0, "mass" : 1, "resources" : 20, 
                           "iron" : 1, "bor" : 0, "ger" : 5, "ability" : 20},
            "Jammer 30" : {"energy" : 8, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 16, "biotechnology" : 0, "mass" : 1, "resources" : 20, 
                           "iron" : 1, "bor" : 0, "ger" : 6, "ability" : 30},
            "Jammer 50" : {"energy" : 16, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 22, "biotechnology" : 0, "mass" : 1, "resources" : 20, 
                           "iron" : 2, "bor" : 0, "ger" : 7, "ability" : 50},
            "Energy Capacitor" : {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                  "electronics" : 4, "biotechnology" : 0, "mass" : 1, "resources" : 5, 
                                  "iron" : 0, "bor" : 0, "ger" : 8, "ability" : 10},
            "Flux Capacitor" : {"energy" : 14, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                "electronics" : 8, "biotechnology" : 0, "mass" : 1, "resources" : 5, 
                                "iron" : 0, "bor" : 0, "ger" : 8, "ability" : 20},
            "Energy Dampener" : {"energy" : 14, "weapons" : 0, "propulsion" : 8, "construction" : 0, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 2, "resources" : 50, 
                                 "iron" : 5, "bor" : 10, "ger" : 0, "ability" : -4},
            "Tachyon Detector" : {"energy" : 8, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                  "electronics" : 14, "biotechnology" : 0, "mass" : 1, "resources" : 70, 
                                  "iron" : 1, "bor" : 5, "ger" : 0, "ability" : -5},
            "Anti-matter Generator" : {"energy" : 0, "weapons" : 12, "propulsion" : 0, "construction" : 0, 
                                       "electronics" : 0, "biotechnology" : 7, "mass" : 10, "resources" : 10, 
                                       "iron" : 8, "bor" : 3, "ger" : 3, "ability" : 200}}

def items_engines():
    return {"Settler's Delight" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                   "electronics" : 0, "biotechnology" : 0, "mass" : 2, "resources" : 2, 
                                   "iron" : 1, "bor" : 0, "ger" : 1, "warp 1" : 0, "warp 2" : 0, "warp 3" : 0, 
                                   "warp 4" : 0, "warp 5" : 0, "warp 6" : 0, "warp 7" : 140, "warp 8" : 275, 
                                   "warp 9" : 480, "warp 10" : 576, "warp 10 safe" : False},
            "Quick Jump 5" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                              "electronics" : 0, "biotechnology" : 0, "mass" : 4, "resources" : 3, 
                              "iron" : 3, "bor" : 0, "ger" : 1, "warp 1" : 0, "warp 2" : 25, "warp 3" : 100, 
                              "warp 4" : 100, "warp 5" : 100, "warp 6" : 180, "warp 7" : 500, "warp 8" : 800, 
                              "warp 9" : 900, "warp 10" : 1080, "warp 10 safe" : False}, 
            "Fuel Mizer" : {"energy" : 0, "weapons" : 0, "propulsion" : 2, "construction" : 0, 
                            "electronics" : 0, "biotechnology" : 0, "mass" : 6, "resources" : 11, 
                            "iron" : 8, "bor" : 0, "ger" : 0, "warp 1" : 0, "warp 2" : 0, "warp 3" : 0, 
                            "warp 4" : 0, "warp 5" : 35, "warp 6" : 120, "warp 7" : 175, "warp 8" : 235, 
                            "warp 9" : 360, "warp 10" : 420, "warp 10 safe" : False}, 
            "Long Hump 6" : {"energy" : 0, "weapons" : 0, "propulsion" : 3, "construction" : 0, 
                             "electronics" : 0, "biotechnology" : 0, "mass" : 9, "resources" : 6, 
                             "iron" : 5, "bor" : 0, "ger" : 1, "warp 1" : 0, "warp 2" : 20, "warp 3" : 60, 
                             "warp 4" : 100, "warp 5" : 100, "warp 6" : 105, "warp 7" : 450, "warp 8" : 750, 
                             "warp 9" : 900, "warp 10" : 1080, "warp 10 safe" : False}, 
            "Daddy Long Legs 7" : {"energy" : 0, "weapons" : 0, "propulsion" : 5, "construction" : 0, 
                                   "electronics" : 0, "biotechnology" : 0, "mass" : 13, "resources" : 12, 
                                   "iron" : 11, "bor" : 0, "ger" : 3, "warp 1" : 0, "warp 2" : 20, "warp 3" : 60, 
                                   "warp 4" : 70, "warp 5" : 100, "warp 6" : 100, "warp 7" : 110, "warp 8" : 600, 
                                   "warp 9" : 750, "warp 10" : 900, "warp 10 safe" : False}, 
            "Alpha Drive 8" : {"energy" : 0, "weapons" : 0, "propulsion" : 7, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 0, "mass" : 17, "resources" : 28, 
                               "iron" : 16, "bor" : 0, "ger" : 3, "warp 1" : 0, "warp 2" : 15, "warp 3" : 50, 
                               "warp 4" : 60, "warp 5" : 70, "warp 6" : 100, "warp 7" : 100, "warp 8" : 115, 
                               "warp 9" : 700, "warp 10" : 840, "warp 10 safe" : False}, 
            "Trans-Galactic Drive" : {"energy" : 0, "weapons" : 0, "propulsion" : 9, "construction" : 0, 
                                      "electronics" : 0, "biotechnology" : 0, "mass" : 25, "resources" : 50, 
                                      "iron" : 20, "bor" : 20, "ger" : 9, "warp 1" : 0, "warp 2" : 15, "warp 3" : 35, 
                                      "warp 4" : 45, "warp 5" : 55, "warp 6" : 70, "warp 7" : 80, "warp 8" : 90, 
                                      "warp 9" : 100, "warp 10" : 120, "warp 10 safe" : False}, 
            "Interspace-10" : {"energy" : 0, "weapons" : 0, "propulsion" : 11, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 0, "mass" : 25, "resources" : 60, 
                               "iron" : 18, "bor" : 25, "ger" : 10, "warp 1" : 0, "warp 2" : 10, "warp 3" : 30, 
                               "warp 4" : 40, "warp 5" : 50, "warp 6" : 60, "warp 7" : 70, "warp 8" : 80, 
                               "warp 9" : 90, "warp 10" : 100, "warp 10 safe" : True}, 
            "Trans-Star 10" : {"energy" : 0, "weapons" : 0, "propulsion" : 23, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 0, "mass" : 5, "resources" : 10, 
                               "iron" : 3, "bor" : 0, "ger" : 3, "warp 1" : 0, "warp 2" : 5, "warp 3" : 15, 
                               "warp 4" : 20, "warp 5" : 25, "warp 6" : 30, "warp 7" : 35, "warp 8" : 40, 
                               "warp 9" : 45, "warp 10" : 50, "warp 10 safe" : True}, 
            "Radiating Hydro-Ram Scoop" : {"energy" : 2, "weapons" : 0, "propulsion" : 6, "construction" : 0, 
                                           "electronics" : 0, "biotechnology" : 0, "mass" : 10, "resources" : 8, 
                                           "iron" : 3, "bor" : 2, "ger" : 9, "warp 1" : 0, "warp 2" : 0, "warp 3" : 0, 
                                           "warp 4" : 0, "warp 5" : 0, "warp 6" : 0, "warp 7" : 165, "warp 8" : 375, 
                                           "warp 9" : 600, "warp 10" : 720, "warp 10 safe" : False}, 
            "Sub-Galactic Fuel Scoop" : {"energy" : 2, "weapons" : 0, "propulsion" : 8, "construction" : 0, 
                                         "electronics" : 0, "biotechnology" : 0, "mass" : 20, "resources" : 12, 
                                         "iron" : 4, "bor" : 4, "ger" : 7, "warp 1" : 0, "warp 2" : 0, "warp 3" : 0, 
                                         "warp 4" : 0, "warp 5" : 0, "warp 6" : 85, "warp 7" : 105, "warp 8" : 210, 
                                         "warp 9" : 380, "warp 10" : 456, "warp 10 safe" : False}, 
            "Trans-Galactic Fuel Scoop" : {"energy" : 3, "weapons" : 0, "propulsion" : 9, "construction" : 0, 
                                           "electronics" : 0, "biotechnology" : 0, "mass" : 19, "resources" : 18, 
                                           "iron" : 5, "bor" : 4, "ger" : 12, "warp 1" : 0, "warp 2" : 0, "warp 3" : 0, 
                                           "warp 4" : 0, "warp 5" : 0, "warp 6" : 0, "warp 7" : 88, "warp 8" : 100, 
                                           "warp 9" : 145, "warp 10" : 174, "warp 10 safe" : False}, 
            "Trans-Galactic Super Scoop" : {"energy" : 4, "weapons" : 0, "propulsion" : 12, "construction" : 0, 
                                            "electronics" : 0, "biotechnology" : 0, "mass" : 18, "resources" : 24, 
                                            "iron" : 6, "bor" : 4, "ger" : 16, "warp 1" : 0, "warp 2" : 0, "warp 3" : 0, 
                                            "warp 4" : 0, "warp 5" : 0, "warp 6" : 0, "warp 7" : 0, "warp 8" : 65, 
                                            "warp 9" : 90, "warp 10" : 108, "warp 10 safe" : False}, 
            "Trans-Galactic Mizer Scoop" : {"energy" : 4, "weapons" : 0, "propulsion" : 16, "construction" : 0, 
                                            "electronics" : 0, "biotechnology" : 0, "mass" : 11, "resources" : 20, 
                                            "iron" : 5, "bor" : 2, "ger" : 13, "warp 1" : 0, "warp 2" : 0, "warp 3" : 0, 
                                            "warp 4" : 0, "warp 5" : 0, "warp 6" : 0, "warp 7" : 0, "warp 8" : 0, 
                                            "warp 9" : 70, "warp 10" : 84, "warp 10 safe" : True}, 
            "Galaxy Scoop" : {"energy" : 5, "weapons" : 0, "propulsion" : 20, "construction" : 0, 
                              "electronics" : 0, "biotechnology" : 0, "mass" : 8, "resources" : 12, 
                              "iron" : 4, "bor" : 2, "ger" : 9, "warp 1" : 0, "warp 2" : 0, "warp 3" : 0, 
                              "warp 4" : 0, "warp 5" : 0, "warp 6" : 0, "warp 7" : 0, "warp 8" : 0, 
                              "warp 9" : 0, "warp 10" : 60, "warp 10 safe" : True}}


def items_hulls():
    return {"Small Freighter" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 25, "resources" : 20, 
                                 "iron" : 12, "bor" : 0, "ger" : 17, "fuel" : 130, "cargo" : 70, "DP" : 25, "initiative" : 0}, 
            "Medium Freighter" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 3, 
                                  "electronics" : 0, "biotechnology" : 0, "mass" : 60, "resources" : 40, 
                                  "iron" : 20, "bor" : 0, "ger" : 19, "fuel" : 450, "cargo" : 210, "DP" : 50, "initiative" : 0}, 
            "Large Freighter" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 8, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 125, "resources" : 100, 
                                 "iron" : 35, "bor" : 0, "ger" : 21, "fuel" : 2600, "cargo" : 1200, "DP" : 150, "initiative" : 0}, 
            "Super Freighter" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 13, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 175, "resources" : 125, 
                                 "iron" : 45, "bor" : 0, "ger" : 21, "fuel" : 8000, "cargo" : 3000, "DP" : 400, "initiative" : 0}, 
            "Scout" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                       "electronics" : 0, "biotechnology" : 0, "mass" : 8, "resources" : 10, 
                       "iron" : 4, "bor" : 2, "ger" : 4, "fuel" : 50, "cargo" : 0, "DP" : 20, "initiative" : 1}, 
            "Frigate" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 6, 
                         "electronics" : 0, "biotechnology" : 0, "mass" : 8, "resources" : 12, 
                         "iron" : 4, "bor" : 2, "ger" : 4, "fuel" : 125, "cargo" : 0, "DP" : 45, "initiative" : 4}, 
            "Destroyer" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 3, 
                           "electronics" : 0, "biotechnology" : 0, "mass" : 30, "resources" : 35, 
                           "iron" : 15, "bor" : 3, "ger" : 5, "fuel" : 280, "cargo" : 0, "DP" : 200, "initiative" : 3}, 
            "Cruiser" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 9, 
                         "electronics" : 0, "biotechnology" : 0, "mass" : 90, "resources" : 85, 
                         "iron" : 40, "bor" : 5, "ger" : 8, "fuel" : 600, "cargo" : 0, "DP" : 700, "initiative" : 5}, 
            "Battle Cruiser" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 10, 
                                "electronics" : 0, "biotechnology" : 0, "mass" : 120, "resources" : 120, 
                                "iron" : 55, "bor" : 8, "ger" : 1, "fuel" : 1400, "cargo" : 0, "DP" : 1000, "initiative" : 5}, 
            "Battleship" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 13, 
                            "electronics" : 0, "biotechnology" : 0, "mass" : 222, "resources" : 225, 
                            "iron" : 120, "bor" : 25, "ger" : 20, "fuel" : 2800, "cargo" : 0, "DP" : 2000, "initiative" : 10}, 
            "Dreadnought" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 16, 
                             "electronics" : 0, "biotechnology" : 0, "mass" : 250, "resources" : 275, 
                             "iron" : 140, "bor" : 30, "ger" : 25, "fuel" : 4500, "cargo" : 0, "DP" : 4500, "initiative" : 10}, 
            "Privateer" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 4, 
                           "electronics" : 0, "biotechnology" : 0, "mass" : 65, "resources" : 50, 
                           "iron" : 50, "bor" : 3, "ger" : 2, "fuel" : 650, "cargo" : 250, "DP" : 150, "initiative" : 3}, 
            "Rogue" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 8, 
                       "electronics" : 0, "biotechnology" : 0, "mass" : 75, "resources" : 60, 
                       "iron" : 80, "bor" : 5, "ger" : 5, "fuel" : 2250, "cargo" : 500, "DP" : 450, "initiative" : 4}, 
            "Galleon" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 11, 
                         "electronics" : 0, "biotechnology" : 0, "mass" : 125, "resources" : 105, 
                         "iron" : 70, "bor" : 5, "ger" : 5, "fuel" : 2500, "cargo" : 1000, "DP" : 900, "initiative" : 4}, 
            "Mini-Colony Ship" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                  "electronics" : 0, "biotechnology" : 0, "mass" : 8, "resources" : 3, 
                                  "iron" : 2, "bor" : 0, "ger" : 2, "fuel" : 150, "cargo" : 10, "DP" : 10, "initiative" : 0}, 
            "Colony Ship" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                             "electronics" : 0, "biotechnology" : 0, "mass" : 20, "resources" : 20, 
                             "iron" : 10, "bor" : 0, "ger" : 15, "fuel" : 200, "cargo" : 25, "DP" : 20, "initiative" : 0}, 
            "Mini Bomber" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 1, 
                             "electronics" : 0, "biotechnology" : 0, "mass" : 28, "resources" : 35, 
                             "iron" : 20, "bor" : 5, "ger" : 10, "fuel" : 120, "cargo" : 0, "DP" : 50, "initiative" : 0}, 
            "B-17 Bomber" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 6, 
                             "electronics" : 0, "biotechnology" : 0, "mass" : 69, "resources" : 150, 
                             "iron" : 55, "bor" : 10, "ger" : 10, "fuel" : 400, "cargo" : 0, "DP" : 175, "initiative" : 0}, 
            "Stealth Bomber" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 8, 
                                "electronics" : 0, "biotechnology" : 0, "mass" : 70, "resources" : 175, 
                                "iron" : 55, "bor" : 10, "ger" : 15, "fuel" : 750, "cargo" : 0, "DP" : 225, "initiative" : 0}, 
            "B-52 Bomber" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 15, 
                             "electronics" : 0, "biotechnology" : 0, "mass" : 110, "resources" : 280, 
                             "iron" : 90, "bor" : 15, "ger" : 10, "fuel" : 750, "cargo" : 0, "DP" : 450, "initiative" : 0}, 
            "Midget Miner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                              "electronics" : 0, "biotechnology" : 0, "mass" : 10, "resources" : 20, 
                              "iron" : 10, "bor" : 0, "ger" : 3, "fuel" : 210, "cargo" : 0, "DP" : 100, "initiative" : 0}, 
            "Mini-miner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 2, 
                            "electronics" : 0, "biotechnology" : 0, "mass" : 80, "resources" : 50, 
                            "iron" : 25, "bor" : 0, "ger" : 6, "fuel" : 210, "cargo" : 0, "DP" : 130, "initiative" : 0}, 
            "Miner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 6, 
                       "electronics" : 0, "biotechnology" : 0, "mass" : 110, "resources" : 110, 
                       "iron" : 32, "bor" : 0, "ger" : 6, "fuel" : 500, "cargo" : 0, "DP" : 475, "initiative" : 0}, 
            "Maxi-Miner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 11, 
                            "electronics" : 0, "biotechnology" : 0, "mass" : 110, "resources" : 140, 
                            "iron" : 32, "bor" : 0, "ger" : 6, "fuel" : 850, "cargo" : 0, "DP" : 1400, "initiative" : 0}, 
            "Ultra-Miner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 14, 
                             "electronics" : 0, "biotechnology" : 0, "mass" : 100, "resources" : 130, 
                             "iron" : 30, "bor" : 0, "ger" : 6, "fuel" : 1300, "cargo" : 0, "DP" : 1500, "initiative" : 0}, 
            "Fuel Transport" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 4, 
                                "electronics" : 0, "biotechnology" : 0, "mass" : 12, "resources" : 50, 
                                "iron" : 10, "bor" : 0, "ger" : 5, "fuel" : 750, "cargo" : 0, "DP" : 5, "initiative" : 0}, 
            "Super-Fuel Xport" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 7, 
                                  "electronics" : 0, "biotechnology" : 0, "mass" : 111, "resources" : 70, 
                                  "iron" : 20, "bor" : 0, "ger" : 8, "fuel" : 2250, "cargo" : 0, "DP" : 12, "initiative" : 0}, 
            "Mini Mine Layer" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 10, "resources" : 20, 
                                 "iron" : 8, "bor" : 2, "ger" : 5, "fuel" : 400, "cargo" : 0, "DP" : 60, "initiative" : 0}, 
            "Super Mine Layer" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 15, 
                                  "electronics" : 0, "biotechnology" : 0, "mass" : 30, "resources" : 30, 
                                  "iron" : 20, "bor" : 3, "ger" : 9, "fuel" : 2200, "cargo" : 0, "DP" : 1200, "initiative" : 0}, 
            "Nubian" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 26, 
                        "electronics" : 0, "biotechnology" : 0, "mass" : 100, "resources" : 150, 
                        "iron" : 75, "bor" : 12, "ger" : 12, "fuel" : 5000, "cargo" : 0, "DP" : 5000, "initiative" : 2}, 
            "Meta Morph" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 10, 
                            "electronics" : 0, "biotechnology" : 0, "mass" : 85, "resources" : 120, 
                            "iron" : 50, "bor" : 12, "ger" : 12, "fuel" : 700, "cargo" : 300, "DP" : 500, "initiative" : 2}}


def items_mechanical():
    return {"Colonization Module" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                     "electronics" : 0, "biotechnology" : 0, "mass" : 32, "resources" : 10, 
                                     "iron" : 12, "bor" : 10, "ger" : 10, "ability" : 0},
            "Orbital Construction Module" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                             "electronics" : 0, "biotechnology" : 0, "mass" : 50, "resources" : 20, 
                                             "iron" : 20, "bor" : 15, "ger" : 15, "ability" : 2},
            "Cargo Pod" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 3, 
                           "electronics" : 0, "biotechnology" : 0, "mass" : 5, "resources" : 10, 
                           "iron" : 5, "bor" : 0, "ger" : 2, "ability" : 5},
            "Super Cargo Pod" : {"energy" : 3, "weapons" : 0, "propulsion" : 0, "construction" : 9, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 7, "resources" : 15, 
                                 "iron" : 8, "bor" : 0, "ger" : 2, "ability" : 10},
            "Fuel Tank" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 0, "biotechnology" : 0, "mass" : 3, "resources" : 4, 
                           "iron" : 6, "bor" : 0, "ger" : 0, "ability" : 250},
            "Super Fuel Tank" : {"energy" : 6, "weapons" : 0, "propulsion" : 4, "construction" : 14, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 8, "resources" : 8, 
                                 "iron" : 8, "bor" : 0, "ger" : 0, "ability" : 500},
            "Manoeuvring Jet" : {"energy" : 2, "weapons" : 0, "propulsion" : 3, "construction" : 0, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 5, "resources" : 10, 
                                 "iron" : 5, "bor" : 0, "ger" : 5, "ability" : 1},
            "Overthruster" : {"energy" : 5, "weapons" : 0, "propulsion" : 12, "construction" : 0, 
                              "electronics" : 0, "biotechnology" : 0, "mass" : 5, "resources" : 20, 
                              "iron" : 10, "bor" : 0, "ger" : 8, "ability" : 2},
            "Beam Deflector" : {"energy" : 6, "weapons" : 6, "propulsion" : 0, "construction" : 6, 
                                "electronics" : 6, "biotechnology" : 0, "mass" : 1, "resources" : 8, 
                                "iron" : 0, "bor" : 0, "ger" : 10, "ability" : -10}}


def items_minelayers():
    return {"Mine Dispenser 40" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                   "electronics" : 0, "biotechnology" : 0, "mass" : 25, "resources" : 45, 
                                   "iron" : 2, "bor" : 10, "ger" : 8, "mines per year" : 40},
            "Mine Dispenser 50" : {"energy" : 2, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                   "electronics" : 0, "biotechnology" : 4, "mass" : 30, "resources" : 55, 
                                   "iron" : 2, "bor" : 12, "ger" : 10, "mines per year" : 50},
            "Mine Dispenser 80" : {"energy" : 3, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                   "electronics" : 0, "biotechnology" : 7, "mass" : 30, "resources" : 65, 
                                   "iron" : 2, "bor" : 14, "ger" : 10, "mines per year" : 80},
            "Mine Dispenser 130" : {"energy" : 6, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                    "electronics" : 0, "biotechnology" : 12, "mass" : 30, "resources" : 80, 
                                    "iron" : 2, "bor" : 18, "ger" : 10, "mines per year" : 130},
            "Heavy Dispenser 50" : {"energy" : 5, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                    "electronics" : 0, "biotechnology" : 3, "mass" : 10, "resources" : 50, 
                                    "iron" : 2, "bor" : 20, "ger" : 5, "mines per year" : 50},
            "Heavy Dispenser 110" : {"energy" : 9, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                     "electronics" : 0, "biotechnology" : 5, "mass" : 15, "resources" : 70, 
                                     "iron" : 2, "bor" : 30, "ger" : 5, "mines per year" : 110},
            "Heavy Dispenser 200" : {"energy" : 14, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                     "electronics" : 0, "biotechnology" : 7, "mass" : 20, "resources" : 90, 
                                     "iron" : 2, "bor" : 45, "ger" : 5, "mines per year" : 200},
            "Speed Trap 20" : {"energy" : 0, "weapons" : 0, "propulsion" : 2, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 2, "mass" : 100, "resources" : 60, 
                               "iron" : 30, "bor" : 0, "ger" : 12, "mines per year" : 20},
            "Speed Trap 30" : {"energy" : 0, "weapons" : 0, "propulsion" : 3, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 6, "mass" : 135, "resources" : 72, 
                               "iron" : 32, "bor" : 0, "ger" : 14, "mines per year" : 30},
            "Speed Trap 50" : {"energy" : 0, "weapons" : 0, "propulsion" : 5, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 11, "mass" : 140, "resources" : 80, 
                               "iron" : 40, "bor" : 0, "ger" : 15, "mines per year" : 50}}


def items_miningrobots():
    return {"Robo-Midget Miner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                   "electronics" : 0, "biotechnology" : 0, "mass" : 80, "resources" : 50, 
                                   "iron" : 14, "bor" : 0, "ger" : 4, "KT per year" : 5},
            "Robo-Mini-Miner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 2, 
                                 "electronics" : 1, "biotechnology" : 0, "mass" : 240, "resources" : 100, 
                                 "iron" : 30, "bor" : 0, "ger" : 7, "KT per year" : 4},
            "Robo-Miner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 4, 
                            "electronics" : 2, "biotechnology" : 0, "mass" : 240, "resources" : 100, 
                            "iron" : 30, "bor" : 0, "ger" : 7, "KT per year" : 12},
            "Robo-Maxi-Miner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 7, 
                                  "electronics" : 4, "biotechnology" : 0, "mass" : 240, "resources" : 100, 
                                  "iron" : 30, "bor" : 0, "ger" : 7, "KT per year" : 18},
            "Robo-Super-Miner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 12, 
                                  "electronics" : 6, "biotechnology" : 0, "mass" : 240, "resources" : 100, 
                                  "iron" : 30, "bor" : 0, "ger" : 7, "KT per year" : 27},
            "Robo-Ultra-Miner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 15, 
                                  "electronics" : 8, "biotechnology" : 0, "mass" : 80, "resources" : 50, 
                                  "iron" : 14, "bor" : 0, "ger" : 4, "KT per year" : 25},
            "Orbital Adjuster" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                  "electronics" : 0, "biotechnology" : 6, "mass" : 80, "resources" : 50, 
                                  "iron" : 25, "bor" : 25, "ger" : 25, "KT per year" : 0}}


def items_torpedoes():
    return {"Alpha Torpedo" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 0, "mass" : 25, "resources" : 5, 
                               "iron" : 9, "bor" : 3, "ger" : 3, "range"  : 4, "DP" : 5, "initiative" : 0, "hit chance" : 35, "double damage unshielded" : False},
            "Beta Torpedo" : {"energy" : 0, "weapons" : 5, "propulsion" : 1, "construction" : 0, 
                              "electronics" : 0, "biotechnology" : 0, "mass" : 25, "resources" : 6, 
                              "iron" : 18, "bor" : 6, "ger" : 4, "range"  : 4, "DP" : 12, "initiative" : 1, "hit chance" : 45, "double damage unshielded" : False},
            "Delta Torpedo" : {"energy" : 0, "weapons" : 10, "propulsion" : 2, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 0, "mass" : 25, "resources" : 8, 
                               "iron" : 22, "bor" : 8, "ger" : 5, "range"  : 4, "DP" : 26, "initiative" : 1, "hit chance" : 60, "double damage unshielded" : False},
            "Epsilon Torpedo" : {"energy" : 0, "weapons" : 14, "propulsion" : 3, "construction" : 0, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 25, "resources" : 10, 
                                 "iron" : 30, "bor" : 10, "ger" : 6, "range"  : 5, "DP" : 48, "initiative" : 2, "hit chance" : 65, "double damage unshielded" : False},
            "Rho Torpedo" : {"energy" : 0, "weapons" : 18, "propulsion" : 4, "construction" : 0, 
                             "electronics" : 0, "biotechnology" : 0, "mass" : 25, "resources" : 12, 
                             "iron" : 34, "bor" : 12, "ger" : 8, "range"  : 5, "DP" : 90, "initiative" : 2, "hit chance" : 75, "double damage unshielded" : False},
            "Upsilon Torpedo" : {"energy" : 0, "weapons" : 22, "propulsion" : 5, "construction" : 0, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 25, "resources" : 15, 
                                 "iron" : 40, "bor" : 14, "ger" : 9, "range"  : 5, "DP" : 169, "initiative" : 3, "hit chance" : 75, "double damage unshielded" : False},
            "Omega Torpedo" : {"energy" : 0, "weapons" : 26, "propulsion" : 6, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 0, "mass" : 25, "resources" : 18, 
                               "iron" : 52, "bor" : 18, "ger" : 12, "range"  : 5, "DP" : 316, "initiative" : 4, "hit chance" : 80, "double damage unshielded" : False},
            "Anti Matter Missile" : {"energy" : 0, "weapons" : 11, "propulsion" : 12, "construction" : 0, 
                                     "electronics" : 0, "biotechnology" : 21, "mass" : 8, "resources" : 50, 
                                     "iron" : 3, "bor" : 8, "ger" : 1, "range"  : 6, "DP" : 60, "initiative" : 0, "hit chance" : 85, "double damage unshielded" : False},
            "Jihad Missile" : {"energy" : 0, "weapons" : 12, "propulsion" : 6, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 0, "mass" : 35, "resources" : 13, 
                               "iron" : 37, "bor" : 13, "ger" : 9, "range"  : 5, "DP" : 85, "initiative" : 0, "hit chance" : 20, "double damage unshielded" : True},
            "Juggernaught Missile" : {"energy" : 0, "weapons" : 16, "propulsion" : 8, "construction" : 0, 
                                      "electronics" : 0, "biotechnology" : 0, "mass" : 35, "resources" : 16, 
                                      "iron" : 48, "bor" : 16, "ger" : 11, "range"  : 5, "DP" : 150, "initiative" : 1, "hit chance" : 20, "double damage unshielded" : True},
            "Doomsday Missile" : {"energy" : 0, "weapons" : 20, "propulsion" : 10, "construction" : 0, 
                                  "electronics" : 0, "biotechnology" : 0, "mass" : 35, "resources" : 20, 
                                  "iron" : 60, "bor" : 20, "ger" : 13, "range"  : 6, "DP" : 280, "initiative" : 2, "hit chance" : 25, "double damage unshielded" : True},
            "Armageddon Missile" : {"energy" : 0, "weapons" : 24, "propulsion" : 10, "construction" : 0, 
                                    "electronics" : 0, "biotechnology" : 0, "mass" : 35, "resources" : 24, 
                                    "iron" : 67, "bor" : 23, "ger" : 16, "range"  : 6, "DP" : 525, "initiative" : 3, "hit chance" : 30, "double damage unshielded" : True}}


def items_planetary_scanners():
    return {"Viewer 50" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 0, "biotechnology" : 0, "resources" : 100, 
                           "iron" : 10, "bor" : 10, "ger" : 70, "range" : 50, "pen scan" : 0},
            "Viewer 90" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 1, "biotechnology" : 0, "resources" : 100, 
                           "iron" : 10, "bor" : 10, "ger" : 70, "range" : 90, "pen scan" : 0},
            "Scoper 150" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                            "electronics" : 3, "biotechnology" : 0, "resources" : 100, 
                            "iron" : 10, "bor" : 10, "ger" : 70, "range" : 150, "pen scan" : 0},
            "Scoper 220" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                            "electronics" : 6, "biotechnology" : 0, "resources" : 100, 
                            "iron" : 10, "bor" : 10, "ger" : 70, "range" : 220, "pen scan" : 0},
            "Scoper 280" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                            "electronics" : 8, "biotechnology" : 0, "resources" : 100, 
                            "iron" : 10, "bor" : 10, "ger" : 70, "range" : 280, "pen scan" : 0},
            "Snooper 320X" : {"energy" : 3, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                              "electronics" : 10, "biotechnology" : 3, "resources" : 100, 
                              "iron" : 10, "bor" : 10, "ger" : 70, "range" : 320, "pen scan" : 160},
            "Snooper 400X" : {"energy" : 4, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                              "electronics" : 13, "biotechnology" : 6, "resources" : 100, 
                              "iron" : 10, "bor" : 10, "ger" : 70, "range" : 400, "pen scan" : 200},
            "Snooper 500X" : {"energy" : 5, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                              "electronics" : 16, "biotechnology" : 7, "resources" : 100, 
                              "iron" : 10, "bor" : 10, "ger" : 70, "range" : 500, "pen scan" : 250},
            "Snooper 620X" : {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                              "electronics" : 23, "biotechnology" : 9, "resources" : 100, 
                              "iron" : 10, "bor" : 10, "ger" : 70, "range" : 620, "pen scan" : 310}}


def items_planetary_defenses():
    return {"SDI" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                     "electronics" : 0, "biotechnology" : 0, "resources" : 15, 
                     "iron" : 5, "bor" : 5, "ger" : 5, "ability" : 10},
            "Missile Battery" : {"energy" : 5, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                 "electronics" : 0, "biotechnology" : 0, "resources" : 15, 
                                 "iron" : 5, "bor" : 5, "ger" : 5, "range" : 20},
            "Laser Battery" : {"energy" : 10, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 0, "resources" : 15, 
                               "iron" : 5, "bor" : 5, "ger" : 5, "range" : 24},
            "Planetary Shield" : {"energy" : 16, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                  "electronics" : 0, "biotechnology" : 0, "resources" : 15, 
                                  "iron" : 5, "bor" : 5, "ger" : 5, "range" : 30},
            "Neutron Shield" : {"energy" : 23, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                "electronics" : 0, "biotechnology" : 0, "resources" : 15, 
                                "iron" : 5, "bor" : 5, "ger" : 5, "range" : 38}}


def items_scanners():
    return {"Bat Scanner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                             "electronics" : 0, "biotechnology" : 0, "mass" : 2, "resources" : 1, 
                             "iron" : 1, "bor" : 0, "ger" : 1, "range" : 0, "pen scan" : 0},
            "Rhino Scanner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                               "electronics" : 1, "biotechnology" : 0, "mass" : 5, "resources" : 3, 
                               "iron" : 3, "bor" : 0, "ger" : 2, "range" : 50, "pen scan" : 0},
            "Mole Scanner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                              "electronics" : 4, "biotechnology" : 0, "mass" : 2, "resources" : 9, 
                              "iron" : 2, "bor" : 0, "ger" : 2, "range" : 100, "pen scan" : 0},
            "DNA Scanner" : {"energy" : 0, "weapons" : 0, "propulsion" : 3, "construction" : 0, 
                             "electronics" : 0, "biotechnology" : 6, "mass" : 2, "resources" : 5, 
                             "iron" : 1, "bor" : 1, "ger" : 1, "range" : 125, "pen scan" : 0},
            "Possum Scanner" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                "electronics" : 5, "biotechnology" : 0, "mass" : 3, "resources" : 18, 
                                "iron" : 3, "bor" : 0, "ger" : 3, "range" : 150, "pen scan" : 0},
            "Pick Pocket Scanner" : {"energy" : 4, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                     "electronics" : 4, "biotechnology" : 4, "mass" : 15, "resources" : 35, 
                                     "iron" : 8, "bor" : 10, "ger" : 6, "range" : 80, "pen scan" : 0},
            "Chameleon Scanner" : {"energy" : 3, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                   "electronics" : 6, "biotechnology" : 0, "mass" : 6, "resources" : 25, 
                                   "iron" : 4, "bor" : 6, "ger" : 4, "range" : 160, "pen scan" : 45},
            "Ferret Scanner" : {"energy" : 3, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                "electronics" : 7, "biotechnology" : 2, "mass" : 2, "resources" : 36, 
                                "iron" : 2, "bor" : 0, "ger" : 8, "range" : 185, "pen scan" : 50},
            "Dolphin Scanner" : {"energy" : 5, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                 "electronics" : 10, "biotechnology" : 4, "mass" : 4, "resources" : 40, 
                                 "iron" : 5, "bor" : 5, "ger" : 10, "range" : 220, "pen scan" : 100},
            "Gazelle Scanner" : {"energy" : 4, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                 "electronics" : 8, "biotechnology" : 0, "mass" : 5, "resources" : 24, 
                                 "iron" : 4, "bor" : 0, "ger" : 5, "range" : 225, "pen scan" : 0},
            "RNA Scanner" : {"energy" : 0, "weapons" : 0, "propulsion" : 5, "construction" : 0, 
                             "electronics" : 0, "biotechnology" : 10, "mass" : 2, "resources" : 20, 
                             "iron" : 1, "bor" : 1, "ger" : 2, "range" : 230, "pen scan" : 0},
            "Cheetah Scanner" : {"energy" : 5, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                 "electronics" : 11, "biotechnology" : 0, "mass" : 4, "resources" : 50, 
                                 "iron" : 3, "bor" : 1, "ger" : 13, "range" : 275, "pen scan" : 0},
            "Elephant Scanner" : {"energy" : 6, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                  "electronics" : 16, "biotechnology" : 7, "mass" : 6, "resources" : 70, 
                                  "iron" : 8, "bor" : 5, "ger" : 14, "range" : 300, "pen scan" : 200},
            "Eagle Eye Scanner" : {"energy" : 6, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                   "electronics" : 14, "biotechnology" : 0, "mass" : 3, "resources" : 64, 
                                   "iron" : 3, "bor" : 2, "ger" : 21, "range" : 335, "pen scan" : 0},
            "Robber Baron Scanner" : {"energy" : 10, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                      "electronics" : 15, "biotechnology" : 10, "mass" : 20, "resources" : 90, 
                                      "iron" : 10, "bor" : 10, "ger" : 10, "range" : 220, "pen scan" : 120},
            "Peerless Scanner" : {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                  "electronics" : 24, "biotechnology" : 0, "mass" : 4, "resources" : 90, 
                                  "iron" : 3, "bor" : 2, "ger" : 30, "range" : 500, "pen scan" : 0}}


def items_shields():
    return {"Mole-skin Shield" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                  "electronics" : 0, "biotechnology" : 0, "mass" : 1, "resources" : 4, 
                                  "iron" : 1, "bor" : 0, "ger" : 1, "DP" : 25}, 
            "Cow-hide Shield" : {"energy" : 3, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                 "electronics" : 0, "biotechnology" : 0, "mass" : 1, "resources" : 5, 
                                 "iron" : 2, "bor" : 0, "ger" : 2, "DP" : 40}, 
            "Wolverine Diffuse Shield" : {"energy" : 6, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                          "electronics" : 0, "biotechnology" : 0, "mass" : 1, "resources" : 6, 
                                          "iron" : 3, "bor" : 0, "ger" : 3, "DP" : 60}, 
            "Croby Sharmor" : {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 4, 
                               "electronics" : 0, "biotechnology" : 0, "mass" : 10, "resources" : 15, 
                               "iron" : 7, "bor" : 0, "ger" : 4, "DP" : 60}, 
            "Shadow Shield" : {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                               "electronics" : 3, "biotechnology" : 0, "mass" : 2, "resources" : 7, 
                               "iron" : 3, "bor" : 0, "ger" : 3, "DP" : 75}, 
            "Bear Neutrino Barrier" : {"energy" : 10, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                       "electronics" : 0, "biotechnology" : 0, "mass" : 1, "resources" : 8, 
                                       "iron" : 4, "bor" : 0, "ger" : 4, "DP" : 100}, 
            "Gorilla Delagator" : {"energy" : 14, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                   "electronics" : 0, "biotechnology" : 0, "mass" : 1, "resources" : 11, 
                                   "iron" : 5, "bor" : 0, "ger" : 6, "DP" : 175}, 
            "Elephant Hide Fortress" : {"energy" : 18, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                        "electronics" : 0, "biotechnology" : 0, "mass" : 1, "resources" : 15, 
                                        "iron" : 8, "bor" : 0, "ger" : 10, "DP" : 300}, 
            "Complete Phase Shield" : {"energy" : 22, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                       "electronics" : 0, "biotechnology" : 0, "mass" : 1, "resources" : 20, 
                                       "iron" : 12, "bor" : 0, "ger" : 15, "DP" : 500}} 

def items_starbases():
    return {"Orbital Fort" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                              "electronics" : 0, "biotechnology" : 0, "resources" : 80, 
                              "iron" : 24, "bor" : 0, "ger" : 34, "dock size" : 0, "DP" : 100, "initiative" : 10}, 
            "Space Dock" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 4, 
                            "electronics" : 0, "biotechnology" : 0, "resources" : 200, 
                            "iron" : 40, "bor" : 10, "ger" : 50, "dock size" : 200, "DP" : 250, "initiative" : 12}, 
            "Space Station" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                               "electronics" : 0, "biotechnology" : 0, "resources" : 1200, 
                               "iron" : 240, "bor" : 160, "ger" : 500, "dock size" : 'inf', "DP" : 500, "initiative" : 14},
            "Ultra Station" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 12, 
                               "electronics" : 0, "biotechnology" : 0, "resources" : 1200, 
                               "iron" : 240, "bor" : 160, "ger" : 600, "dock size" : 'inf', "DP" : 1000, "initiative" : 16}, 
            "Death Star" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 17, 
                            "electronics" : 0, "biotechnology" : 0, "resources" : 1500, 
                            "iron" : 240, "bor" : 160, "ger" : 700, "dock size" : 'inf', "DP" : 1500, "initiative" : 18}}

def items_stargates():
    return {"Stargate 100/250" : {"energy" : 0, "weapons" : 0, "propulsion" : 5, "construction" : 5, 
                                  "electronics" : 0, "biotechnology" : 0, "resources" : 200, 
                                  "iron" : 50, "bor" : 20, "ger" : 20, "hull mass" : 100, "range" : 250},
            "Stargate any/300" : {"energy" : 0, "weapons" : 0, "propulsion" : 6, "construction" : 10, 
                                  "electronics" : 0, "biotechnology" : 0, "resources" : 250, 
                                  "iron" : 50, "bor" : 20, "ger" : 20, "hull mass" : 'inf', "range" : 300}, 
            "Stargate 150/600" : {"energy" : 0, "weapons" : 0, "propulsion" : 11, "construction" : 7, 
                                  "electronics" : 0, "biotechnology" : 0, "resources" : 500, 
                                  "iron" : 50, "bor" : 20, "ger" : 20, "hull mass" : 150, "range" : 600}, 
            "Stargate 300/500" : {"energy" : 0, "weapons" : 0, "propulsion" : 9, "construction" : 13, 
                                  "electronics" : 0, "biotechnology" : 0, "resources" : 600, 
                                  "iron" : 50, "bor" : 20, "ger" : 20, "hull mass" : 300, "range" : 500}, 
            "Stargate 100/any" : {"energy" : 0, "weapons" : 0, "propulsion" : 16, "construction" : 12, 
                                  "electronics" : 0, "biotechnology" : 0, "resources" : 700, 
                                  "iron" : 50, "bor" : 20, "ger" : 20, "hull mass" : 100, "range" : 'inf'}, 
            "Stargate any/800" : {"energy" : 0, "weapons" : 0, "propulsion" : 12, "construction" : 18, 
                                  "electronics" : 0, "biotechnology" : 0, "resources" : 700, 
                                  "iron" : 50, "bor" : 20, "ger" : 20, "hull mass" : 'inf', "range" : 800}, 
            "Stargate any/any" : {"energy" : 0, "weapons" : 0, "propulsion" : 19, "construction" : 24, 
                                  "electronics" : 0, "biotechnology" : 0, "resources" : 800, 
                                  "iron" : 50, "bor" : 20, "ger" : 20, "hull mass" : 'inf', "range" : 'inf'}} 

def items_mass_drivers():
    return {
        "Mass Driver 5" : {"energy" : 4, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 0, "biotechnology" : 0, "resources" : 70, 
                           "iron" : 24, "bor" : 20, "ger" : 20, "warp" : 5}, 
        "Mass Driver 6" : {"energy" : 7, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 0, "biotechnology" : 0, "resources" : 144, 
                           "iron" : 24, "bor" : 20, "ger" : 20, "warp" : 6}, 
        "Mass Driver 7" : {"energy" : 9, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                           "electronics" : 0, "biotechnology" : 0, "resources" : 512, 
                           "iron" : 100, "bor" : 100, "ger" : 100, "warp" : 7}, 
        "Super Driver 8" : {"energy" : 11, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                            "electronics" : 0, "biotechnology" : 0, "resources" : 256, 
                            "iron" : 24, "bor" : 20, "ger" : 20, "warp" : 8}, 
        "Super Driver 9" : {"energy" : 13, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                            "electronics" : 0, "biotechnology" : 0, "resources" : 324, 
                            "iron" : 24, "bor" : 20, "ger" : 20, "warp" : 9}, 
        "Ultra Driver 10" : {"energy" : 15, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                             "electronics" : 0, "biotechnology" : 0, "resources" : 968, 
                             "iron" : 100, "bor" : 100, "ger" : 100, "warp" : 10}, 
        "Ultra Driver 11" : {"energy" : 17, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                             "electronics" : 0, "biotechnology" : 0, "resources" : 484, 
                             "iron" : 24, "bor" : 20, "ger" : 20, "warp" : 11}, 
        "Ultra Driver 12" : {"energy" : 20, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                             "electronics" : 0, "biotechnology" : 0, "resources" : 576, 
                             "iron" : 24, "bor" : 20, "ger" : 20, "warp" : 12}, 
        "Ultra Driver 13" : {"energy" : 24, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                             "electronics" : 0, "biotechnology" : 0, "resources" : 676, 
                             "iron" : 24, "bor" : 20, "ger" : 20, "warp" : 13}
    }
                    
def items_terraforming():
    return {"Total Terraform ±3" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                    "electronics" : 0, "biotechnology" : 0, "resources" : 70, "ability" : 3, "variable" : "any"},
            "Total Terraform ±5" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                    "electronics" : 0, "biotechnology" : 3, "resources" : 70, "ability" : 5, "variable" : "any"}, 
            "Total Terraform ±7" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                    "electronics" : 0, "biotechnology" : 6, "resources" : 70, "ability" : 7, "variable" : "any"}, 
            "Total Terraform ±10" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                     "electronics" : 0, "biotechnology" : 9, "resources" : 70, "ability" : 10, "variable" : "any"}, 
            "Total Terraform ±15" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                     "electronics" : 0, "biotechnology" : 13, "resources" : 70, "ability" : 15, "variable" : "any"}, 
            "Total Terraform ±20" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                     "electronics" : 0, "biotechnology" : 17, "resources" : 70, "ability" : 20, "variable" : "any"}, 
            "Total Terraform ±25" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                     "electronics" : 0, "biotechnology" : 22, "resources" : 70, "ability" : 25, "variable" : "any"}, 
            "Total Terraform ±30" : {"energy" : 0, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                     "electronics" : 0, "biotechnology" : 25, "resources" : 70, "ability" : 30, "variable" : "any"}, 
            "Gravity Terraform ±3" : {"energy" : 0, "weapons" : 0, "propulsion" : 1, "construction" : 0, 
                                      "electronics" : 0, "biotechnology" : 1, "resources" : 100, "ability" : 3, "variable" : "gravity"}, 
            "Gravity Terraform ±7" : {"energy" : 0, "weapons" : 0, "propulsion" : 5, "construction" : 0, 
                                      "electronics" : 0, "biotechnology" : 2, "resources" : 100, "ability" : 7, "variable" : "gravity"}, 
            "Gravity Terraform ±11" : {"energy" : 0, "weapons" : 0, "propulsion" : 10, "construction" : 0, 
                                       "electronics" : 0, "biotechnology" : 3, "resources" : 100, "ability" : 11, "variable" : "gravity"}, 
            "Gravity Terraform ±15" : {"energy" : 0, "weapons" : 0, "propulsion" : 16, "construction" : 0, 
                                       "electronics" : 0, "biotechnology" : 4, "resources" : 100, "ability" : 15, "variable" : "gravity"}, 
            "Temp Terraform ±3" : {"energy" : 1, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                   "electronics" : 0, "biotechnology" : 1, "resources" : 100, "ability" : 3, "variable" : "temperature"}, 
            "Temp Terraform ±7" : {"energy" : 5, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                   "electronics" : 0, "biotechnology" : 2, "resources" : 100, "ability" : 7, "variable" : "temperature"}, 
            "Temp Terraform ±11" : {"energy" : 10, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                    "electronics" : 0, "biotechnology" : 3, "resources" : 100, "ability" : 11, "variable" : "temperature"}, 
            "Temp Terraform ±15" : {"energy" : 16, "weapons" : 0, "propulsion" : 0, "construction" : 0, 
                                    "electronics" : 0, "biotechnology" : 4, "resources" : 100, "ability" : 15, "variable" : "temperature"}, 
            "Radiation Terraform ±3" : {"energy" : 0, "weapons" : 1, "propulsion" : 0, "construction" : 0, 
                                        "electronics" : 0, "biotechnology" : 1, "resources" : 100, "ability" : 3, "variable" : "radiation"}, 
            "Radiation Terraform ±7" : {"energy" : 0, "weapons" : 5, "propulsion" : 0, "construction" : 0, 
                                        "electronics" : 0, "biotechnology" : 2, "resources" : 100, "ability" : 7, "variable" : "radiation"}, 
            "Radiation Terraform ±11" : {"energy" : 0, "weapons" : 10, "propulsion" : 0, "construction" : 0, 
                                         "electronics" : 0, "biotechnology" : 3, "resources" : 100, "ability" : 11, "variable" : "radiation"}, 
            "Radiation Terraform ±15" : {"energy" : 0, "weapons" : 16, "propulsion" : 0, "construction" : 0, 
                                         "electronics" : 0, "biotechnology" : 4, "resources" : 100, "ability" : 15, "variable" : "radiation"}} 


def items_restrictions():
    """
    Returns a dict with all of the techs which have a restriction related to
    PRT or LRT. The restrictions have the following forms:
       must be PRT
       must not be PRT
       must have LRT
       must not have LRT
       must have LRT and not LRT
    which will be recorded as follows:
       hasPRT []   (not PRT is same as requires any other PRT)
       hasLRT       
       notLRT
    """
    _allPRT = get_PRT_list()
    _notWM   = [x for x in _allPRT if x != "WM"]
    _notHE   = [x for x in _allPRT if x != "HE"]
    _notAR   = [x for x in _allPRT if x != "AR"]
    _notIS   = [x for x in _allPRT if x != "IS"]
    _notWM_AR= [x for x in _allPRT if x not in ["AR", "WM"]]
    return {
        "SDI" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : []},
        "Missile Battery" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : []},
        "Laser Battery" : {"hasPRT" : [_notWM_AR], "hasLRT" : [], "notLRT" : []},
        "Planetary Shield" : {"hasPRT" : [_notWM_AR], "hasLRT" : [], "notLRT" : []},
        "Neutron Shield" : {"hasPRT" : [_notWM_AR], "hasLRT" : [], "notLRT" : []},
        "Mini-Colony Ship" : {"hasPRT" : ["HE"], "hasLRT" : [], "notLRT" : []},
        "Total Terraform ±3" : {"hasPRT" : [], "hasLRT" : ["TT"], "notLRT" : []},
        "Total Terraform ±5" : {"hasPRT" : [], "hasLRT" : ["TT"], "notLRT" : []},
        "Total Terraform ±7" : {"hasPRT" : [], "hasLRT" : ["TT"], "notLRT" : []},
        "Total Terraform ±10" : {"hasPRT" : [], "hasLRT" : ["TT"], "notLRT" : []},
        "Total Terraform ±15" : {"hasPRT" : [], "hasLRT" : ["TT"], "notLRT" : []},
        "Total Terraform ±20" : {"hasPRT" : [], "hasLRT" : ["TT"], "notLRT" : []},
        "Total Terraform ±25" : {"hasPRT" : [], "hasLRT" : ["TT"], "notLRT" : []},
        "Total Terraform ±30" : {"hasPRT" : [], "hasLRT" : ["TT"], "notLRT" : []},
        "Space Dock" : {"hasPRT" : [], "hasLRT" : ["ISB"], "notLRT" : []},
        "Ultra Station" : {"hasPRT" : [], "hasLRT" : ["ISB"], "notLRT" : []},
        "Death Star" : {"hasPRT" : ["AR"], "hasLRT" : [], "notLRT" : []},
        "Croby Sharmor" : {"hasPRT" : ["IS"], "hasLRT" : [], "notLRT" : []},
        "Shadow Shield" : {"hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []},
        "Robber Baron Scanner" : {"hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []},
        "Pick Pocket Scanner" : {"hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []},
        "Chameleon Scanner" : {"hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []},
        "Super Freighter" : {"hasPRT" : ["IS"], "hasLRT" : [], "notLRT" : []},
        "Battle Cruiser" : {"hasPRT" : ["WM"], "hasLRT" : [], "notLRT" : []},
        "Dreadnought" : {"hasPRT" : ["WM"], "hasLRT" : [], "notLRT" : []},
        "Rogue" : {"hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []},
        "Stealth Bomber" : {"hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []},
        "Midget Miner" : {"hasPRT" : [], "hasLRT" : ["ARM"], "notLRT" : []},
        "Miner" : {"hasPRT" : [], "hasLRT" : ["ARM"], "notLRT" : []},
        "Maxi-Miner" : {"hasPRT" : [], "hasLRT" : [], "notLRT" : ["OBRM"]},
        "Ultra-Miner" : {"hasPRT" : [], "hasLRT" : ["ARM"], "notLRT" : []},
        "Fuel Transport" : {"hasPRT" : ["IS"], "hasLRT" : [], "notLRT" : []},
        "Mini Mine Layer" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Super Mine Layer" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Meta Morph" : {"hasPRT" : ["HE"], "hasLRT" : [], "notLRT" : []},
        "Ferret Scanner" : {"hasPRT" : [], "hasLRT" : [], "notLRT" : ["NAS"]},
        "Dolphin Scanner" : {"hasPRT" : [], "hasLRT" : [], "notLRT" : ["NAS"]},
        "Elephant Scanner" : {"hasPRT" : [], "hasLRT" : [], "notLRT" : ["NAS"]},
        "Viewer 50" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : []},
        "Viewer 90" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : []},
        "Scoper 150" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : []},
        "Scoper 220" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : []},
        "Scoper 280" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : []},
        "Snooper 320X" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : ["NAS"]},
        "Snooper 400X" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : ["NAS"]},
        "Snooper 500X" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : ["NAS"]},
        "Snooper 620X" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : ["NAS"]},
        "Stargate 100/250" : {"hasPRT" : [_notHE], "hasLRT" : [], "notLRT" : []},
        "Stargate any/300" : {"hasPRT" : ["IT"], "hasLRT" : [], "notLRT" : []},
        "Stargate 150/600" : {"hasPRT" : [_notHE], "hasLRT" : [], "notLRT" : []},
        "Stargate 300/500" : {"hasPRT" : [_notHE], "hasLRT" : [], "notLRT" : []},
        "Stargate 100/any" : {"hasPRT" : ["IT"], "hasLRT" : [], "notLRT" : []},
        "Stargate any/800" : {"hasPRT" : ["IT"], "hasLRT" : [], "notLRT" : []},
        "Stargate any/any" : {"hasPRT" : ["IT"], "hasLRT" : [], "notLRT" : []},
        "Mass Driver 5" : {"hasPRT" : ["PP"], "hasLRT" : [], "notLRT" : []},
        "Mass Driver 6" : {"hasPRT" : ["PP"], "hasLRT" : [], "notLRT" : []},
        "Super Driver 8" : {"hasPRT" : ["PP"], "hasLRT" : [], "notLRT" : []},
        "Super Driver 9" : {"hasPRT" : ["PP"], "hasLRT" : [], "notLRT" : []},
        "Ultra Driver 11" : {"hasPRT" : ["PP"], "hasLRT" : [], "notLRT" : []},
        "Ultra Driver 12" : {"hasPRT" : ["PP"], "hasLRT" : [], "notLRT" : []},
        "Ultra Driver 13" : {"hasPRT" : ["PP"], "hasLRT" : [], "notLRT" : []},
        "Robo-Midget Miner" : {"hasPRT" : [], "hasLRT" : ["ARM"], "notLRT" : []},
        "Robo-Miner" : {"hasPRT" : [], "hasLRT" : [], "notLRT" : ["OBRM"]},
        "Robo-Maxi-Miner" : {"hasPRT" : [], "hasLRT" : [], "notLRT" : ["OBRM"]},
        "Robo-Super-Miner" : {"hasPRT" : [], "hasLRT" : [], "notLRT" : ["OBRM"]},
        "Robo-Ultra-Miner" : {"hasPRT" : [], "hasLRT" : ["ARM"], "notLRT" : []},
        "Orbital Adjuster" : {"hasPRT" : ["CA"], "hasLRT" : [], "notLRT" : []},
        "Mine Dispenser 40" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Mine Dispenser 50" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Mine Dispenser 80" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Mine Dispenser 130" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Heavy Dispenser 50" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Heavy Dispenser 110" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Heavy Dispenser 200" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Speed Trap 20" : {"hasPRT" : ["SD", "IS"], "hasLRT" : [], "notLRT" : []},
        "Speed Trap 30" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Speed Trap 50" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Colonization Module" : {"hasPRT" : [_notAR], "hasLRT" : [], "notLRT" : []},
        "Orbital Construction Module" : {"hasPRT" : ["AR"], "hasLRT" : [], "notLRT" : []},
        "Settler's Delight" : {"hasPRT" : ["HE"], "hasLRT" : [], "notLRT" : []},
        "Fuel Mizer" : {"hasPRT" : [], "hasLRT" : ["IFE"], "notLRT" : []},
        "Interspace-10" : {"hasPRT" : [], "hasLRT" : ["NRSE"], "notLRT" : []},
        "Sub-Galactic Fuel Scoop" : {"hasPRT" : [], "hasLRT" : [], "notLRT" : ["NRSE"]},
        "Trans-Galactic Fuel Scoop" : {"hasPRT" : [], "hasLRT" : [], "notLRT" : ["NRSE"]},
        "Trans-Galactic Super Scoop" : {"hasPRT" : [], "hasLRT" : [], "notLRT" : ["NRSE"]},
        "Trans-Galactic Mizer Scoop" : {"hasPRT" : [], "hasLRT" : [], "notLRT" : ["NRSE"]},
        "Galaxy Scoop" : {"hasPRT" : [], "hasLRT" : ["IFE"], "notLRT" : ["NRSE"]},
        "Transport Cloaking" : {"hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []},
        "Ultra-Stealth Cloak" : {"hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []},
        "Jammer 10" : {"hasPRT" : ["IS"], "hasLRT" : [], "notLRT" : []},
        "Jammer 50" : {"hasPRT" : ["IS"], "hasLRT" : [], "notLRT" : []},
        "Flux Capacitor" : {"hasPRT" : ["HE"], "hasLRT" : [], "notLRT" : []},
        "Energy Dampener" : {"hasPRT" : ["SD"], "hasLRT" : [], "notLRT" : []},
        "Tachyon Detector" : {"hasPRT" : ["IS"], "hasLRT" : [], "notLRT" : []},
        "Anti-matter Generator" : {"hasPRT" : ["IT"], "hasLRT" : [], "notLRT" : []},
        "Retro Bomb" : {"hasPRT" : ["CA"], "hasLRT" : [], "notLRT" : []},
        "Smart Bomb" : {"hasPRT" : ["_notIS"], "hasLRT" : [], "notLRT" : []},
        "Neutron Bomb" : {"hasPRT" : ["_notIS"], "hasLRT" : [], "notLRT" : []},
        "Enriched Neutron Bomb" : {"hasPRT" : ["_notIS"], "hasLRT" : [], "notLRT" : []},
        "Peerless Bomb" : {"hasPRT" : ["_notIS"], "hasLRT" : [], "notLRT" : []},
        "Annihilator Bomb" : {"hasPRT" : ["_notIS"], "hasLRT" : [], "notLRT" : []},
        "Mini Gun" : {"hasPRT" : ["IS"], "hasLRT" : [], "notLRT" : []},
        "Gatling Neutrino Cannon" : {"hasPRT" : ["WM"], "hasLRT" : [], "notLRT" : []},
        "Blunderbuss" : {"hasPRT" : ["WM"], "hasLRT" : [], "notLRT" : []},
        "Fielded Kelarium" : {"hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []},
        "Depleted Neutronium" : {"hasPRT" : ["SS"], "hasLRT" : [], "notLRT" : []}
    }

def order_tech():
    """Returns all of the tech in a dict. The struct of the dict is:
    {category : {tech ....}}
    This function also adds the restrictions to the tech obtained from items_restrictions
    """
    #get all of the dicts
    tech = {"armor" : items_armor(),
            "beam weapons" : items_beams(),
            "bombs" : items_bombs(),
            "electrical" : items_electrical(),
            "engines" : items_engines(),
            "mechanical" : items_mechanical(),
            "mine layers" : items_minelayers(),
            "mining robots" : items_miningrobots(),
            "orbital" : dict(list(items_stargates().items()) +  list(items_mass_drivers().items())),
            "planetary" : dict(list(items_planetary_defenses().items()) + list(items_planetary_scanners().items())),
            "scanners" : items_scanners(),
            "shields" : items_shields(),
            "ship hulls" : items_hulls(),
            "starbase hulls" : items_starbases(),
            "terraforming" : items_terraforming(),
            "torpedoes" : items_torpedoes()}

    #add empty lists as the restriction for all tech
    for v1 in tech.values():
        for v2 in v1.values():
            v2.update({"hasPRT" : [], "hasLRT" : [], "notLRT" : []})
    
    restrictions = items_restrictions()

    for k1, v1 in restrictions.items():
        found = False
        for k2, v2 in tech.items():
            if k1 in v2.keys():
                found = True
                for k4, v4 in v1.items():
                    tech[k2][k1][k4] = v4
        if not found:
            raise ValueError("Trying to apply a restriction to tech '{}' but it wasn't found in tech".format(k1))
    return tech
