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

        pass

    def addToQueue(self):
        """
        updates the self.prodQueue list with a dictionary?
        {'itemType':'type', 'itemName': 'name', 'quantity': 3, 'progress': 'resources',
            'reqIron': 0, 'reqBor':0, 'reqGerm':0, 'reqResources':0 }

            --TODO-- figure out if 'progress' includes percentage of minerals. 
                it would seem that the total project would be reviewed, if any 
                one of the required items were needed, then it would work up to the 
                percentage of the available material and then halt. 

            --TODO-- Default and Auto queue orders should be added the same way?
            perhaps they are merely settings - but I seem to remember that they 
            were entries in the queue.


        """
        pass

    def productionController(self):
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


        """

        # handle the produceAutoMineral setting?

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







