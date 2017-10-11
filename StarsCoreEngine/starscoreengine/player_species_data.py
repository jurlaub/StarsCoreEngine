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

from .player_species_traits import SpeciesTraits

class SpeciesData(SpeciesTraits):
    """
    
    habitat: 
    > if radius is -1 this means immune. 

    
    """
    def __init__(self, speciesName):
        self.speciesName = speciesName            # used by universe when generating HW
        self.speciesNamePlural = speciesName
        self.raceIcon = None
        self.LeftOverRWPoints = None

        self.PRT = 'SS'
        self.LRT = []

        self.growthRate = .14
        self.popEfficiency = 1000  # 1 resource per 1000 colonists
        
        '''
        #Environment
        >> Consists of centerpoint & range

        |------<==========x==========>----------------------|

        >> the range value captures only the positive side of the total 
        habitat values 

        immune habitate = -1 radius


        NOTE: May need to adjust to be Upper and Lower bounds because of 'odd' 
        low gravity click spaces 

        '''
        self.habGravityCenter = 1.0  # 1 (centerpoint) total range = .85 to 1.15
        self.habGravRadius = -1         # change to upper/lower bounds   # 15.0 pos range from Center. Total range doubled  
        
        self.habTempCenter = 70 
        self.habTempRadius = -1         # change to upper/lower bounds

        self.habRadCenter = 50
        self.habRadRadius = 13.0        # change to upper/lower bounds

        self.terraformCosts = [0, 0, 0, 100]    # --TODO-- change to dynamic

        self.factoryProduce = 10    # 10 factories produce n resources a year
        self.factoryCost = 10       # a factory cost n resources to build
        self.factoryOperate = 10    # 10,000 colonist operate n factories       
        self.factoryGermCost = False # True = cost 1kt less of Germanium to build

        self.mineProduce = 10       # 10 mines produce n kt of each mineral a year
        self.mineCost = 10         # a mine costs n resources to build
        self.mineOperate = 10       #  10,000 colonist operate n mines
        
        self.defensesCosts = [5, 5, 5, 15]  # --TODO-- change to dynamic
        self.scannerCosts = [10, 10, 70, 100] # --TODO-- change to dynamic
        self.mineralCosts = [0, 0, 0, 100] # --TODO-- change to dynamic


        # Research costs = (75% extra, standard amount, 50% less)
        self.techCostEner = 1 
        self.techCostWeap = 1 
        self.techCostProp = 1 
        self.techCostCon = 1 
        self.techCostElec = 1 
        self.techCostBio = 1 
        
        self.techJumpStart = False # True = All 'Costs 75% extra' fields start at Tech 4


        self.fuelEfficiency = 1  # --TODO-- review
    
    # def setPlayerCosts(self, techTree):
    #     """
    #         Setting the player costs in RaceData class after player has been created.
    #     """
    #     pass





    # def buildCosts_MineFactory(self):
    #     m = "Mines"
    #     f = "Factories"

        
    #     mCosts = [0, 0, 0, self.mineCost]


    #     fGerm = 4
    #     if self.factoryGermCosts: 
    #         fGerm = 3
        
    #     fCosts = [0, 0, fGerm, self.factoryCost]





    #     return { m:{"itemType": m, "targetItemsCost": mCosts}, \
    #             f: {"itemType": f, "targetItemsCost": fCosts} }




