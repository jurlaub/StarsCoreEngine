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

"""

Note:   See research.py for interaction between productionQ, research, and Order 
        of Events. 



Question:   does .x file update productionQ (at player level?) 
            Is each colony updated with orders or do the orders stay at the 
            player object level. 



productionQ:
        
        ShipDesign:
            Ships 
            Starbase
        Planetary Installations:
            Scanner
            Defenses
            Terraform   # works on the one which would be most beneficial?
        Mines
        Factories
        Minerals
        Special

        Support (expansion on original - for later)
        Dedicate to Research (expansion)



        Miniaturization:
        Input: techLevel, techTree, LRT
        Output: revise the values in productionItems
 
        Items that Miniaturization impacts are the PlayerDesigns. No planetInstallations
        are impacted or other items. 

        After Technology research occurs, each players ShipDesigns are updated.
        ProductionQ tracks how much is spent on any given item. The ShipDesign 
        values are compared to the spent items. If more was spent then is needed
        due to Miniaturization then that is unfortunate. (no refunds of minerals 
        or resources, if overspent)



"""


class ProductionQ(object):
    """ ProductionQ
    One ProductionQ object should exist for each colony object.


    """

    itemType = ('Ship', 'Starbase', 'Scanner', 'Defenses', 'Mines', \
                 'Factories', 'Terraform', 'Minerals','Special')

    defaultSetting = ()     # default options for all Q's

    def __init__(self, colony, player):         # defaultSetting may not be necessary.
        

        #self.productionList = [] # shipDesigns + starbaseDesign + planetInstallations + autoBuild
        self.colony = colony
        self.research = player.research
        self.raceData = player.raceData
        self.designs = player.designs

        self.prodQueue = []
        self.ExcludedFromResearch = False
        self.customDefaultSettings = []

        self.productionOrder = []   # each order should point to a unique item  
        self.productionItems = {}   # 


        pass

    def addToQueue(self):
        """
        Multiple types of entries:
        1) autoBuild orders
        2) quantity 1 items
        3) quantity n items

        {'itemType':'type', 'itemName': 'name', 'quantity': 3,
        "ironUsed" : 0, "borUsed" : 0, "germUsed" :0, "resourcesUsed" : 0 }

        or

        "materialsUsed" : (0, 0, 0, 0)  == (iron, bor, germ, resources)

        ironUsed, borUsed, etc. are only used when quantity == 1. 



        autoBuild & everything -> 
        need to have a {"finishedForThisTurn" : false} entry. 


        """
        pass

    def productionController(self):
        """
        The productionController is used to 'parse' through the production list == self.prodQueue 
        
        1) It identifies the amount of resources that can be used for production 
        (Calling the self equivalent of Research.colonyResearchTax(colony) method to obtain the # 
        of resources available )
        
        2) next it examines the next item in the Q. 
    
        2b) if "quantity" : n > 1,
            call a special helper method dealing with producing multiples of an 
            item, the method will determine how many 'whole' items can be built 
            with the available resources & materials. The respective items will 
            be built by calling the approprate method.

        2ba) if more of the 'item' needs to be built, quantity > 2,
             A new quantity 1 entry should be entered into the productionQ at 
             the beginning of the list. It should consume as many resources as 
             possible. 
             The quantity > 2 entry should be decremented
        2bb) if the 'item' is quantity == 2:
             A new quantity 1 entry should be entered into the productionQ at 
             the beginning of the list. It should consume as many resources as 
             possible.
             The quantity > 2 entry should be decremented to 1, it should have
             all the 'attributes' necessary for a quantity 1 entry      
        2bc) if 'item' quantity == 1:
             It should consume as many resources as 
             possible.
        2bd) if 'item' quantity == 0:
             item should be removed from productionQ and productionList
     
         
        !!  
        3) if items in the queue cannot be completed due to lack of resources, 
        follows AutoMinerals, and tries again, until production is completed or
        resources depletion.

        4) if not AutoMinerals, and still have resources, complete the next item
        until minerals are depleted.
        then choose the next item in the default list that can be completed, 
        

        Misc) removes completed item if approprate



 20150117 ju - NOTE: ProductionQ instructions may specifiy to produce 'n' of a 
              ShipDesign. Only 1 of a design should be produced at a time.
            Once 
              produced the 'n' value should be decremented. If '0' then proceed
              to the next instruction.
 

20150207 ju - partially complete items in the queue -> resource 'spent'/'used' 
            must be proportional to the materials available. It would be 
            ridiculious to set aside 100% of the resources with none of the 
            materials. 

            Solution1: use a ratio
            the sum of remaining materials as defined by target item / 
            the sum of available required materials





        producitonQ
        while True:
        > Find next entry
        >> if at the end
        >> start at beginning, if "finishedForThisTurn" == True, move to next entry
        >> if empty(or at end of list) -> break
        >> Act on autoBuild orders only once (unless its autoBuild minerals in order to complete a project)
        
        > obtain target materials and resources (access to colony.planet, raceData, research, PlayerDesign)

        > Do I have the resources to complete the entry?
        > Do I have the materials to complete the entry?
        >> if yes -> complete entry
        
        >> if no -> 
        >>> is quantity > 1:
        >>>> if yes -> create a single entry, add to beginning, (continue - or use as many resources as possible, break.)
        >>>> if no -> (does the Q need to autobuild minerals? if yes, add to beginning, continue) 
                    -> use as many resources and materials as are available, update ironUsed etc.

        > Do I have resources left? 
        >> if yes -> continue
        >> if no -> break



        """
        iron = self.colony.planet.surfaceIron
        bor  = self.colony.planet.surfaceBor
        germ = self.colony.planet.surfaceGerm
        res = 0



        if self.ExcludedFromResearch:
            res  = self.colony.totalResources
        else:
            # now I've thought about it, this won't update the yearlyResearchResources as it isn't an
            # instance of research, only the class?
            res  = self.research.colonyResourcesAfterTax(self.colony)

        # handle the produceAutoMineral setting?

        while True:

            if not self.productionList:     
                break




            # check all items in list if count 
            if res > 0: 
                continue
            else:
                break


        # for line in self.prodQueue:
        #     #if line["itemType"] not autobuild something 
        #     for item in range(line["quantity"]):
        #         #if item isn't completed then want to create a new line at the start of the Q, can't really
        #         #change the current line as if quantity > 1 then the following items would have less cost

        #         #enough minerals, at least one res can start
        #         if iron >= line["reqIron"] and bor >= line["reqBor"] and ger >= line["reqGerm"] and res > 0: 
        #             #remove minerals
        #             iron -= line["reqIron"]
        #             bor  -= line["reqBor"]
        #             germ -= line["reqGerm"]
        #             #build one
        #             if res >= line["reqResources"]:
        #                 if line["itemType"] == 'Ship':
        #                     self.produceShip()
        #                 elif line["itemType"] == 'Starbase':
        #                     self.produceStarbase()
        #                 elif line["itemType"] == 'Scanner':
        #                     self.producePlanetaryInstallation()
        #                 elif line["itemType"] == 'Defenses':
        #                     self.producePlanetaryInstallation()
        #                 elif line["itemType"] == 'Mines':
        #                     self.producePlanetUpgrades()
        #                 elif line["itemType"] == 'Factories':
        #                     self.producePlanetUpgrades()
        #                 elif line["itemType"] == 'Terraform':
        #                     self.producePlanetUpgrades()
        #                 elif line["itemType"] == 'Minerals':
        #                     self.producePlanetUpgrades()
        #                 elif line["itemType"] == 'Special':
        #                     self.produceSpecial()

        #                 #remove from Q
        #                 line["quantity"] -= 1
        #                 if line["quantity"] == 0:
        #                     self.prodQueue.pop(0)
        #                 res -= line["reqResources"]

        #             #start building but don't finish
        #             else:
        #                 progress = float(res) / line["reqResources"]
        #                 partiallyBuiltItem = {}
        #                 for k, v in line.items():
        #                     partiallyBuiltItem[k] = v
        #                 partiallyBuiltItem["reqIron"] = 0
        #                 partiallyBuiltItem["reqBor"]  = 0
        #                 partiallyBuiltItem["reqGerm"] = 0
        #                 partiallyBuiltItem["reqResouces"] -= res
        #                 partiallyBuiltItem["progress"] = progress
        #                 partiallyBuiltItem["quantity"] = 1
        #                 #replace line in Q
        #                 if line["quantity"] == 1:
        #                     self.prodQueue[0] = partiallyBuiltItem 
        #                 else:
        #                     line["quantity"] -= 1
        #                     self.prodQueue.insert(partiallyBuiltItem, 0)
        #         #Q either blocked as not enough mineral left, or no resources left     
        #         else:
        #             break

        # self.colony.surfaceIron = iron
        # self.colony.surfaceBor = bor
        # self.colony.surfaceGerm = germ
        # Research.yearlyResearchResources += res
        
        
    def updateQCosts(self):
        """
        Q persists across turns, but the cost of ships\starbases will change due to tech changes or redesign,
        not sure how to change the dict of items in the prodQ list with changes to ship designs?

        also need to change costs of design of starbase if upgrading
        """
        pass

    def produceAutoMinerals(self):
        """
        may be the same as produceMinerals. The auto part may be handled in the 
        controller

        """
        pass

    def produceMinerals(self):
        """
        using resources to 'alchemy' minerals
        """

        pass
    
    def produceDefault(self):
        """
        if items on the list cannot be produced because of a need for 

        """
        pass

    def consumeRequiredElements(self):
        """
        used to reduce elements like iron,bor,germ perportionally to what is available.

        """
        pass

    def produceShip(self):
        """
        produces ShipDesign, instantiates Token, looks for available fleet that 
        Token can be added to. If no available fleet, generate fleet. 

        """

        pass

    def produceStarbase(self):
        """produces starbase, instantiates Token, assigns to Colony. """
        pass


    def producePlanetaryInstallation(self):
        """
        'Scanner', 'Defenses'

        """
        pass

    def producePlanetUpgrades(self):
        """
        'Mines', 'Factories', 'Terraform', 'Minerals'

        """
        pass

    def produceSpecial(self):
        """ 
        like the MT Genesis device

        """
        pass






