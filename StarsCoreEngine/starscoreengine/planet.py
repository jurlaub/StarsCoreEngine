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
import random


class Planet(SpaceObjects):
    """ 
        Planet is the template that provides all the data available for a planet. 


    """
    def __init__(self, xy, ID, name, origHab = (1.1, 90, 45), origConc = None):
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


    def updateSurfaceMinerals(self, minerals):
        self.surfaceIron += minerals[0]
        self.surfaceBor += minerals[1]
        self.surfaceGerm += minerals[2]


class Colony(object):
    """ 
    Requires 
        >   A player object. Every player.colonies = {} holding colony objects. 
            
        >   a planet object >>> or object that mimics required attributes



    """

    def __init__(self, raceData, planet, population):
        # self.player = player    #link to owner
        self.planet = planet    # *** connects a colony to a planet object ****
        

        self.scanner = False
        self.orbital = False
        self.productionQ = False   # this would be good to have as a seperate object for AR races and (future) none-planet starbase production

        self.population = population
        self.defenses = 0

        #calculated values
        #! this is race figure and then the true growth rate is calculate in populationGrowth function, taking into account hab\capacity?
        self.growthRate = raceData.growthRate  # set when colony is instantiated 

        self.mineProduce = raceData.mineProduce
        self.mineOperate = raceData.mineOperate
         
        self.factoryProduce = raceData.factoryProduce
        self.factorOperate  = raceData.factoryOperate
        self.totalResources = 0
        self.resourceTax = False  
        self.planetValue = 100    # 100 = 100% Value = calculated from currHab 
        self.planetMaxPopulation = 1000000  # based on PlanetValue & PRT # HE is .5; JOAT is 1.20

    def calcTotalResources(self, popEfficiency):
        """Pop <= maxPop, everyone works at 100%,
           Pop between 100% and 300% of maxPop work at 50%, 
           Pop above 300% enjoy a life of leisure and don't work
        """
        if self.population <= self.planetMaxPopulation:
            self.totalResources = self.population / popEfficiency
        elif self.population <= 3 * self.planetMaxPopulation:
            self.totalResources = self.planetMaxPopulation / popEfficiency
            self.totalResources += (self.population - self.planetMaxPopulation) / (popEfficiency / 2.)
        else:
            self.totalResources = self.planetMaxPopulation * 2 / popEfficiency

        self.totalResources += self.operatingFactories() * self.factoryProduce

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



