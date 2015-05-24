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

import pickle
import json




def createMFile(game):
    

    # 

    #**********************************************
    #  For command line review:
    #        print out of planet information
    #       for dev only - remove.
    ##**********************************************

    print("-----------%s-----------" % game.game_name)  
    printGameValues(game)
    printPlayerValues(game) 
    
    print("""*** Players .m files are under development. ***
        The .m code is found in game_utility.py. """)




def createXYFile(game):
    ''' Generates the game .xy file for users.

    --TODO-- add tech tree. 
    
    '''
    # for each planet in universe, capture: ID, Name, XY, 
    xy_filename = game.game_name + '.xy'
    xy_data = {}

    planets_in_game = {} # key is existing key -> name
    technology_tree = {}    

    for universeKey in game.game_universe:
        universe = game.game_universe[universeKey]

        for planetKey in universe.planets:
            planet = universe.planets[planetKey]


            # planet data to be added to JSON file
            planetDict = {}
            planetDict['ID'] = planet.ID
            planetDict['name'] = planet.name
            planetDict['xy'] = planet.xy 


            planets_in_game[planetKey] = planetDict

    tmpTree = game.technology


    #     for eachKey in componentObj:
    #         eachObj = componentObj[eachKey]
    for componentKey, componentObj in tmpTree.items():
        tmpAttributes = {}
        componentDict = componentObj.__dict__

        
        for k, v in componentDict.items():
            tmpOpts = ['None', None, 'none']
            if v not in tmpOpts:
                tmpAttributes[k] = v 

        technology_tree[componentKey] = tmpAttributes





    xy_data['gamename'] = game.game_name
    xy_data['planets'] = planets_in_game
    xy_data['technology'] = technology_tree




    saveFileToJSON(xy_data, xy_filename)
    # call json encoder
    # with open(xy_filename, 'w') as fp:
    #     json.dump(planetList, fp, indent=4)


def saveFileToJSON(customDict, fileName = 'testSetupFile.json'):
    ''' Saves the stream (typically a dictionary) in json form to a file 
    for later use.

    ---- json != tuples -----
    json does not handle tuples. If tuples are needed to be saved - consider a 
    adding a special tool/utility to parse the dict before saving to json. The 
    tool should replace every tuple with a structure that can be loaded and 
    returned to a tuple state. See the stackoverflow:
    http://stackoverflow.com/questions/15721363/preserve-python-tuples-with-json

    '''

    with open(fileName, 'w') as fp:
        json.dump(customDict, fp, indent=6)


def loadFileFromJSON(fileName):
    ''' Given a fileName - load JSON values and convert to game dictionary to be 
    used to generate a game.

    NOTE: json - may need to add a special object hook to translate tuples 
    stored in an alternative form 
    '''
    with open(fileName, 'r') as fp:
        setupObject = json.load(fp)


    return setupObject


class GamePickle(object):

    def makePickle(fileName, p_object):
        with open(fileName, "bw") as a_file:    # file closed by the with statement
            pickle.dump(p_object, a_file)


    def unPickle(fileName):
        '''
        unpickle 

        requires a fileName,
            - test if the name uses the game name or fileName (i.e. <name>.hst)
            - add .hst and other values to unpack relevant values

        returns a number of objects:
            gameTemplate = StandardGameTemplate
            game = data after Game
        '''
        with open(fileName, "rb") as fn:
            #(gameTemplate, game) = pickle.load(fn)
            #p_object = pickle.load(fn)
            #return p_object
            return pickle.load(fn)


def printGameValues(game):
    for zz in iter(game.game_universe):
        print("\t%s%s%d%s"%('-'*20, 'UniverseNumber:', zz,'-'*20 ))

        for x in iter(game.game_universe[zz].planets):
            
            nn = game.game_universe[zz].planets[x]

            temp, grav, rad = nn.origTemp, nn.origGrav, nn.origRad
            ironC, borC, germC = nn.concIron, nn.concBor, nn.concGerm 
            print("ID:%s, %s:  %s  - Owner:%s" % (nn.ID, nn.name, nn.xy, nn.owner))
            print("\tEnvironment: \t\t(%sc, %sg, %smr) " % (temp, grav, rad))
            print("\tMineral Concentration: \t(i:%skt, b:%skt, g:%skt)" % (ironC, borC, germC))





def printPlayerValues(game):
    print("\n%s%s%s" % ('-'*10, '**** Players ****', '-' * 10))
    
    for player in iter(game.players):
        playerObject = game.players[player]
        print("%s" % ( playerObject.raceName ))
        print("Population growth rate: %s" % str(playerObject.raceData.growthRate))
        print("%s has %d planets" % (playerObject.raceName, len(playerObject.colonies)))

        for each in playerObject.colonies:
            colony = playerObject.colonies[each]
            print("%s : %d colonists" % (colony.planet.name, colony.population))


    print("\nFor game: %s, the year is %d\n" % (game.game_name, game.year))




def findMaxTechnologyComponent(targetType, techLevels, techTree):
    """

    There must be a better way to compare tech components.

    returns highest tech component for a given type

    """
    tmpName = ""
    tmpObj = {}
    tmpTechLevelSum = 0

    

    for eachName, eachObj in techTree.items():
        
        if eachObj["itemType"] == targetType:
            withinTechLevel = True
            sumEachObjLevel = 0
            
            for techName, techVal in techLevels.items():
                if eachObj[techName] > techVal:
                    #continue # will this continue the techLevel loop or the techTree loop?
                    withinTechLevel = False
                
                sumEachObjLevel += eachObj[techName]



            if withinTechLevel and tmpName == "":  # the first correct value
                tmpName = eachName
                tmpObj = eachObj
                tmpTechLevelSum = sumEachObjLevel

            elif tmpTechLevelSum < sumEachObjLevel:
                tmpName = eachName
                tmpObj = eachObj
                tmpTechLevelSum = sumEachObjLevel
            
            else:

                continue






    return tmpName




