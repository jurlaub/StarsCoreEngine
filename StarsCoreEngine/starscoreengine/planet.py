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

from .space_objects import SpaceObjects
from .fleets import Starbase
from .productionQ import ProductionQ
import random


DEBUG_1 = False
DEBUG_2 = False

class Planet(SpaceObjects):
    """ 
        Planet is the template that provides all the data available for a planet. 


    """
    def __init__(self, xy, ID, name, universe,  origHab = (1.1, 90, 45), origConc = None):
        super(Planet, self).__init__(xy, ID)
        self.name = name    
        self.origHab = origHab              #depreciate
        self.origGrav = origHab[0]
        self.origTemp = origHab[1]
        self.origRad = origHab[2]

        self.currHab = self.origHab         # depreciate
        self.currentTemp = self.origTemp
        self.currentGrav = self.origGrav
        self.currentRad = self.origRad

        self.universe = universe

        #detail current Concentration, random by default
        if not origConc: 
            self.concIron = random.randint(1,135)
            self.concBor = random.randint(1,135)
            self.concGerm = random.randint(1,135)
        else:
            self.concIron = origConc[0]
            self.concBor = origConc[1]
            self.concGerm = origConc[2]
        


        self.currSurfaceMinerals = 0  # depreciate  (should be  3 values in a list)
        self.surfaceIron = 0
        self.surfaceBor = 0
        self.surfaceGerm = 0


        self.HW = False
        self.owner = None       

        #--TODO-- planetary population needs to be here.
        self.orbitalStarbase = None     # Starbase object

        self.factories = 0
        self.mines = 0
        self.defenseValue = 0





    def changeHab(self):
        pass

    def changeConc(self, concIron, concBor, concGerm):
        #set concentrations to new values, perhaps best to let the mines\mining fleets decide how much and have them set the values?
        self.concIron = concIron
        self.concBor = concBor
        self.concGerm = concGerm


    def addSurfaceMinerals(self, minerals):
        self.surfaceIron += minerals[0]
        self.surfaceBor += minerals[1]
        self.surfaceGerm += minerals[2]

    def removeSurfaceMinerals(self, minerals):
        """
        Removes the specified number of minerals from currSurfaceMinerals

        precondition: minerals exist on the surface, the amount specified will 
                    not cause the surface minerals to go negative.
                    assumes minerals is a valid amount to be removed 

        input: [minerals]
        output: self.surfaceminerals is updated


        """
        self.surfaceIron -= minerals[0]
        self.surfaceBor -= minerals[1]
        self.surfaceGerm -= minerals[2]

    def getSurfaceMinerals(self):      
        return [self.surfaceIron, self.surfaceBor, self.surfaceGerm]

class Colony(object):
    """ 
    Requires 
        >   A player object. Every player.colonies = {} holding colony objects. 
            
        >   a planet object >>> or object that mimics required attributes



    """

    def __init__(self, player, planet, population):
        # self.player = player    #link to owner
        self.planet = planet    # *** connects a colony to a planet object ****
        

        self.scanner = False
        self.orbital = False
        self.productionQ = ProductionQ(self, player)   # this would be good to have as a seperate object for AR races and (future) none-planet starbase production

        self.population = population # population needs to be part of planet
        self.defenses = 0

        #calculated values
        #! this is race figure and then the true growth rate is calculate in populationGrowth function, taking into account hab\capacity?
        self.growthRate = player.raceData.growthRate  # set when colony is instantiated 

        self.mineProduce = player.raceData.mineProduce
        self.mineOperate = player.raceData.mineOperate
         
        self.factoryProduce = player.raceData.factoryProduce   # 10 factories produce n resources a year
        self.factorOperate  = player.raceData.factoryOperate
        self.totalResources = 0     # used indirectly
        self.resourceTax = False        # DEPRECIATE - should be handled in productionQ  
        self.planetValue = 100    # 100 = 100% Value = calculated from currHab 
        self.planetMaxPopulation = 1000000  # based on PlanetValue & PRT # HE is .5; JOAT is 1.20
        #self.raceData = raceData

    def calcTotalResources(self, popEfficiency):
        """Pop <= maxPop, everyone works at 100%,
           Pop between 100% and 300% of maxPop work at 50%, 
           Pop above 300% enjoy a life of leisure and don't work
        """
        #popEfficiency = self.raceData.popEfficiency
        
        self.totalResources = 0  # set to zero for recalculation
        partiallyEmployed = 0



        # ------------------- overpopulation calculations -------------- 
        if self.population > self.planetMaxPopulation:

            # find the 300% of population cap
            employedMax = 3 * self.planetMaxPopulation  
            
            # cap employment at 300% of planetMaxPopulation
            if self.population > employedMax:
                partiallyEmployed = employedMax - self.planetMaxPopulation  # the 100% - 300%
            
            # if under 300% 
            else:
                partiallyEmployed = self.population - self.planetMaxPopulation


            #obtain resources from partially employed
            self.totalResources += int(partiallyEmployed / (popEfficiency / 2.))
            if DEBUG_2: print("Colony.calcTotalResources - employedMax:%d  partiallyEmployed: %d included in totalResources:%d" %(employedMax, partiallyEmployed, self.totalResources))
        

        # ------------------- normal population calculations -------------- 
        self.totalResources += int(self.population / popEfficiency)
        if DEBUG_2: print("Colony.calcTotalResources - population: %d efficiency: %d  with calculated totalResources:%d" %(self.population, popEfficiency, self.totalResources))


        # ------------------- factory calculations -------------- 
        TEN = 10 # factoryProduce is based on TEN factories producing factoryProduce resources.
        self.totalResources += int( (self.operatingFactories() / TEN) * self.factoryProduce)


        if DEBUG_2: print("Colony.calcTotalResources - factories: %d efficiency: %d  with (pop + factory) totalResources:%d" %(self.planet.factories, self.factoryProduce, self.totalResources))




    def operatingFactories(self):
        '''
        Input: 
        returns the number of factories that can be run

        '''
        #--TODO-- calculate and use the maximum available factories (due to hab & race settings, e.g. a -f popdrop a developed HP colony won't be able to use them all
        return  min(int(self.population / self.factorOperate), self.planet.factories)
        

    def operateMines(self):
        ''' Extract minerals from planet and turn into surface minerals
                minerals should deplete in a seperate method
        '''
        pass

    def populationGrowth(self):
        ''' Population Growth is a function of Planet Value, GrowthRate, and 
        Population. 
        http://wiki.starsautohost.org/wiki/Guts_of_population_growth
        
        under 25%: popgrowth = population * growthrate * habvalue
        over 25%:  as above, then multiply by crowdingfactor = 16/9 * (1-cap%)^2.

        '''
        pop = self.population
        growth = self.growthRate
        hab = self.planetValue / 100
        popgrowth = 0

        capacity = (self.population * 1.0) / self.planetMaxPopulation # 1.0 = ensure float

        if hab < 0:
            popgrowth = pop * hab / 10. 
        else:
            if capacity > 1.0:
                # --TODO--- negative growth
            
                return  
        
            else:
                popgrowth = pop * growth * hab

                if (capacity > .25):
                    popgrowth = popgrowth * 16.0/9
                    popgrowth = popgrowth * (1.0 - capacity) * (1.0 - capacity)


        self.population += popgrowth
        print("(planet.Colony): %s had %d population growth. Total Population: %d" % (self.planet.name, popgrowth, self.population))
            


    # unecessary function.
    # def calcGrowthRate(self, raceRate):
    #     '''
    #     Input:  raceRate is from owning Player object.
    #             self.planetValue must be present and updated
                
    #     Output: the method should update the rate at which the colonist grow.
    #             This value is based on planet value. 
    #     (Currently set to the max race rate.)
    #     '''
    #     self.growthRate = raceRate

    def colonyUninhabit(self):
        # self.planet.owner = None
        # damage to infrastructure?
        # self.resources = 0
        # self.population = 0
        # self.scanner = False
        # self.orbital = False
        # self.prodQ = False

        pass


    def maxMinesOnColony(self):
        """
        Maximum possible mines that race can build on a Colony.
        based on the maximum number of population that can fit at a given PlanetValue 


        --TODO-- handle JOAT (120%) HE(50%) PRTs There should be a minimum and max threshold
        """
        ONE_HUNDRED = 100   # base value for planetValue ratio
        TEN_THOUSAND = 10000
        maxPopulation = 1000000     # --TODO-- change based on PRT



        # update planetValue

        if self.planetValue < 0:
            return 50
        
        else:
            maxSupportedPopulation = (self.planetValue / ONE_HUNDRED) * maxPopulation
            maxMines = int((maxSupportedPopulation / TEN_THOUSAND) * self.mineOperate)
            print("Colony.maxMinesOnColony: maxMines:%d " % maxMines)
            
            return maxMines





    def maxUsableMinesOnColony(self):
        """
        of the mines on the planet, how many can be used?
        This is a function of the planetValue and population
        """
        # what is the max population of the planet
        ## 
        maxMines = int((self.population / TEN_THOUSAND) * self.mineOperate)
        planetMines = self.planet.mines
        mineCeiling = self.maxMinesOnColony()

        # compare max mines that the current population can support VS 
        # number of mines built
        compareList = [maxMines, planetMines] 
        lowValue = min(compareList) # the lowest value is the one that is usable


        if self.planetValue < 0:
            print("Colony.maxUsableMinesOnColony: HARDCODED Needs updated, assumes 50 mines base")
            
            if lowValue > 50:
                return 50    
            else:
                return lowValue 
        
        else:
            
            print("Colony.maxUsableMinesOnColony: lowest value between what the population could operate and what was built: " % lowValue)
            
            return lowValue

    def processProductionQ(self):
        self.productionQ.productionController()

