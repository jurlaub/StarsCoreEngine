"""
    This file is part of Stars Core Engine, which provides an interface and 
    processing of Game data. 

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

    Contributors to this project agree to abide by the interpretation expressed 
    in the COPYING.Interpretation document.

"""

'''
base tech

HE - none
SS - elec  5
WM - energy 1, weapons 6, prop 1
CA - energy 1, weapons 1, prop 1, con 2, bio 6
IS - none
SD - prop 2, bio 2
PP - energy 4
IT - prop 5, con 5
AR - ener 1
JOAT - 3 in all

IFE - prop +1
CE - prop +1

expensive start at 4 cost :60#JOATA
expensive start at 3 cost :60#none JOAT

1 tech exp -    -49
2 tech exp -    -109
3 tech exp -    -179
4 tech exp -    -259
5 tech exp -    -349
6 tech exp -    -459
1 tech cheap -  43
2 tech cheap -  173
3 tech cheap -  390
4 tech cheap -  693
5 tech cheap -  910
6 tech cheap -  1083

1, 1           0
2, 2           0
3, 3           0


cost - base cost following fibonacci sequence + 10 res per tech level)

cost_research(normal)
50, 80, 130 (base)
50, 90, 150 (true, inc +10)

cost_(expensive)
88, 140
88, 157
'''

"""
research:
> players have a current tech levels
> players spend resources on tech to increase level
> players can gain tech levels by non-research means (invasion, 
    battle, MT encounter)

> player research settings:
    > can indicate the next category to research
    > can indicate the 'research tax' to take from planetary resources

> research levels govern (limit) the type of components that can be used to 
    design a ship 
    > players can only build their own designs
    > players can operate other (higher tech) ships/designs
> research levels limit the type of planetary installations that can be built




"""

DEBUG = False

class Research(object):
    """ Research

    Works in cooperation with ProductionQ, Player.colonies, and OrderOfEvents.
    During the production event, the ProductionQ's and planetary resources are 
    checked. If the planet provides resources, then those resources are pooled 
    with the other colonies accross the empire. (the remaining resources are used
    for production.) After all the colonies are checked, the research resources 
    are applied to the remaining cost for the current research. If any are left
    over, (the new research value is calculated?) and the remaining resources 
    are applied to the nextToResearch technology level.

    """
    
    # this collects all races research for the year. Its to calculate the SS spy bonus
    # must be zeroed out each year.
    yearsResearch = {"energy" : {"speciesResearchingField" : 0, "resourcesSpent" : 0}, 
              "weapons" : {"speciesResearchingField" : 0, "resourcesSpent" : 0},
              "propulsion" : {"speciesResearchingField" : 0, "resourcesSpent" : 0},
              "construction" : {"speciesResearchingField" : 0, "resourcesSpent" : 0},
              "electronics" : {"speciesResearchingField" : 0, "resourcesSpent" : 0},
              "biotechnology" : {"speciesResearchingField" : 0, "resourcesSpent" : 0}
          }
    
    # class variable used for tech research reference
    #"energy": 0; "weapons":1; "propulsion":2; "construction":3; "electronics":4; "biotechnology":5;
    techResearch = ("energy", "weapons", "propulsion", "construction", 
                    "electronics","biotechnology")

    researchCost =  ("normal", "cheap", "expensive")



    def __init__(self, PRT, LRTs = [], speciesData = [], tech4 = False):   # modify speciesData to be a dictionary?
        
        self.techLevels = {"energy" : 0, 
                  "weapons" : 0,
                  "propulsion" : 0,
                  "construction" : 0,
                  "electronics" : 0,
                  "biotechnology" : 0
              }

        # tracks the amount spent per level, MUST RESET when level is reached
        self.alreadySpent = {"energy" : 0, 
                  "weapons" : 0,
                  "propulsion" : 0,
                  "construction" : 0,
                  "electronics" : 0,
                  "biotechnology" : 0
              }

        self.currentResearch = Research.techResearch[3] 
        self.nextToResearch = Research.techResearch[4]
        self.currentResourcesSpent = 0
        self.nextResourcesSpent = 0
        self.yearlyResearchResources = 0     # Collected by player changes each year
        self.totalResources = 0     # Collected by player changes each year
        self.researchTax = .1  # a percentage of total resources


        # technology costs from Player speciesData
        # use Research class variable for cost assessment
        self.techCostEner = Research.researchCost[1]  # speciesData[0] -> or something else from speciesData
        self.techCostWeap = 1 
        self.techCostProp = 1 
        self.techCostCon = 1 
        self.techCostElec = 1 
        self.techCostBio = 1 
        self.startAtTech4 = tech4


        # sets the starting tech levels according to the race PRT and LRT's
        self.techLevels = Research.set_base_tech(self.techLevels, PRT, LRTs)

        if tech4:
            # if a techLevel expensive bump starting level to tech4?
            pass


    # for SS PRT update total spent on resources -> if levels attained follow process outlined in spendResearchTax
    def globalResearchSpying(self):
        pass


    # def to spend total research on approapriate technology level
    def spendResearchTax(self):
        """
        input: 
            self.yearlyResearchResources
            self.currentResearch
            self.nextToResearch

        output: 
            calculates amount left to spend on level. 
            researches level
            if reached, update level, zero out alreadySpent, add value to 
                    yearsResearched class variable, update other variables
            repeat if resources left over (multiple levels may be attained this way)



        """
        pass

    # def to 'collect' planetary research tax and return remainder 
    def colonyResourcesAfterTax(self, colony):
        """
        input: colony object with .totalResources amount

        output: 
            >   returns to colony (or ProductionQ) the portion not used for 
                research according to self.researchTax
            >   updates Research.totalResources with the researched tax amount


        """
        researchTax = int(self.researchTax * colony.totalResources)
        self.yearlyResearchResources += researchTax
        remainingResources = colony.totalResources - researchTax 

        if DEBUG: print("colonyResourcesAfterTax: colonyResources: %s  researchTax:%s  usableResources:%s " % (colony.totalResources, researchTax, remainingResources))


        return remainingResources


    def yearsResearch_add(self):
        """ Add total research resources spent on a tech level for a player"""
        pass

    #@staticmethod
    def yearsResearch_zero(self):
        """ set shared class variable Research.yearsResearch to 0.
        After all SS races in game have used research bonus class data 
        """

        for techKey, techObj in self.yearsResearch.items():
            for i, o in techObj.items():
                o = 0 



    @staticmethod
    def set_base_tech(startLevels, PRT, LRTs=[]):
        """Returns the starting tech levels for a race design based on its PTR and a list of LRTs.
        Expects a string as PTR ('JOAT' etc) and a list of strings for LRTs (['IFE', 'CE'] etc)
        """
        # startLevels = {"energy" : 0, 
        #           "weapons" : 0,
        #           "propulsion" : 0,
        #           "construction" : 0,
        #           "electronics" : 0,
        #           "biotechnology" : 0
        #       }
        if PRT in ("HE", "IS"):
            pass #start at 0 in all fields
        elif PRT == "SS":
            startLevels["electronics"] += 5
        elif PRT == "WM":
            startLevels["energy"] += 1
            startLevels["weapons"] += 6
            startLevels["propulsion"] += 1
        elif PRT == "CA":
            startLevels["energy"] += 1
            startLevels["weapons"] += 1
            startLevels["propulsion"] += 1 
            startLevels["construction"] += 2
            startLevels["biotechnology"] += 6 
        elif PRT == "SD":
            startLevels["propulsion"] += 2 
            startLevels["biotechnology"] += 2 
        elif PRT == "PP":
            startLevels["energy"] += 4
        elif PRT == "IT":
            startLevels["propulsion"] += 5
            startLevels["construction"] += 5 
        elif PRT == "AR":
            startLevels["energy"] += 1
        elif PRT == "JOAT":
            for k in startLevels.keys():
                startLevels[k] += 3
        else:
            raise ValueError("PRT not recognised, what is {}?".format(PRT))
        #print ("LRTs are")
        #print (LRTs)
        #print (i for i in LRTs)
        for LRT in LRTs:
            if LRT in ("IFE", "CE"):
                startLevels["propulsion"] += 1
        return startLevels
    



def species_editor_tech_costs(numExpensive, numCheap, boxTicked):
    """Returns the cost in points from the number of expensive and cheap fields chosen,
    and whether the 'start expensive fields at level 3/4' box is ticked.
    """ 
    _diff = numExpensive - numCheap
    cost = 0
    if _diff == 0:    cost = 0    
    elif _diff == 1:  cost = -49  #-49
    elif _diff == 2:  cost = -109 #-60
    elif _diff == 3:  cost = -179 #-70
    elif _diff == 4:  cost = -259 #-80
    elif _diff == 5:  cost = -349 #-90
    elif _diff == 6:  cost = -459 #-110
    elif _diff == -1: cost = 43   #43
    elif _diff == -2: cost = 173  #130
    elif _diff == -3: cost = 390  #217
    elif _diff == -4: cost = 693  #303
    elif _diff == -5: cost = 910  #217
    elif _diff == -6: cost = 1083 #173
    if boxTicked:
        cost -= 60
    return cost



    

def cost_remaining(level, cost, totalLevels, alreadySpent):
    """Calculates the cost remaining for this tech level. 
    Level = integer level number, 1 - 26
    multiplier = normal, cheap, expensive
    totalLevels = total number of levels researched
    alreadySpent = resources already spent towards this level

    Normal research cost calculated using fibonacci sequence from 30, 50, ... plus 10 per level of research. 
    Increase by 75% for expensive tech, reduce by 50% for cheap (including the increase per level of research)
    """
    def fib(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fib(n-1) + fib(n-2)
    #e.g. level 1 = 50 = fib(5) * 10
    _mult = 0.
    if cost == "normal":
        _mult = 1.
    elif cost == "cheap":
        _mult = 0.5
    elif cost == "expensive":
        _mult = 1.75
    else:
        raise ValueError("cost must be one of normal, cheap, expensive, but is {}".format(cost))
        
    fibCost = fib(level + 4) * 10  
    #print (fibCost)
    otherCost = 10 * totalLevels
    totalCost = (fibCost + otherCost) * _mult - alreadySpent
    return totalCost
