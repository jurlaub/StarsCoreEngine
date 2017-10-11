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
    > speciesData - player.method that produces this
    > techTree - player.method gen the most recent one planetaryInstallations 
    > playerDesigns Ships
    > playerDesigns Starbases

    List updated every Turn:
    > minus speciesData
    > refresh planetaryInstallations
    > refresh pD




    -------- ??? ---------
    Should this be used as a place to contain/present max values? ie the working 
    max used by the client?

    - 20150607 JU: probably not as this is game setup / planet value based
    _____________________




    """

    def __init__(self, playerN):
        # define where to obtain the information
        #self.speciesData = playerN.speciesData
        self.playerN = playerN

        self.buildList = {} #{"Mines" : { "itemType": "Mines", "targetItemsCost": [0,0,0,4]}}

        # ------ BuildList ------
        # pulls into the build list the initial values.
        self.buildList.update(self.buildCosts_Mine(self.playerN))
        self.buildList.update(self.buildCosts_Factory(self.playerN))
        self.buildList.update(self.buildCosts_PlanetScanner(self.playerN))
        self.buildList.update(self.buildCosts_PlanetDefenses(self.playerN))
    

    def buildCosts_StarbaseDesigns(self, playerN):
        pass

    def buildCosts_ShipDesigns(self, playerN):
        """

        Requests PlayerDesigns object to provide list of valid ship designs to 
        be built. 

        Conditions: 
            - PlayerDesigns must check if the player is capabile of building the
            design (tech level, PRT/LRT, other?)
            - PlayerDesigns must include ship mass. 
            - PlayerDesigns must provide costs (updated for tech miniturization)
            - > PlayerBuildList will not apply miniturization

        """

        pass

    def buildCosts_Mine(self, playerN):
        speciesData = playerN.speciesData

        m = "Mines"
        mCosts = [0, 0, 0, speciesData.mineCost]

        return { m: {"itemType": m, "targetItemsCost": mCosts} }

    def buildCosts_Factory(self, playerN):
        speciesData = playerN.speciesData

        f = "Factories"

        fGerm = 4
        if speciesData.factoryGermCost: 
            fGerm = 3
        
        fCosts = [0, 0, fGerm, speciesData.factoryCost]


        return { f: {"itemType": f, "targetItemsCost": fCosts} }



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


        -- TODO --
        Check speciesData for tech exclusions (like the LRT:No Advanced Scanners or
            other rules)



        """


        s = "PlanetaryScanner"
        currTechLevels = playerN.research.techLevels

        sName = findMaxTechnologyComponent(s, currTechLevels, playerN.techTree)
        sObj = playerN.techTree[sName]
        sCosts = [sObj.iron, sObj.bor, sObj.germ, sObj.resources]


        return {sName :{"itemType": s, "targetItemsCost":sCosts }}

    def buildCosts_PlanetDefenses(self, playerN):
        """

        -- TODO --
        need to check PRT & LRT for defense exclusions. 


        """

        d = "PlanetaryDefenses"
        currTechLevels = playerN.research.techLevels

        dName = findMaxTechnologyComponent(d, currTechLevels, playerN.techTree)
        dObj = playerN.techTree[dName]
        dCosts = [dObj.iron, dObj.bor, dObj.germ, dObj.resources]


        return { dName : {"itemType": d, "targetItemsCost":dCosts }}



