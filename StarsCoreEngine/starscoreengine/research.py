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


class Research(object):
    
    # this collects all races research for the year. Its to calculate the SS spy bonus
    yearsResearch = {"energy" : {"racesResearchingField" : 0, "resourcesSpent" : 0}, 
              "weapons" : {"racesResearchingField" : 0, "resourcesSpent" : 0},
              "propulsion" : {"racesResearchingField" : 0, "resourcesSpent" : 0},
              "construction" : {"racesResearchingField" : 0, "resourcesSpent" : 0},
              "electronics" : {"racesResearchingField" : 0, "resourcesSpent" : 0},
              "biotechnology" : {"racesResearchingField" : 0, "resourcesSpent" : 0}
          }



    def __init__(self, PRT, LRTs = []):
        
        self.startLevels = {"energy" : 0, 
                  "weapons" : 0,
                  "propulsion" : 0,
                  "construction" : 0,
                  "electronics" : 0,
                  "biotechnology" : 0
              }

        self.startLevels = Research.set_base_tech(self.startLevels, PRT, LRTs)


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
    



def race_editor_tech_costs(numExpensive, numCheap, boxTicked):
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
