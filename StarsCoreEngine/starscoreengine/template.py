"""
    This file is part of Stars Core Engine, which provides an interface and 
    processing of Stars data. 

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
import random
from .player import RaceData



# -- define the universe data in a standard values object, similar format, 
class StandardGameTemplate(object):
    """
    StandardGameTemplate is a class for generating a standard universe. 
    
    The standard universe data can be modified by passing in a dictionary 
    containing key:value pairs which will be used to update the standard values.

    Use the provided command line arguments to create a custom universe file as 
    well as modify/add technology. 

    """
    '''
    #u_name = ["Prime", "Alpha", "Beta", "Gamma", "Delta", "Omega", "Zeta"]

    planet_density = (.5, 1, 1.5) 
    planets = 10
    standard_universe_size_small = {"UniverseSizeXY":(200,200)}
    standard_universe_size_medium = {"UniverseSizeXY":(600,600)}
    standard_universe_size_large = {"UniverseSizeXY":(1000,1000)}

    standard_universe = {"UniverseNumber":1, "UniverseSizeXY": (200,200), \
    "UniverseName":("Prime"), "UniversePlanets":planets, \
    "PlanetDensity": planet_density[1], "Players":(1)}
    '''

    # instantiate the standard object
    #                           customUniverse = {}, customTech = {}, customVC = {}
    def __init__(self, game_name = None, playerFileList = [], setupDict = {}, universeNumber = 1):
        # instantiates a new game dictionary while merging setup data
        
        # self.game_name = game_name # "rabid_weasels"
        if not game_name:
            self.game_name = "rabid_weasels"
        else:
             self.game_name = game_name # "rabid_weasels"

        self.planet_names = planetNameTemplate()
        self.starting_population = 50000
        self.universeNumber = int(universeNumber)
        self.universe_data = []    # list of universe dictionary data

        #self.technology_data       #template would have technology
        #self.victory_conditions    # standard VC template with changes        


        # ---- HARDCODED =>> requires updating custom setup
        # -- TODO --- Template grabs data from r1 files
        self.players_data = self.getPlayerRaceFile(playerFileList)    # list of player race file names 
        self.player_by_universe = None  # method to sort players into respective universes



        if universeNumber < 1:
            sys.exit("universeNumber must be greater then 1")
        else:

            for i in range(0, int(universeNumber)):
                x = self.standardUniverse()
                x['UniverseNumber'] = i

                #merge setupDict (the customized dictionary) with standard
                if setupDict:
                    tmp_universe = 'UniverseNumber' + str(i)
                    customUniverseObject = setupDict[tmp_universe]

                    x = self.mergeDictionaryData(x, customUniverseObject)

                self.universe_data.append(x)          # NOTE: appending to a list
                






    def standardUniverse(self):
        # standard universe comprises standard settings for 1 universe.

        standard_universe = {"UniverseNumber":0, "UniverseSizeXY": (200,200), \
        "UniverseName": "Prime", "UniversePlanets":6, "Players":1}
        
        return standard_universe

    @classmethod
    def homeworld():
        iron = 78
        bora = 67
        germ = 79


    def mergeDictionaryData(self, dict1, dict2):
        '''
        input: dict1, dict2
        output: dict1

        if items in dict2 are in dict1, merge those items into dict1
        '''

        for n in dict2:
            if n in dict1:
                dict1[n] = dict2[n]

        return dict1

    def getPlayerRaceFile(self, fileList):
        # 'race name'.r1
        # look for all r1 files in folder
        # should match number of players
        raceObjects = []

        for each in fileList:

            #--- TODO  change from grabbing a dev race to grabbing a .r1 file
            # and turning it into a RaceData() object
            raceObjects.append(self.getDevRaceFile(each))

        return raceObjects

    def getDevRaceFile(self, raceName):
        # returns a development file that will substitute as a player race file

        return RaceData(raceName)









def getPlanetNameFromTemplate():
    planet_names = planetNameTemplate()
    count = len(planet_names)
    rand = random.randrange(0, count)
    
    return planet_names[rand]

def planetNameTemplate():
    planet_names = ["Alan", "Fenge", "Fenris", "Shill", "239_Alf", "Wolf 359",\
     "Dark Star", "Kirk", "Flo Rida", "Pluto", "Centari", "Mau Tai", "Zeta", 
     "Mars", "Babylon 5", "Quell", "Be Still My Heart", "Soft Light",
     "Vertigo", "Verillon", "Camelot", "Too Much", "Avalon", "Quiver", 
     "Shining Star", "Bamboo II", "Deralon", "Dark Tide", "Everlon", "Eeek!",
     "Exegenesis", "Et'Varloon", "Gallifrey", "Geronimo", "Gytalli", "Hilda",
     "Harriot's Star", "Indigo", "Intel", "Inner Peace", "Jester's Crown", 
     "Jykle", "Kelly's Eye", "Kirkland", "Katie", "Loomiss", "Lester Pike",
     "Mea Tal", "Martoon", "Marcross", "McKenny", "McDevitton", "Reynold's Star",
     "Heinland", "Stross", "Brust", "Mat'Etvel", "Nooon", "Nubia", "Never Land",
     "Narly", "Opal",
     "Oster Den", "Old One", "Ol' Yeller", "Otaah", "Penelope's Star", "Piink",
     "Patrick's Way", "Pla'yet'Oh", "Pu Tai La", "Shei Gua", "Ping Loom", 
     "Q'atell", "007", "Bantha", "Betazoid", "Realist", "New Hope", "Recall",
     "Renovate This", "Sad Tide", "Sally Way", "Sol Two", "Shia Tell", 
     "Shitzu", "Sassyland", "Sardovia", "Telmarie", "Tennyson", "Termaso"
     "Terra", "Tar Rok", "Lok Tar", "Umbria", "Umbridge", "Unrepentant",
     "Unknown Star", "Un'Lo'Tek", "Ventillia", "Vargo II", "Vicktor's Star",
     "Vok'Ba", "Vot'Tark'Le", "Vessel", "Veree", "Ross 359", "Wolf Star", 
     "Wolf's Eye", "Moteland", "Wolfbane", "Transylvania", "Woe Tide", "Wode",
     "Woot", "Waco", "Wackyland", "Wat'up", "Wolfrik", "Yeet", "Yether", "Aether", "Yee",
     "Yent'il", "Yankee", "Coyote", "Yesterday", "Raster", "Xavier", "Xander",
     "Xandidu", "X-Factor", "Xidus", "Xtol", "Zeet", "Zak'To", "Zah'ha'dum", 
     "Zetherland", "Zoot", "4004da", "QWERTY"]
    return planet_names

def planetNamesFromFile():
    #--TODO--
    pass

