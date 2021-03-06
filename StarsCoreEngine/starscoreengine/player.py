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

from math import sqrt

from .planet import Planet
from .colony import Colony
from .research import Research
from .player_designs import PlayerDesigns
from .productionQ import ProductionQ
from .player_build_list import PlayerBuildList
from .fleet_command import FleetCommand
# from .game_utility import findMaxTechnologyComponent

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

    def __init__(self, speciesData, playerNumber, multiverse, techTree = {}):
        self.multiverse = multiverse
        self.speciesName = speciesData.speciesName
        self.speciesNamePlural = speciesData.speciesName
        self.playerNumber = playerNumber     # for accessing and saving x file
        self.xfilestatus = []     # list of 'error' strings

        self.PRT = speciesData.PRT     # apply PRT values after player variables set,
        self.LRT = speciesData.LRT   # apply LRT values after player is updated with PRT variables
        

        self.speciesData = speciesData    


   
        self.colonies = {}  # colony objects

        # --TODO--- add technology 'research' costs (cheap, normal, expensive) to Research
        self.research = Research(self.PRT, self.LRT)  # tech object
        self.techTree = techTree
        self.designs = PlayerDesigns(self.speciesName, self.research.techLevels, self.LRT) # ship design objects
        self.historicalShipDesign = {}  #? 
        
        self.fleetCommand = FleetCommand(self, self.multiverse)

        self.battleOrders = {} 
        self.buildListObject = PlayerBuildList(self)

        # self.playerSpecificBuildCosts = {}  # include: terriforming, factory, defenses etc
        # self.speciesData.

        """ turnOrders:
        when created    - should be sequentially numbered
                        - should be classifiable (where possible - should be possible in all cases)
        When imported:  - grouped by OrderOfEvents 
                        - within each event, the player order will be maintained
                        - for example: (player research)
                        -- the player may change intentions regarding player research multiple times
                        -- 1st - currentResearch = 'weapons'; currentResearchTax = .15 %
                        -- 2nd - currentResearch = 'energy'; currentResearchTax = .50 %
                        -- 3rd - currentResearch = 'construction'; currentResearchTax = .35 %
                        each order would be processed. (this may be reconsidered)
                        Some orders may have only one state. Some orders may have multiple states
                        One state orders could maintain only 1 set of orders (like research)

                        what else fits in this category? Waypoint 0 orders? 
                        The tricky one seems to be splitting and merging fleets.


        """

        self.turnOrders = {}


        self.diplomacy = {} # diplomacy object?
        self.intel = {} 



    def ISFleetGrowth(self):

        if self.PRT is not 'IS':
            return

        # for fltID, flt in self.fleets.items():

        """
        # iterate throught fleets. If they have cargo of population, popGrowth.
        If they over grow cargoCapacity, check if they are around a planet, if so,
        offload (invasion?) If not, fill up to capacity.


        """
        pass

    def colonyMining(self):
        pass

    def colonyResources(self):
        pass

    def colonizePlanet(self, planet, pop, fleetMinerals = (25,20,30)):
        '''
        input:  planet = planet object; 
                pop = colonists - typically cargo of colony ship
                fleetMinerals = colony fleet object that has been salvaged from the ship hulls.

        precondition: all minerals in colony fleet cargo has been offloaded to the planet

        '''
        newColony = Colony(self, planet, pop)
        planet.addSurfaceMinerals(fleetMinerals)

        newColony.planetValue = self.planetValue(planet)
        #newColony.growthRate = self.speciesData.growthRate

        planet.owner = self.speciesName

        # productionQ = ProductionQ(newColony, self)
        # newColony.productionQ = productionQ

        self.colonies[planet.ID] = newColony
        

    def updateColonyValues(self):
        ''' updateColonyValues called from OrderOfEvents 
        to update colony values before population growth

        uses planetValue()

        '''
        for each, colony in self.colonies.items():              

            value = self.planetValue(colony.planet)

            colony.planetValue = value


    def planetValue(self, planet):
        '''Calculates planet value for player based on Race Data. 

        >used for each colony before OrderOfEvents.population (growth)
        >>> called from Player.updateColonyValues()

        >used when calculating intel on planets


        input:  self.hab values 
                planet hab values

        output: planet value for player (used for colony and planet assessments)

        from m.a@stars
        http://starsautohost.org/sahforum2/index.php?t=msg&th=2299&rid=625&S=ee625fe2bec617564d7c694e9c5379c5&pl_view=&start=0#msg_19643
        http://starsautohost.org/sahforum2/index.php?t=msg&th=2271&start=0&rid=0

        @ju -> check "calculateHabValues2" 

        Origional code written by m.a@stars, just converted to python
        #define BYTE char
        #define WORD short

        #define IMMUNE(a) ((a)==-1)
        
        //simplified for this. Initialized somewhere else
        struct playerDataStruct 
        {
            BYTE lowerHab[3];	 // from 0 to 100 "clicks", -1 for immunity
            BYTE upperHab[3];
        } player;

        //in: an array of 3 bytes from 0 to 100
        //out: a signed integer between -45 and 100
        //hey, it was the Jeffs idea! Smile
        signed long planetValueCalc(BYTE* planetHabData)
        {
            signed long planetValuePoints=0,redValue=0,ideality=10000;	//in fact, they are never < 0
            WORD planetHab,habUpper,habLower,habCenter;
            WORD Excentr,habRadius,margin,Negativ,dist2Center;
        
            for (WORD i=0; i<3; i++) {
                habUpper = player.upperHab[i];
                if (IMMUNE(habUpper)) {			//perfect hab
                    planetValuePoints += 10000;
                }
                else {	//the messy part
                    habLower  = player.lowerHab[i];
                    habCenter = (habUpper+habLower)/2;	//no need to precalc
                    planetHab = planetHabData[i];
        
                    /*
                    note: this version makes the basic assumption that habitability is
                    symmetrical around the center, that is, the ideal center is located
                    in the middle of the lower and upper boundaries, and both halves
                    have the same value. The original algorithm seems able to cope with
                    weirder definitions, i.e: bottom is 20, top is 80, center is 65,
                    and hab value stretches proportionally to the different length of
                    both "halves"...
                    */
                    
                    dist2Center = abs(planetHab-habCenter);
                    habRadius = habCenter-habLower;
        
                    if (dist2Center<=habRadius) {		/* green planet */
              	        Excentr = 100*dist2Center/habRadius;	//note: implicit conversion to integer
            	        Excentr = 100 - Excentr;		//kind of reverse excentricity
            	        planetValuePoints += Excentr*Excentr;
                  	    
                        margin = dist2Center*2 - habRadius;
            	        if (margin>0) {		//hab in the "external quarters". dist2Center > 0.5*habRadius
                            ideality *= (double)(3/2 - dist2Center/habRadius);	//decrease ideality up to ~50%
            	            /*
                            ideality *= habRadius*2 - margin;	//better suited for integer math
                            ideality /= habRadius*2;
            	            */
            	        }
                    } else {					/* red planet */
            	        Negativ = dist2Center-habRadius;
            	        if (Negativ>15) Negativ=15;
            	        redValue += Negativ;
                    }
                }
            }
        
        if (redValue!=0) return -redValue;
        planetValuePoints = sqrt((double)planetValuePoints/3)+0.9;	//rounding a la Jeffs
        planetValuePoints = planetValuePoints * ideality/10000;	//note: implicit conversion to integer
        
        return planetValuePoints;		//Thanks ConstB for starting this
        '''
        rdat = self.speciesData

        # NOTE: May need to adjust to be Upper and Lower bounds because of 'odd' 
        # low gravity click spaces 
        gc = rdat.habGravityCenter 
        gr = rdat.habGravRadius     
        
        tc = rdat.habTempCenter 
        tr = rdat.habTempRadius

        rc = rdat.habRadCenter 
        rr = rdat.habRadRadius

        hab = ((gc, gr, planet.currentGrav), (tc, tr, planet.currentTemp), (rc, rr, planet.currentRad))
        
        ideality = 10000
        planetValuePoints = 0
        redValue = 0

        for i in hab:
            radius = i[1]
            center = i[0]

            planetHab = i[2]
            habUpper = center + radius
            habLower =  center - radius
            #print("habUpper: %f; habLower: %f" % (habUpper, habLower))

            if radius == -1:      
                planetValuePoints += 10000
            else:
                
                dist2Center = abs(planetHab - center)  
                #print("dist2Center:%f = abs ( planetHab:%f - center:%f" % (dist2Center,planetHab,  center))

                if dist2Center <= radius:       

                    Excentr = 100*dist2Center//radius
                    Excentr = 100 - Excentr
                    planetValuePoints += Excentr*Excentr

                    margin = dist2Center*2 - radius
                    #print("margin:%f" % margin)
                    if margin > 0:
                        ideality *= (3/2 - dist2Center//radius)
                        #print("ideality1:%f" %ideality)
                else:
                    neg = dist2Center-radius
                    if neg > 15:
                        neg = 15
                    redValue += neg


        if redValue != 0:
            return -redValue

        #print("planetValuePoints: %f" % planetValuePoints)
        planetValuePoints = sqrt(planetValuePoints/3.0) + 0.9
        #print("planetValuePoints2: %f" % planetValuePoints)
        planetValuePoints = planetValuePoints * ideality//10000
        #print("planetValuePoints3: %f" % planetValuePoints)


        #planetValue = 1.0

        return planetValuePoints
            

    # def buildCosts_PlanetScannerDefenses(self):
        
    #     s = "PlanetaryScanner"
    #     d = "PlanetaryDefenses"
    #     currTechLevels = self.research.techLevels

    #     sName = findMaxTechnologyComponent(s, currTechLevels, self.techTree)
    #     sObj = self.techTree[sName]
    #     sCosts = [sObj["iron"], sObj["bor"], sObj["germ"], sObj["resources"]]


    #     dName = findMaxTechnologyComponent(d, currTechLevels, self.techTree)
    #     dObj = self.techTree[dName]
    #     dCosts = [dObj["iron"], dObj["bor"], dObj["germ"], dObj["resources"]]

    #     d : {"itemType": d, "targetItemsCost": dCosts}



    #     return {sName :{"itemType": s, "targetItemsCost":sCosts }, \
    #             dName : {"itemType": d, "targetItemsCost":dCosts }}


