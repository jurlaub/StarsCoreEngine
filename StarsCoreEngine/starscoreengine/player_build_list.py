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

from .game_utility import findMaxTechnologyComponent


class PlayerBuildList(object):
    """
    PlayerBuildList collects information from different components and generates
    a list of possible items to be produced by a players ProductionQ.
    This list is a super-set of all producable items for all productionQ's


    player designs + research = research costs

    initial list:
    > Mines
    > Factories
    > Minerals
    > Planetary Installations

    > on init - check if designs exist and add these if valid



    source for data
    > raceData - player.method that produces this
    > techTree - player.method gen the most recent one planetaryInstallations 
    > playerDesigns Ships
    > playerDesigns Starbases

    List updated every Turn:
    > minus raceData
    > refresh planetaryInstallations
    > refresh pD




    -------- ??? ---------
    Should this be used as a place to contain/present max values? ie the working 
    max used by the client?
    _____________________




    """

    def __init__(self, playerN):
        # define where to obtain the information
        #self.raceData = playerN.raceData
        self.playerN = playerN

        self.buildList = {} #{"Mines" : { "itemType": "Mines", "targetItemsCost": [0,0,0,4]}}

        self.buildList.update(self.buildCosts_MineFactory(self.playerN))
        self.buildList.update(self.buildCosts_PlanetScanner(self.playerN))
        self.buildList.update(self.buildCosts_PlanetDefenses(self.playerN))
    

    def buildCosts_StarbaseDesigns(self, playerN):
        pass

    def buildCosts_ShipDesigns(self, playerN):
        pass

    def buildCosts_MineFactory(self, playerN):
        raceData = playerN.raceData

        m = "Mines"
        f = "Factories"

        
        mCosts = [0, 0, 0, raceData.mineCost]


        fGerm = 4
        if raceData.factoryGermCost: 
            fGerm = 3
        
        fCosts = [0, 0, fGerm, raceData.factoryCost]


        return { m:{"itemType": m, "targetItemsCost": mCosts}, \
                f: {"itemType": f, "targetItemsCost": fCosts} }

    def buildCosts_PlanetScanner(self, playerN):
        """

        --- PlanetaryScanner ---
        Should this present "Planetary Scanner"? OR the actual scanner to be built?
        The current plan is that the max scanner will be built/used -- all 
        scanners will be upgraded when the next higher level is reached. Managing
        this seems to added nuiance for little gameplay benefit. 

        If a non-standard tech tree were involved providing multiple planetary scanner
        options, then presenting all options and perhaps requiring upgrading would
        make sense.


        """


        s = "PlanetaryScanner"
        currTechLevels = playerN.research.techLevels

        sName = findMaxTechnologyComponent(s, currTechLevels, playerN.techTree)
        sObj = playerN.techTree[sName]
        sCosts = [sObj.iron, sObj.bor, sObj.germ, sObj.resources]


        return {sName :{"itemType": s, "targetItemsCost":sCosts }}

    def buildCosts_PlanetDefenses(self, playerN):
        """


        """

        d = "PlanetaryDefenses"
        currTechLevels = playerN.research.techLevels

        dName = findMaxTechnologyComponent(d, currTechLevels, playerN.techTree)
        dObj = playerN.techTree[dName]
        dCosts = [dObj.iron, dObj.bor, dObj.germ, dObj.resources]


        return { dName : {"itemType": d, "targetItemsCost":dCosts }}



