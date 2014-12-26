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

from .space_objects import SpaceObjects
import random


class Planet(SpaceObjects):
    """ 
        Planet is the template that provides all the data available for a planet. 
        origHab = Tuple  --TODO-- change to individual variables
        origConc = Tuple --TODO-- change to individual variables

    """
    def __init__(self, xy, ID, name, origHab = (90, 1.1, 65), origConc = None):
        super(Planet, self).__init__(xy, ID)
        self.name = name    
        self.origHab = origHab              #depreciate
        self.origTemp = origHab[0]
        self.origGrav = origHab[1]
        self.origRad = origHab[2]

        self.currHab = self.origHab         # depreciate
        self.currentTemp = self.origTemp
        self.currentGrav = self.origGrav
        self.currentRad = self.origRad

        #detail current Concentration, random by default
        if not origConc: 
            self.concIron = random.randint(1,100)
            self.concBora = random.randint(1,100)
            self.concGerm = random.randint(1,100)
        else:
            self.concIron = origConc[0]
            self.concBora = origConc[1]
            self.concGerm = origConc[2]
        


        self.currSurfaceMinerals = 0  # depreciate  (should be  3 values in a list)
        self.surfaceIron = 0
        self.surfaceBora = 0
        self.surfaceGerm = 0


        self.HW = False
        self.owner = None       

        self.factories = 0
        self.mines = 0
        self.defenseValue = 0



    def changeHab(self):
        pass

    def changeConc(self, concIron, concBora, concGerm):
        #set concentrations to new values, perhaps best to let the mines\mining fleets decide how much and have them set the values?
        self.concIron = concIron
        self.concBora = concBora
        self.concGerm = concGerm


    def updateSurfaceMinerals(self, minerals):
        self.surfaceIron += minerals[0]
        self.surfaceBora += minerals[1]
        self.surfaceGerm += minerals[2]


class Colony(object):
    """ 
    Requires 
        >   A player object. Every player.colonies = {} holding colony objects. 
            
        >   a planet object >>> or object that mimics required attributes



    """

    def __init__(self, planet, population):
        # self.player = player    #link to owner
        self.planet = planet    # *** connects a colony to a planet object ****
        

        self.scanner = False
        self.orbital = False
        self.prodQ = False   # this would be good to have as a seperate object for AR races and (future) none-planet starbase production

        self.population = population
        self.defenses = 0

        #calculated values
        #! this is race figure and then the true growth rate is calculate in populationGrowth function, taking into account hab\capacity?
        self.growthRate = .10  # calc on colonizing; recalc on any terriform event ! 
        self.totalResources = 0
        self.resourceTax = False  
        self.planetValue = 1.0    # 1.0 = 100% Value = calculated from currHab 
        self.planetMaxPopulation = 1000000  # based on PlanetValue & PRT # HE is .5; JOAT is 1.20


    def calcTotalResources(self, popEfficiency):

        # -- TODO -- include operating factory resources
        self.totalResources = self.population / popEfficiency


    def operatingFactories(self):
        '''
        Input: 
        returns the number of factories that can be run

        '''
        pass

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
        hab = self.planetValue

        capacity = (self.population * 1.0) / self.planetMaxPopulation # 1.0 = ensure float

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
            



    def calcGrowthRate(self, raceRate):
        '''
        Input:  raceRate is from owning Player object.
                self.planetValue must be present and updated
                
        Output: the method should update the rate at which the colonist grow.
                This value is based on planet value. 
        (Currently set to the max race rate.)
        '''
        self.growthRate = raceRate

    def colonyUninhabit(self):
        # self.planet.owner = None
        # damage to infrastructure?
        # self.resources = 0
        # self.population = 0
        # self.scanner = False
        # self.orbital = False
        # self.prodQ = False

        pass



