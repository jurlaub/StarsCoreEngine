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
        
        May be directly connected to a colony. Alternative is its connected directly to player object.

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


"""


class ProductionQ(object):
    """ ProductionQ
    One ProductionQ object should exist for each colony object.


    """

    itemType = ('Ship', 'Starbase', 'Scanner', 'Defenses', 'Mines', \
                 'Factories', 'Terraform', 'Minerals','Special')

    defaultSetting = ()     # default options for all Q's

    def __init__(self, colony, defaultSetting):         # defaultSetting may not be necessary.
        


        self.colony = colony
        self.defaultSetting = defaultSetting
        self.prodQueue = []
        self.ExcludedFromResearch = False
        self.customDefaultSettings = []

        self.productionOrder = []   # each order should point to a unique item  
        self.productionItems = {}   # 


        pass

    def addToQueue(self):
        """
        updates the self.prodQueue list with a dictionary?
        {'itemType':'type', 'itemName': 'name', 'quantity': 3, 'progress': 'resources',      #progress is a percentage?
            'reqIron': 0, 'reqBor':0, 'reqGerm':0, 'reqResources':0 }

        to prevent the starbase bug (or whatever its called when you 99% complete an empty hull and then
        edit the design to get all of the components for free, it might be useful to have both reqIron and
        spentIron, so that if the design changes the reqIron can be increased, rather than the way I've implemented
        it which just sets reqIron to 0 once production starts

            --TODO-- figure out if 'progress' includes percentage of minerals. 
                it would seem that the total project would be reviewed, if any 
                one of the required items were needed, then it would work up to the 
                percentage of the available material and then halt. 

            --TODO-- Default and Auto queue orders should be added the same way?
            perhaps they are merely settings - but I seem to remember that they 
            were entries in the queue.
        
            #110115 MF - How about treat them as entries (with their own itemType) in the Q, and then
                         have the productionController temporarily remove them, insert the appropriate itemType 
                         and quantity, taking into account the available miners etc so that it won't block the Q,
                         and then re-insert the auto entry once its finished production, ready for the next turn?


        """
        pass

    def productionController(self, techLevel = {}):
        """
        The productionController is used to 'parse' through the production list == self.prodQueue 
        
        1) It identifies the amount of resources that can be used for production 
        (Calling the Research.colonyResearchTax(colony) method to obtain the # 
        of resources available )
        
        2) next it examines the next item in the Q. Calls the approprate method. 
        that method handles the item production, resource reduction, and object
        instantiation. Continues while there are objects in the queue that can 
        completed. 

        3) if items in the queue cannot be completed due to lack of resources, 
        follows AutoMinerals, and tries again, until production is completed or
        resources depletion.

        4) if not AutoMinerals, and still have resources, complete the next item
        until minerals are depleted.
        then choose the next item in the default list that can be completed, 
        

        Misc) removes completed item if approprate


 20150117 ju - Miniaturization:
            when starting work, prior to work being finished. The design should 
            called to determine if Miniaturization occurs. The required minerals
            and resources should be updated to reflect Miniaturization. 
            Actual Values in ShipDesign should NOT be updated/revised. 

            techLevel added to accomodate this. NOTE: production is called from OrderOfEvents.

 20150117 ju - NOTE: ProductionQ instructions may specifiy to produce 'n' of a 
              ShipDesign. Only 1 of a design should be produced at a time.
              (This is when the Miniaturization value would be calculated) Once 
              produced the 'n' value should be decremented. If '0' then proceed
              to the next instruction.


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
            res  = Research.colonyResourcesAfterTax(self.colony)

        # handle the produceAutoMineral setting?

        for line in self.prodQueue:
            #if line["itemType"] not autobuild something 
            for item in range(line["quantity"]):
                #if item isn't completed then want to create a new line at the start of the Q, can't really
                #change the current line as if quantity > 1 then the following items would have less cost

                #enough minerals, at least one res can start
                if iron >= line["reqIron"] and bor >= line["reqBor"] and ger >= line["reqGerm"] and res > 0: 
                    #remove minerals
                    iron -= line["reqIron"]
                    bor  -= line["reqBor"]
                    germ -= line["reqGerm"]
                    #build one
                    if res >= line["reqResources"]:
                        if line["itemType"] == 'Ship':
                            self.produceShip()
                        elif line["itemType"] == 'Starbase':
                            self.produceStarbase()
                        elif line["itemType"] == 'Scanner':
                            self.producePlanetaryInstallation()
                        elif line["itemType"] == 'Defenses':
                            self.producePlanetaryInstallation()
                        elif line["itemType"] == 'Mines':
                            self.producePlanetUpgrades()
                        elif line["itemType"] == 'Factories':
                            self.producePlanetUpgrades()
                        elif line["itemType"] == 'Terraform':
                            self.producePlanetUpgrades()
                        elif line["itemType"] == 'Minerals':
                            self.producePlanetUpgrades()
                        elif line["itemType"] == 'Special':
                            self.produceSpecial()

                        #remove from Q
                        line["quantity"] -= 1
                        if line["quantity"] == 0:
                            self.prodQueue.pop(0)
                        res -= line["reqResources"]

                    #start building but don't finish
                    else:
                        progress = float(res) / line["reqResources"]
                        partiallyBuiltItem = {}
                        for k, v in line.items():
                            partiallyBuiltItem[k] = v
                        partiallyBuiltItem["reqIron"] = 0
                        partiallyBuiltItem["reqBor"]  = 0
                        partiallyBuiltItem["reqGerm"] = 0
                        partiallyBuiltItem["reqResouces"] -= res
                        partiallyBuiltItem["progress"] = progress
                        partiallyBuiltItem["quantity"] = 1
                        #replace line in Q
                        if line["quantity"] == 1:
                            self.prodQueue[0] = partiallyBuiltItem 
                        else:
                            line["quantity"] -= 1
                            self.prodQueue.insert(partiallyBuiltItem, 0)
                #Q either blocked as not enough mineral left, or no resources left     
                else:
                    break

        self.colony.surfaceIron = iron
        self.colony.surfaceBor = bor
        self.colony.surfaceGerm = germ
        Research.yearlyResearchResources += res
        
        
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






