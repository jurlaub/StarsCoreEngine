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
import random
from .template import getPlanetNameFromTemplate, planetNameTemplate
from .planet import Planet, Colony


class UniverseObject(object):
    """
        The universe object should ultimately allow for the creation of multiple universes within a game.

        Within this context, a 'universe' means the space objects associated within the same 2d plane (should the game
         ever develop a 3rd dimension then space objects within a given cubic volume.) A multi-universe context would provide 
        multiple 'galaxies' of space objects that require access through a dimension shift. The respective x,y may shift 
        or may be congruent. In fact, when this becomes fully detailed, game hosts should be able to set the number of 
        universes, universe shifting tech, potential game turn information (as in universes provide delayed
            reporting of turn information) and other values that create delicious game play

        universe ID
        universe x,y size
        game play differences? (i.e. one has higher mineral concentration when game generates, different min
            depletion rates, )
        game races HW or starting players, partial starting players
        universe planet space objects
        universe other space objects (non-player)
        universe events
        universe variables



    """

    #--TODO-- PLANET_NAMES  new Universe accepts planet name list generated by game object
    def __init__(self, ID, universe_data, planet_names = []):
        self.ID = ID    # Key for universe in universe dictionary
        self.UniverseSizeXY = universe_data['UniverseSizeXY']
        self.UniverseName = universe_data['UniverseName']
        self.UniversePlanets = universe_data['UniversePlanets']
        self.Players = universe_data['Players']
        self.PlayerList = None  # which player races are located in this uni
        
        self.planets = self.createPlanetObjects()
        
        self.usedNames = []

        self.genericfleets = {} # fleet objects like Mystery Traders
        # other space objects
        # this is where a universe would initialize special rules and tech tree

          
        """
            use a dictionary of (x,y,z) coords along with space object id's to collect locations and other data

            d = {}
            l = d.setdefault((25,45), [])   # it returns the list associated with the first value or a new list
            l.append(355)
            l.append(655)
        """
        self.objectsAtXY = {} 


    #  need isAPlanet(XYLocation)


    def createPlanetObjects(self):
        """
        generates planet objects

        inputs:  universe data found in universe object
        returns: dictionary of planet objects

        """
        planets = {}


        uPlanet = int(self.UniversePlanets)
        uNumber = self.ID

        # create and add Planet objects with random locations, names and ID's
        for i in range(0, uPlanet):
            
            name = self.getPlanetName()
            ID = str(uNumber) + '_' + str(i)

            #generate Random Hab range?
            planetHab = (1.5, 123, 70)

            newPlanet = self.createPlanet(ID, name, planetHab)
            
            planets[ID] = newPlanet

        return planets



    def getPlanetName(self):

        name = getPlanetNameFromTemplate()

        return name



    def createPlanet(self, ID, name, playerHab):
        ''' createPlanet generates the initial planet values. 


        '''

        # -- TODO -- randomized planet values

        uSize = self.UniverseSizeXY
        xy = (random.randrange(0, uSize[0]), random.randrange(0, uSize[1]))
        tmpVal = Planet(xy, ID, name, playerHab)  # --TODO -- Add random values to Planet object
        
        return tmpVal




    def createHomeworldPlanet(self, raceData):
        # -- TODO --- a positional location of HWs based on some number

        count = len(self.planets)   # 0 based count == next planet number
        ID = str(self.ID) + '_' + str(count)  # new planet ID

        #**********************
        #Shuffling a new HW into the existing planet ID's so that HW's are not 
        #easily identified.
        #**********************
        switchID = str(self.ID) + '_' + str(random.randrange(0, count))


        switchPlanet = self.planets[switchID]
        switchPlanet.ID = ID    # Existing Planet takes in new planet ID
        self.planets[ID] = switchPlanet
        print("createHomeworldPlanet-switchPlanet: PlanetName:%s, IdNewToPlanet:%s, OldIDreplacedByLastEntry:%s, PlanetOwner:%s, IsPlanetAHW:%s" % (switchPlanet.name, switchPlanet.ID, switchID,  switchPlanet.owner, switchPlanet.HW))

        name = self.getPlanetName()
        playerHab = (raceData.habGravityCenter, raceData.habTempCenter, raceData.habRadCenter)
        
        homeworld = self.createPlanet(switchID, name, playerHab)   # HW takes existing planet ID
        homeworld.HW = True  
        homeworld.owner = raceData.raceName    
        print("createHomeworldPlanet-NewHW: HWName:%s, Id:%s, PlanetOwner:%s, IsPlanetAHW:%s" % (homeworld.name, homeworld.ID,  homeworld.owner, homeworld.HW))

        #homeworld.

        self.planets[switchID] = homeworld      # HW takes existing planet Key


        return homeworld




class UniverseEvents(object):
    """
        this class describes universe events that could happen every game turn. 
        on game creation the host can set each universe's settings including frequency of events.
        events could be new minerals, wormhole appearance, or negative.
        like a astroid impacting a planet. (severe negative impacts should not occur until later in the game)

        

    """
    pass

