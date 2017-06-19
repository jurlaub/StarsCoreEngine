
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


from .tech import Component, Hull, CoreStats

DEBUG = True
VERBOSE = False


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
        self.spaceDockSize = None

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

        #print("Hull:%s" % hullObj.__dict__)
        if VERBOSE: print("hullObj:%s" % hullObj.spaceDockSize)
        # apply hullObj miniturization if necessary

        self.tally(1, hullObj, techLevel, LRT)              # there can be only one... (1) Hull :)

        

        if VERBOSE: print("updateDesign(hullObj):spaceDockSize:%s \n%s" % (self.spaceDockSize, self.designName))

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
        highestLevel = ('energy', 'weapons', 'propulsion', 'construction', 'electronics', 'biotechnology', 'spaceDockSize')       #    
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
            # if kee == 'spaceDockSize':
            #     if VERBOSE: print("tall: spaceDockSize:%s" % obj)

            if obj in noneVals:         
                continue
            
            if kee in skipKey:        # these should not be changed
                if VERBOSE: print("shipKey: %s:%s" % (kee, obj))
                continue
            
            elif kee in highestLevel:
                if kee == 'spaceDockSize':
                    #sizeRank = ('0', '200', '-1')
                    sizeRank = (0, 200, Hull.INFINITY) 
                    #assert(isinstance(obj, String))

                    # if obj is not in sizeRank it is None or some other value
                    if obj == Hull.INFINITY:
                        tmpVal = obj
                        print("component: {} set to INFINITY".format(comp.name))

                    elif obj in sizeRank:
                        
                        sds = self.__dict__[kee]
                        print("%s spaceDockSize - existing:%s and potential %s " % (comp.name, sds, obj) )
                        if sds in sizeRank:
                            #compare index
                            obj_index = sizeRank.index(obj)
                            sds_index = sizeRank.index(sds)
                            print("sds: %s  :: obj: %s" % (sds_index, obj_index))
                            if sds_index > obj_index:
                                if DEBUG: print("tally: spaceDockSize - current value (%s) is greater then component value(%s)" % (sds, obj))
                                continue
                        
                        
                        tmpVal = obj
                    else:
                        if DEBUG: print("%s - value not in %s  - value is %s" % (comp.name, sizeRank, obj))


                elif int(self.__dict__[kee]) > int(obj):   #  only want the highest tech level
                    continue
                
                else:
                    tmpVal = int(obj)

                #print("highestLevel: kee: %s value is %s" % (kee,  tmpVal ) )

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
                if VERBOSE: print("tally ignoring value: %s : %s" % (kee, obj )) 
                
                continue
            
            #if kee is 'Starbases': print("Starbase: kee:%s value:%s" % (kee, tmpVal))
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


