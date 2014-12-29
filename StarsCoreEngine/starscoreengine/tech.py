
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
    """CoreStats captures the parts of a Component and ShipDesign that are shared.

    Note: with ShipDesign subclassing Component - there may not be a need to 
    seperate this out anymore. 

    """

    def __init__(self):
            # Costs
        self.iron = 0
        self.bor = 0
        self.germ = 0
        self.resources = 0

        # Some witty 'Mass' related grouping
        self.mass = 0
        self.initative = None
        self.cloaking = None
        self.battleMovement = None

        # 20141228 ju -> It would be nice to have a consitent value across all compononets for fuel/cargo capacity
        # the capacity is a function of Hull and components. The currently stored value is a part of the specific design

        self.fuelCapacity = None       # max fuel capacity
        self.cargoCapacity = None   # max cargo capacity    




class BaseTech(CoreStats):
    """BaseTech captures the parts of a Component and Hull that are shared.

    """
    
    def __init__(self):
        super(BaseTech,self).__init__()
        self.name = None            # tech object name (game name for object)
        self.itemType = None


        self.special = None     
        self.fuelGeneration = None

        # fuel & cargo in CoreStats

        self.hasPRT = None
        self.hasLRT = None
        self.notLRT = None

        # Tech Requirements
        self.energy = 0
        self.weapons = 0
        self.propulsion = 0
        self.construction = 0 
        self.electronics = 0
        self.biotechnology = 0
     



class Component(BaseTech):
    """ Component 

    Captures all information about components (and are not Hull related).

    *** - Update an attribute -> update the 'staticmethods'  --**

    'staticmethods' should capture the component attributes. They are used in the
    custom tech dialog.

    """

    def __init__(self):
        super(Component, self).__init__()
        # self.name = None
        self.itemID = None
        #self.typeDict = {}   # unnecessary as the types are handled prior to instantiation



        #engines
        self.optimalSpeed = None
        self.freeSpeed = None
        self.safeSpeed = None   # still necessary with warp10safe?
        self.radiation = False
        
        # 20141228 ju -> seems like a nicer solution for warp to use fuelEfficiencies list
        # but the warp# seems more explicit. The question becomes - what is more readable and maintanable? 
        # And does it matter in this case?  BTW - the list seems better for expansion (like ships moving warp10+ :) )
        # perhaps a function in custom tech tree can then feed into the fuelEfficiencies list. 
        # 
        #self.warp1 = None
        #self.warp2 = None 
        #self.warp3 = None 
        #self.warp4 = None 
        #self.warp5 = None 
        #self.warp6 = None
        #self.warp7 = None 
        #self.warp8 = None 
        #self.warp9 = None 
        #self.warp10 = None
        
        #fuel & battleSpeed calculations easier to do if fuel efficiency is in a list, then can
        #just do eff = fuelEff[speed]
        self.fuelEfficiencies = []  #  
        self.warp10safe = False


        #weapons
        self.range = None
        self.beamPower = None
        self.sapper = False         # sapper = shield damage only
        self.missilePower = None    # both torpedo & missile damage power 
        self.minesSwept = None
        self.accuracy = None

        self.hitChance = None 
        self.doubleDamageUnshielded = False     # for 'Missile' (as opposed to 'Torpedos') 


        #bombs
        self.popKillPercent = None
        self.minKill = None
        self.installations = None

        #minelayer
        self.minesPerYear = None
        self.terraform = False

        #Electrical
        self.tachyon = None
        self.deflector = None
        self.capacitor = None

        #Mechanical
        self.beamDeflector = None
        #self.movement = None

        # self.fuel = None
        self.colonizer = None
        # self.cargo = None  

        #scanner
        self.normalScanRange = None
        self.penScanRange = None
        self.stealFromShips = False   
        self.stealFromPlanets = False

        #Armor
        self.armorDP = None

        #Shields
        self.shieldDP = None


    def updateElements(self):
        """ 
        updateElements is probably not needed. Something like this would 
        work better in ShipDesign for updating the Ship Design values.

        """
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

    @staticmethod
    def costs():
        return {'iron': 0, 'bor': 0, 'germ': 0, 'resources': 0, 'mass': 0}

    @staticmethod
    def techRequirements():
        return {'energy': 0, 'weapons': 0, 'propulsion': 0, 
        'construction': 0,'electronics': 0, 'biotechnology': 0}

    @staticmethod
    def base():
        """ 
        'special' is most likely to be removed
        """
        return {'name': 'None', 'itemType': 'None', 'initative': 'None', 
                'cloaking': 'None', 'battleMovement': 'None', 'special': 'None',     
                'fuelGeneration': 'None', 'hasPRT': 'None', 'hasLRT': 'None', 
                'notLRT': 'None', 'fuelCapacity': 'None', 'cargoCapacity': 'None'}


    @staticmethod
    def engines():
        return { 'optimalSpeed' : 'None',
                'freeSpeed' : 'None', 'safeSpeed' : 'None', 'radiation' : 'False', 
                'warp1' : 'None', 'warp2' : 'None', 'warp3' : 'None', 'warp4' : 'None', 
                'warp5' : 'None', 'warp6' : 'None', 'warp7' : 'None', 'warp8' : 'None',
                'warp9' : 'None', 'warp10' : 'None', 'warp10safe' : 'False'}

    @staticmethod
    def weapons():
        return {'range': 'None', 'sapper' : 'None', 'beamPower': 'None', 'missilePower': 'None', 
                'minesSwept': 'None', 'accuracy': 'None'}

    @staticmethod
    def bombs():
        return {'popKillPercent': 'None', 'minKill': 'None', 
                'installations': 'None'}

    @staticmethod
    def mineLayer():
        return  {'minesPerYear': 'None', 'terraform': 'False'}

    @staticmethod
    def electronics():
        return {'tachyon': 'None', 'deflector': 'None', 'capacitor': 'None', 
                'cloaking': 'None' }      # may need to change cloaking

    @staticmethod
    def orbital():
        return {'safeGatableMass': 'None', 'safeRange': 'None', 
                'warpDriverSpeed': 'None'}
        
    @staticmethod
    def planetaryInstallations():
        return {'normalScanRange': 'None', 'penScanRange': 'None'} # 'defenses40': 'None', 'defenses80': 'None'

    @staticmethod
    def terraforming():
        return {'modGrav' : 'None', 'modTemp': 'None', 'modRad': 'None'}

    @staticmethod
    def mechanical():
        return {'beamDeflector': 'None', 'fuelCapacity': 'None', 'cargoCapacity': 'None', 
                'colonizer': 'None'}        # 'fuelCapacity' & 'cargoCapacity' are held within BaseTech
 
    @staticmethod
    def scanner():
        return {'normalScanRange': 'None', 'penScanRange': 'None', 
                'stealFromShips': 'False', 'stealFromPlanets': 'False'}

    @staticmethod
    def armor():
        return {'armorDP': 'None'}

    @staticmethod
    def shields():
        return {'shieldDP': 'None'}


    @staticmethod
    def hull():
        """
        The items in Hull may need to be incorporated into the component object.
        """
        print("Component().hull() custom component Not Implemented")

    # method for checking that static methods match component attributes.






class Hull(BaseTech):

    def __init__(self):
        super(Hull,self).__init__()
        self.shipType = None    # Miner, Transport, Armed, ect.

        # self.fuel = None           # amount of current fuel
        # self.fuelCapacity = 0      # max fuel transported in the ship

        self.armorDP = 0
        
        self.mineLayerDouble = False
        self.shipsHeal = False

        self.ARPopulation = None
        self.spaceDockSize = None


        # slot defines the hull component composition
        self.slot = {
            "A":{"objectType": ["engine"], "slotsAvalable":1 }, 
            "B":{"objectType":["itemType"],  "slotsAvalable":2}}  # each key == specific slot

        # identify slots:
        #   slot type -> General, Engine, Weap, Mech, Elect, etc
        #   how many slots available

        # specify all ship related question?


class ShipDesign(Component):
    ''' ShipDesign is a specific user defined design of the Hull class 


    ShipDesign is a subclass of CoreStats. As components are added or removed, 
    these values are updated. Perhaps subclassing Component would be better. 
    As Components are added/removed they could update the ShipDesign Component values. 
    The final design would capture all the designs capabilities. 
    
    20141226 - ju - I think subclassing Component is better.



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
        
        # 20141228 ju -> "capacity" should be captured by the BaseTech.fuelCapacity
        #               A value is needed to capture the currently held fuel/cargo
        # self.fuel_capacity = 0  #can be different to hull due to fuel tanks
        # self.cargo_capacity = 0 #can be different to hull due to cargo tanks
        self.fuel = 0            # amount of currently held fuel  
        self.cargo = 0           # amount contained in cargo hold

        # 20141228 ju -> this information is already captured in Ship Design by 
        #               it subclassing Component (inherits from CoreStats)
        #need to be reevaluated every turn to take into account tech changes, need to know them both 
        #for production cost and for evaluating attractiveness in battle
        # self.iron = None
        # self.bor  = None
        # self.germ = None
        # self.resources = None

        #20141228 ju -> These are calculated values and are somewhat different 
        #   from fuelCapacity (which is basically the sum of all fuelCapacity in a design)
        #   It seems better for this sort of value to be separate.
        self.deflector_effectiveness = None
        self.jamming_effectiveness = None
        self.computing_power = None

    def componentDict(self, key, value):

        '''
        if key is electrical:
            update the ship designs electrical object values?
            update BaseTech values + objects values?
        '''
        pass










