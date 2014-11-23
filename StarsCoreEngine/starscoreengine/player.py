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
from .planet import Colony, Planet


'''
    Player Data

    players race file starts as <'race_name'.r1>
    > this establishes the basic race information that is generated by the RaceWizard
    RaceWizard data needs to be saved and referenced. 

    PRT Summary:
    >PRT ==> changes how species operate in some manner. typically acts as an augmentation
    >>> WM = extra hulls + tech, better invasion, better ship speed etc, invasion benefit
    >>> SS = base stealth, extra hulls, extra tech, capture percent of research resources
    >>> JOAT = base pop higher, scout hulls have intrinsic pen scanners
    >>> IT = extra tech, jump cargo and pop through gates, better at gating, 2nd planets
    >>> PP = extra tech, extra planet, diff pack behavior
    >>> SD = extra hulls, extra tech, diff minefild behavior,
    >>> HE = extra hulls, extra engine, double growthrate, half pop capacity
    >>> IS = extra tech, invasion benefit
    >>> AR = special housing, extra hulls, different behavior


    >LRT ==> chages how a species operate in a smaller manner
    >>> UR = ultimate recycling
    >>> IFE = Access two unique engines? no ramscoops
    >>> Double Shields = 
    >>> no pen scanners
    >>> 



    > Player object should track
    >> race file data
    >> habitable planets (list?)
    >> (list?) of fleets object ids 
    >> minefild list?
    >> tech levels
    >> ship designs
    >> player VC data
    >>

'''

'''
    New Game  & New player
    > player race file name is added to the Custom File.
    > one name for each list.
    > name of file must match race name for new game setup

'''


class Player(object):
    """
    Contains player related data that is not space objects.

    Case for multiple inheritance:
    > inherits a set of behaviors that changes based on the PRT

    """

    def __init__(self, raceData):
        self.raceName = raceData.raceName
        self.raceNamePlural = raceData.raceName

        self.PRT = raceData.PRT     # apply PRT values after player variables set,
        self.LRT = raceData.LRT   # apply LRT values after player is updated with PRT variables

        self.growthRate = raceData.growthRate
        self.popEfficiency = raceData.popEfficiency

        self.habGravityCenter = raceData.habGravityCenter  # (centerpoint, Click width)?  
        self.habGravRange = raceData.habGravRange  # pos range from Center. Total range doubled  
        
        self.habTempCenter = raceData.habTempCenter
        self.habTempRange = raceData.habTempRange

        self.habRadCenter = raceData.habRadCenter
        self.habRadRange = raceData.habRadRange

        self.factoryProduce = raceData.factoryProduce   # 10 factories produce n resources a year
        self.factoryOperate = raceData.factoryOperate   # 10,000 colonist operate n factories       
        self.mineProduce = raceData.mineProduce     # 10 mines produce n kt of each mineral a year
        self.mineOperate = raceData.mineOperate       #  10,000 colonist operate n mines

        self.factoryCost = raceData.factoryCost      # a factory cost n resources to build
        self.factoryGermCost = raceData.factoryGermCost # True = cost 1kt less of Germanium to build
        self.mineCost = raceData.mineCost         # a mine costs n resources to build



        # Research costs = (75% extra, standard amount, 50% less)
        self.techCostEner = raceData.techCostEner 
        self.techCostWeap = raceData.techCostWeap
        self.techCostProp = raceData.techCostProp
        self.techCostCon = raceData.techCostCon 
        self.techCostElec = raceData.techCostElec
        self.techCostBio = raceData.techCostBio
        
        self.techJumpStart = raceData.techJumpStart # True = All 'Costs 75% extra' fields start at Tech 4


        #self.homeUniverse = None
        #self.race = raceData #RaceData()
        self.colonies = {}  # colony objects
        self.tech = {}  # tech object
        self.shipDesign = {} # ship design objects
        self.battleOrders = {} 
        self.production = {} 
        self.turnOrders = {}
        self.diplomacy = {} # diplomacy object?
        self.intel = {} 


    def colonyMining(self):
        pass

    def colonyResources(self):
        pass

    def colonizePlanet(self, planet, pop, fleetMinerals = (25,20,30)):
        '''
        input:  planet = planet object; 
                pop = colonists - typically cargo of colony ship
                fleetMinerals = colony fleet object that has been salvaged

        '''
        newColony = Colony(planet, pop)
        planet.updateSurfaceMinerals(fleetMinerals)
        newColony.planetValue = self.planetValue(planet)
        newColony.calcGrowthRate(self.growthRate)
        planet.owner = self.raceName

        self.colonies[planet.ID] = newColony
        


    def planetValue(self, planet):
        '''Calculates planet value for player based on Race Data. 

            if a colony = updates colony values
            if not a colony, updates intel values

        '''
        planetValue = 1.0

        return planetValue




class RaceData(object):
    """
    Contains data from RaceWizard.
    """
    def __init__(self, raceName):
        self.raceName = raceName
        self.raceNamePlural = raceName
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

        immune = None value for centerpoint

        '''
        self.habGravityCenter = 1  # (centerpoint, Click width)?  
        self.habGravRange = 15.0  # pos range from Center. Total range doubled  
        
        self.habTempCenter = 70
        self.habTempRange = 25.0

        self.habRadCenter = 50
        self.habRadRange = 15.0


        self.factoryProduce = 10    # 10 factories produce n resources a year
        self.factoryCost = 10       # a factory cost n resources to build
        self.factoryOperate = 10    # 10,000 colonist operate n factories       
        self.factoryGermCost = False # True = cost 1kt less of Germanium to build

        self.mineProduce = 10       # 10 mines produce n kt of each mineral a year
        self.mineCost = 10          # a mine costs n resources to build
        self.mineOperate = 10       #  10,000 colonist operate n mines
        
        # Research costs = (75% extra, standard amount, 50% less)
        self.techCostEner = 1 
        self.techCostWeap = 1 
        self.techCostProp = 1 
        self.techCostCon = 1 
        self.techCostElec = 1 
        self.techCostBio = 1 
        
        self.techJumpStart = False # True = All 'Costs 75% extra' fields start at Tech 4



