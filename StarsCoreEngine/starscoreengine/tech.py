
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

"""


"""

DEBUG = False

class CoreStats(object):
    """CoreStats captures the parts of a Component and ShipDesign that are shared.

    Note: with ShipDesign subclassing Component - there may not be a need to 
    seperate this out anymore. 


    Miniaturization: 
    Actual ship values should never be updated. Miniaturization
    values should always be calculated when design is to be built. 

    """

    def __init__(self):
            # Costs
        self.iron = 0
        self.bor = 0
        self.germ = 0
        self.resources = 0

        # Some witty 'Mass' related grouping
        self.mass = 0
        self.initiative = 0
        self.cloaking = 0
        self.battleMovement = 0  #  ['/', 'fi', 'fl', '1', '1/', '1fi', '1fl', '2', '2/', '2fi']
                                    #  [.25, .5, .75, 1, 1.25 ... ]  # what is up with the use of 'fi'    

        # 20141228 ju -> It would be nice to have a consitent value across all compononets for fuel/cargo capacity
        # the capacity is a function of Hull and components. The currently stored value is a part of the specific design

        self.fuelCapacity = 0       # max fuel capacity
        self.cargoCapacity = 0   # max cargo capacity    




class BaseTech(CoreStats):
    """BaseTech captures the parts of a Component and Hull that are shared.

    """

    # each component should be one of the following object types
    objectTypes =  ("Armor", "Scanner", "Elect", "Mech", "Bomb", "Engine",  
                    "Minelayer", "Mining", "PlanetaryScanner",
                    "Shield", "Armor", "Torpedoes", "Terraforming", 
                    "PlanetaryDefenses", "Ships", "Starbases", "Orbital", "BeamWeapons")
    
    def __init__(self):
        super(BaseTech,self).__init__()
        self.name = None            # tech object name (game name for object)
        self.itemType = None        # should be one of the above objectTypes


        #self.special = None        # depreciated (probably)
        self.fuelGeneration = None  # None or amount fuel generated per year

        # fuel & cargo in CoreStats

        self.hasPRT = []    # if empty, all can use. If not empty, only that value can use (all not appearing in list are excluded)
        self.hasLRT = []    # must have LRT to produce, 
        self.notLRT = []    # if it appears in this list, you are excluded

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


    All base attributes:
    True / False : they must be False in this file


    """

    def __init__(self):
        super(Component, self).__init__()

        self.itemID = None      # name of item




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
        self.fuelEfficiencies = None  #  replace with list
        self.warp10safe = False


        """ #weapons
        All weapons attribues need to be redone. 

        this is to cover random cases where a user may put varied ranged weapons
        on a ship. 
        """
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
        self.minPopKill = None
        self.installations = None

        #minelayer
        self.minesPerYear = None
        self.terraform = False

        # mining
        self.mineralKTPerYear = None

        #Electrical
        self.jammer = None      # [10, ]
        self.dampener = None    # [1, 1, 1]
        self.tachyon = None       
        self.capacitor = None       # [.1, .2, .1] = 2x energy cap & 1x Flux cap. records number of caps

        #Mechanical
        self.beamDeflector = None   # [.1, .1, .1]   3x defectors
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

        #Terraform
        self.terraformVariable = None # replace with value     
        self.teffaformRate = None

        #Orbital
        self.safeGateableMass = None
        self.safeGateableRange = None
        self.warpDriverSpeed = None


        self.shipType = None 
        self.mineLayerDouble = False
        self.shipsHeal = False
        self.ARPopulation = None
        self.spaceDockSize = None



    # def updateElements(self):
    #     """ 
    #     updateElements is probably not needed. Something like this would 
    #     work better in ShipDesign for updating the Ship Design values.

    #     """
    #     extraItems = {}

    #     for eachKey in self.typeDict:
    #         each = self.typeDict[eachKey]
            
    #         # -- TODO -- test if each is a dictionary -> if not then should be a value

    #         for item in each.__dict__:
    #             if item in self.__dict__:
    #                 #print("key:%s\t self:%s; other:%s" % (item, self.__dict__[item], each.__dict__[item] ))
    #                 self.__dict__[item] = each.__dict__[item]
    #                 #print("a %s:%s" % (item, self.__dict__[item]))
    #             else:
    #                 # 
    #                 extraItems[item] = each.__dict__[item]

    #     print("Component:%s had %d items which were not added to the component" % (self.name, len(extraItems)))
    #     print("%s" % extraItems)

    @staticmethod
    def sm_costs():
        return {'iron': 0, 'bor': 0, 'germ': 0, 'resources': 0, 'mass': 0}

    @staticmethod
    def sm_techRequirements():
        return {'energy': 0, 'weapons': 0, 'propulsion': 0, 
        'construction': 0,'electronics': 0, 'biotechnology': 0}

    @staticmethod
    def sm_base():
        """ 
        'special' is most likely to be removed
        """
        return {'name': 'None', 'itemType': 'None', 'initiative': 'None', 
                'cloaking': 'None', 'battleMovement': 'None', 'special': 'None',     
                'fuelGeneration': 'None', 'hasPRT': [], 'hasLRT': [], 
                'notLRT': [], 'fuelCapacity': 'None', 'cargoCapacity': 'None'}


    @staticmethod
    def sm_engines():
        return { 'optimalSpeed' : 'None',
                'freeSpeed' : 'None', 'safeSpeed' : 'None', 'radiation' : 'False', 
                'warp1' : 'None', 'warp2' : 'None', 'warp3' : 'None', 'warp4' : 'None', 
                'warp5' : 'None', 'warp6' : 'None', 'warp7' : 'None', 'warp8' : 'None',
                'warp9' : 'None', 'warp10' : 'None', 'warp10safe' : 'False'}

    @staticmethod
    def sm_weapons():
        return {'range': 'None', 'sapper' : 'None', 'beamPower': 'None', 'missilePower': 'None', 
                'minesSwept': 'None', 'accuracy': 'None'}

    @staticmethod
    def sm_bombs():
        return {'popKillPercent': 'None', 'minPopKill': 'None', 
                'installations': 'None'}

    @staticmethod
    def sm_mineLayer():
        return  {'minesPerYear': 'None', 'terraform': 'False'}

    @staticmethod
    def sm_electronics():
        return {'tachyon': 'None', 'deflector': 'None', 'capacitor': 'None'}      # may need to change cloaking

    @staticmethod
    def sm_orbital():
        return {'safeGatableMass': 'None', 'safeRange': 'None', 
                'warpDriverSpeed': 'None'}
        
    @staticmethod
    def sm_planetaryInstallations():
        return {'normalScanRange': 'None', 'penScanRange': 'None'} # 'defenses40': 'None', 'defenses80': 'None'

    @staticmethod
    def sm_terraforming():
        return {'terraformVariable' : 'None', 'teffaformRate': 'None'}

    @staticmethod
    def sm_mechanical():
        return {'beamDeflector': 'None', 'fuelCapacity': 'None', 'cargoCapacity': 'None', 
                'colonizer': 'None'}        # 'fuelCapacity' & 'cargoCapacity' are held within BaseTech
 
    @staticmethod
    def sm_scanner():
        return {'normalScanRange': 'None', 'penScanRange': 'None', 
                'stealFromShips': 'False', 'stealFromPlanets': 'False'}

    @staticmethod
    def sm_armor():
        return {'armorDP': 'None'}

    @staticmethod
    def sm_shields():
        return {'shieldDP': 'None'}


    @staticmethod
    def sm_hull():
        """
        The items in Hull may need to be incorporated into the component object.
        """
        print("Component().hull() custom component Not Implemented")

    # method for checking that static methods match component attributes.

    @staticmethod
    def sm_orderedAtt():
        """collects all static methods into groups that aims to provide an 
        easier way to customize

        """
        import collections

        tmpDict = collections.OrderedDict()
        v = Component()

        tmpDict.update(v.sm_costs())
        tmpDict.update(v.sm_techRequirements())
        tmpDict.update(v.sm_base())
        tmpDict.update(v.sm_armor())
        tmpDict.update(v.sm_shields())
        tmpDict.update(v.sm_electronics())
        tmpDict.update(v.sm_mechanical())
        tmpDict.update(v.sm_weapons())
        tmpDict.update(v.sm_bombs())
        tmpDict.update(v.sm_scanner())
        tmpDict.update(v.sm_engines())
        tmpDict.update(v.sm_terraforming())
        tmpDict.update(v.sm_planetaryInstallations())
        tmpDict.update(v.sm_orbital())
        tmpDict.update(v.sm_mineLayer())

        return tmpDict




# --TODO-- change to inherit from Component?
class Hull(BaseTech):
    """

    --TODO-- shipType classifcation. A hull has a basic type. Some types can be 
    modified. Armed or Unarmed. Some have multiple, (Rogue hull could be an 
        armed transport.) Some stay the same. 

    """


    def __init__(self):
        super(Hull,self).__init__()
        self.shipType = None    # Miner, Transport, Armed, ect.

        # self.fuel = None           # amount of current fuel
        # self.fuelCapacity = 0      # max fuel transported in the ship

        #self.armorDP = 0            # hulls have innate armor values -> remove if armorDP moves from Component
        
        # self.mineLayerDouble = False
        # self.shipsHeal = False

        # self.ARPopulation = None
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

    ShipDesign is used for both Starbases and Ships.


    ShipDesign is a subclass of CoreStats. As components are added or removed, 
    these values are updated. Perhaps subclassing Component would be better. 
    As Components are added/removed they could update the ShipDesign Component values. 
    The final design would capture all the designs capabilities. 
    
    20141226 - ju - I think subclassing Component is better.


    20150117 - ju - ShipDesign should validate itself

    20150607 - ju: slight change in the use of ShipDesign. ShipDesign will instantiate
    the original technology components and original values for any given design, disregarding
    tech level. PlayerBuildList will hold each turns design costs for a given design.
        -- TODO --- 
            make sure ShipDesign works with the new approach


    vals = {'designName': 'doomShip1', 
            'hullID': 'Scout',
            'component': {"B": {"itemID": "Fuel Mizer", "itemQuantity": 1 },
                          "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                          "C": {"itemID": "Mole Scanner", "itemQuantity": 1}
                         }
            }


    '''

    miniturazationList = ('iron', 'bor', 'germ', 'resources')


    def __init__(self, vals, techTree, techLevel, LRT):                      # vals is a dictionary described in notes above    
        super(ShipDesign,self).__init__()
        
        #self.techTree = techTree  # ?references universal tech tree? 

        self.designName = vals['designName']    # user specified ship design name
        self.designID = None                     # ? -> not, better to track and auto assign.
        self.owner = None 
        self.techTree = techTree       #--TODO-- perhaps save reference to tech

        self.isDesignLocked = False             # once a player has built a design- it cannot change
        self.designValidForProduction = True   


        self.hullID = vals['hullID'] # points to a Hull object ID.  one for each type of ship.
        #self.hullCosts = {"costIron" : 0, "costBor" : 0, "costGerm" : 0, "costResources" : 0}

        # ------------------------- self.component --------------------------
        # component holds the number of items assigned to a design
        # self.component = {  
        #         "A":{"itemID": None, "itemQuantity": None, "costIron": n, "costBor": n, "costGerm" : n, "costResources" :n }, 
        #         "B":{"itemID": None, "itemQuantity": None}}  # capacity
        self.component = vals['component']
        # --------------------------------------------------------------------- 


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


        self.updateDesign(techLevel, LRT)


    def updateDesign(self, techLevel, LRT = []):
        """ collect and update all of the components and hull values. 
        Input: self (hull + components), player techLevel, LRT = CuttingEdge, techTree,
        Output: all values of hull and components are updated in the ShipDesign.
                (e.x. self.iron = sum(hull.iron + each_component.iron values))

        
        Design can be updated after instantiation, however, a tech tree 
        must be provided.

        """
        
        hullObj = self.techTree[self.hullID]

        if DEBUG: print("hullObj:%s" % hullObj.spaceDockSize)
        # apply hullObj miniturization if necessary

        self.tally(1, hullObj, techLevel, LRT)              # there can be only one... (1) Hull :)

        

        if DEBUG: print("updateDesign(hullObj):spaceDockSize:%s \n%s" % (self.spaceDockSize, self.designName))

        for k1, obj1 in self.component.items():

            componentName = obj1['itemID']
            componentObj = self.techTree[componentName]

            componentQuant = obj1['itemQuantity']

            # --TODO-- add miniturazation check and calculation to component.
            self.tally(componentQuant, componentObj, techLevel, LRT)

        

    def tally(self, quant, comp, techLevel, LRT ):

        # tech levels = highest number not sum
        # True/False
        # if attribute starts with None need to 0 out.? 
        # if attribute is []:
        #       add
        skipKey = ('slot', 'component')
        highestLevel = ('energy', 'weapons', 'propulsion', 'construction', 'electronics', 'biotechnology', 'spaceDockSize')          
        oneList = ('fuelEfficiencies', 'itemType', 'range' )
        #extendList = ()

        eachInstanceList = ('jammer', 'dampener', 'tachyon', 'capacitor', 
            'beamDeflector', 'cloaking', 'battleMovement', 'accuracy', 
            'hitChance', 'normalScanRange', 'penScanRange', 'hasPRT', 'hasLRT', 'notLRT')

        
        sumItUpList = ( 'mass','fuelCapacity',
         'cargoCapacity', 'initiative', 'armorDP', 'shieldDP', 'beamPower', 'sapper', 'minesSwept' )

        miniturazationList = ShipDesign.miniturazationList #('iron', 'bor', 'germ', 'resources')

        
        noneVals = ( None, []) 
        tmpVal = False     

        for kee, obj in comp.__dict__.items():

            """ obj either contain noneVals or are trumped by a value (True, a number, not None, a non empty object) """     
            # if obj is 0:
            #     obj = '0'
            if kee == 'spaceDockSize':
                if DEBUG: print("tall: spaceDockSize:%s" % obj)

            if obj in noneVals:         
                continue
            
            if kee in skipKey:        # these should not be changed
                if DEBUG: print("shipKey: %s:%s" % (kee, obj))
                continue
            
            elif kee in highestLevel:
                if kee == 'spaceDockSize':
                    sizeRank = ['0', '200', 'infinite']
                    
                    # if obj is not in sizeRank it is None or some other value
                    if obj in sizeRank:
                        
                        sds = self.__dict__[kee]
                        if sds in sizeRank:
                            #compare index
                            obj_index = sizeRank.index(obj)
                            sds_index = sizeRank.index(sds)
                            if sds_index > obj_index:
                                if DEBUG: print("tally: spaceDockSize - current value (%s) is greater then component value(%s)" % (sds, obj))
                                continue
                        
                        
                        tmpVal = obj



                elif int(self.__dict__[kee]) > int(obj):   #  only want the highest tech level
                    continue
                
                else:
                    tmpVal = int(obj)

            elif kee in oneList:
                if self.__dict__[kee] in ('Ships', 'Starbases'):
                    continue
                else:
                    tmpVal = obj

            elif kee in eachInstanceList:     # for all other lists, extend the list to self
                if isinstance(obj, list):
                    self.__dict__[kee].extend(obj)              # is this form valid?
                else:
                    self.__dict__[kee] = [obj]
                
                continue


            elif kee in sumItUpList:

                if self.__dict__[kee] is None: 
                    self.__dict__[kee] = 0      # 


                tmpVal = int(self.__dict__[kee]) + (int(obj) * int(quant))

            elif kee in miniturazationList:

                if self.__dict__[kee] is None: 
                    self.__dict__[kee] = 0
                
                # use comp == component object to figure out miniturization
                # call designMiniaturization()
                # tuple = (iron, bor, germ, resources)

                # then add it to the ship design
                tmpVal = int(self.__dict__[kee]) + (int(obj) * int(quant))
            

            elif obj is True:
                tmpVal = obj
            
            else:
                if DEBUG: print("tally: %s : %s" % (kee, obj )) 
                
                continue
            self.__dict__[kee] = tmpVal




    # def isShipDesignValid(self, techTree):
    #     """ validShipDesign assesses itself to determine if it is a valid ship 
    #     design. 

    #     Validates that the components added to the design align with the 
    #     Hull.slots. PlayerDesign validate PRT, LRT and Tech Level -> for production.

    #     input: self, techTree
    #     output: 
    #         True = Ship Design has correct components, correct number of components
    #         False = Ship Design has an error

    #     """
    #     pass

    def buildList_ShipDesign(self):

        tmpMass = self.mass

        #call current costs
        tmpCosts = self.currentCosts()

        return {'mass': tmpMass, 'costs':tmpCosts}



    def currentCosts(self):
        """
        currentCosts will obtain list of components assigned to ShipDesign
            costs will begin with running Hull component through designMiniaturization
            iterate through component list
                for each component designMiniaturization will be called
                    designMiniaturization will return stats (miniturized if needed)
                    the stats will be added to the current costs

                miniturazationList = ('iron', 'bor', 'germ', 'resources')

        """
        currentCosts = [self.iron, self.bor, self.germ, self.resources]


        return currentCosts

    
    @staticmethod
    def designMiniaturization(techObj, techLevel = None, LRT = []):
        """designMiniaturizationStats() used to get the CoreStats required to 
        build the design. When a user produces the ship, the productionQ should 
        call this method to determine what values to put in the production que. 

        Miniaturization should not change the actual component values.

        Input: ShipDesign, techLevel, LRT
        Output: tuple of CoreStats (related to building)

        NOTE: Returns core stats after applying Miniaturization (if any)

        tuple = (iron, bor, germ, resources)

        """
        tmpList = []

        for each in ShipDesign.miniturazationList:
            tmpVal = techObj.__dict__[each]

            

        pass

    # static method?
    def canOwnerBuildDesign(self, techLevel, techTree, PRT, LRT = []):
        """
        method updates self.canOwnerBuild

        checks Hull, components, 

        """
        pass


    def componentDict(self, key, value):

        '''
        if key is electrical:
            update the ship designs electrical object values?
            update BaseTech values + objects values?
        '''
        pass











