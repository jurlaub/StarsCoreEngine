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

#from .game import StandardGameTemplate.standardUniverse as template

'''
        Warning! 

        Tests not written for this file! 

        Code is not robust! 

'''
import json



def customSetupController(template, fileName = None):
    '''
    Warning... not robust!

    Controller to be used to determine if the custom setup should be saved to 
    file or immediately used (or both). 

    20141101 - Saves custom dialog to file and returns custom dictionary to game.py

    '''
    
    customTemplateDict = customSetupDialog(template, fileName)

    if fileName:
        dialogName = customTemplateDict['json_file_name']
        saveCustomSetupJSON(customTemplateDict, dialogName)
    
    return customTemplateDict




def saveCustomSetupJSON(customDict, fileName = 'testSetupFile.json'):
    '''
    Warning... not robust!

    saves the custom setup dictionary as json to a file for later use.

    ---- json != tuples -----
    json does not handle tuples. If tuples are needed to be saved - consider a 
    adding a special tool/utility to parse the dict before saving to json. The 
    tool should replace every tuple with a structure that can be loaded and 
    returned to a tuple state. See the stackoverflow:
    http://stackoverflow.com/questions/15721363/preserve-python-tuples-with-json

    '''

    with open(fileName, 'w') as fp:
        json.dump(customDict, fp, indent=4)


def loadCustomSetupJSON(fileName):
    '''
    Warning... not robust!

    given a fileName - load JSON values and convert to game dictionary to be 
    used to generate a game.

    NOTE: json - may need to add a special object hook to translate tuples stored in
    an alternative form 
    '''
    with open(fileName, 'r') as fp:
        setupObject = json.load(fp)

    #print("%s"%setupObject)
    return setupObject



def customSetupDialog(template, fileName):
    """
    Warning... not robust!

    The custom setup dialog creates an interactive command line session allowing
    the game host to customize StandardGameTemplate values. The configuration 
    results are saved to an .json file that can be used to generate future games.

    input: template = StandardGameTemplate.standardUniverse dictionary
    output: saves answers to an .json file and returns dictionary to game.py

    The dialog will indicate the key and the standard value. A blank setting 
    results in the standard value

    """
    customTemplateDict = {}


    # Custom Dialog open description
    print("\n\n\n\n%s%s%s" % ("-" * 20, "Custom Stars Universe", "-" * 20 ))
    print("\nThis is a basic command line interface to setup/generate a custom game.")
    print("Play nice and do not break it. Modify the resulting saved file if necessary.\n\n")

 
    # Custom Dialog starting values
    json_file_name = input('''This Custom Setup will be saved as: 
        <%s.json> 
        (Press enter to keep or type a new name): ''' % fileName)

    number_of_universes = input("How many universes do you want to play in? (1): ")
    number_of_players = int(input("How many players are in the universe total?: "))


    if not json_file_name:
        if (fileName[-5:] != '.json'):
            fileNmae = fileName + '.json'
        json_file_name = fileName
    else:
        json_file_name = json_file_name + '.json'


    # Adding starting values to dictionary
    customTemplateDict['json_file_name'] = json_file_name    
    customTemplateDict['number_of_universes'] = int(number_of_universes)
    customTemplateDict['number_of_players'] = int(number_of_players)



    #review all dictionary items contained within the 
    #StandardGameTemplate.standardUniverse() and add values to dictionary
    for i in range(0, int(number_of_universes)):
        universeDict = {}
        template["UniverseNumber"] = i
        print("\nIn Universe#%s" % i)
        

        for x in iter(template):

            # User cannot change the UniverseNumber - Hardcoded
            if x == 'UniverseNumber':
                continue
            
            # (x,y) tuple may require special handling
            elif x == 'UniverseSizeXY':
                print("%s requires a tuple: make sure to add '()' around the xy pair" % x)
                print("'%s':%s" %(x, template[x]))
                posx, posy = template[x]
                tmpValuea = input("What value do you want for x: <%s>? " % (posx))
                tmpValueb = input("What value do you want for y: <%s>? " % (posy))
                
                if not tmpValuea:
                    tmpValuea = posx
                if not tmpValueb:
                    tmpValueb = posy


                tmpValue = (int(tmpValuea), int(tmpValueb))             

            else:
                print("'%s':%s" %(x, template[x]))
                tmpValue = input("What value do you want for %s: <%s>? " % (x, template[x]))

            if not tmpValue:
                tmpValue = template[x]
            universeDict[x] = tmpValue

        
        # Hardcoded UniverseNumber
        tmpUniverseName = 'UniverseNumber' + str(i)

        # Added universe values to the dictionary
        customTemplateDict[tmpUniverseName] = universeDict


    printCustomSetup(customTemplateDict)    

    return customTemplateDict




def printCustomSetup(customDict):
    '''
    prints out the custom setup.
    '''

    print("\n\n\n%s%s%s\n" % ("-" * 20, "Custom Universe Values", "-" * 20))

    for i in iter(customDict):

        # prints out each dictionary item 1 layer deep
        if isinstance(customDict[i], dict):
            print(i)
            for x in iter(customDict[i]):
                print("'%s':%s" %(x, customDict[i][x]))
            print("\n")
        # prints out standard value if its not a dictionary
        else:
            print("%s: %s" % (i, customDict[i]))



