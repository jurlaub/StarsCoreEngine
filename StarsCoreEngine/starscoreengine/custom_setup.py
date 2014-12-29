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
from .game_utility import saveFileToJSON
from .tech import *
from .template_tech import standard_tech_tree



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
        saveFileToJSON(customTemplateDict, dialogName)
    
    return customTemplateDict




# def saveCustomSetupJSON(customDict, fileName = 'testSetupFile.json'):
#     '''
#     Warning... not robust!

#     saves the custom setup dictionary as json to a file for later use.

#     ---- json != tuples -----
#     json does not handle tuples. If tuples are needed to be saved - consider a 
#     adding a special tool/utility to parse the dict before saving to json. The 
#     tool should replace every tuple with a structure that can be loaded and 
#     returned to a tuple state. See the stackoverflow:
#     http://stackoverflow.com/questions/15721363/preserve-python-tuples-with-json

#     '''

#     with open(fileName, 'w') as fp:
#         json.dump(customDict, fp, indent=4)


# def loadCustomSetupJSON(fileName):
#     '''
#     Warning... not robust!

#     given a fileName - load JSON values and convert to game dictionary to be 
#     used to generate a game.

#     NOTE: json - may need to add a special object hook to translate tuples stored in
#     an alternative form 
#     '''
#     with open(fileName, 'r') as fp:
#         setupObject = json.load(fp)

#     #print("%s"%setupObject)
#     return setupObject



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
    

    # -- TODO --
    # change to be input from user that turns user input into a list
    # choice should be to add race filenames, add blank template for later revision
    # or for user to specifically limit the number of race files in current working
    # directory to be the exact race files used in the game
    player_file_names = []

    for player in range(0, number_of_players):
        print("NEED to add interaction for user to input player race file name")
        
        tmpPlayer = 'player' + str(player)  # --TODO -- Interactive naming
        player_file_names.append(tmpPlayer)


    if not json_file_name:
        if (fileName[-5:] != '.json'):
            fileName = fileName + '.json'
        json_file_name = fileName
    else:
        json_file_name = json_file_name + '.json'


    # Adding starting values to dictionary
    customTemplateDict['json_file_name'] = json_file_name    
    customTemplateDict['number_of_universes'] = int(number_of_universes)
    customTemplateDict['number_of_players'] = int(number_of_players)
    customTemplateDict['player_file_names'] = player_file_names


    player_count = number_of_players

    # review all dictionary items contained within the 
    # StandardGameTemplate.standardUniverse() and add values to dictionary
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
                # print("%s requires a tuple: make sure to add '()' around the xy pair" % x)
                print("'%s':%s" %(x, template[x]))
                posx, posy = template[x]
                tmpValuea = input("What value do you want for x: <%s>? " % (posx))
                tmpValueb = input("What value do you want for y: <%s>? " % (posy))
                
                if not tmpValuea:
                    tmpValuea = posx
                if not tmpValueb:
                    tmpValueb = posy


                tmpValue = (int(tmpValuea), int(tmpValueb))             

            elif x == 'Players':
                tmpValue = input("There are %d players total. \nHow many players do you want in this universe? <%d left>: " % (number_of_players, player_count))
                
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




def printCustomSetup(customDict, uniVals = "Universe"):
    '''
    prints out the custom setup.
    '''
    title = "Custom %s Values" % uniVals

    print("\n\n\n%s%s%s\n" % ("-" * 20, title, "-" * 20))

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



def customTechDialog():
    """Create Technology Components File from Command Line
    """

    customTechDict = {}

    fileName = 'customTechTree'

    techTreeHelp = ''' Modifying the file values will result in changes to the 
    tech components. Modified Keys require changes to the code and is discouraged.

    If you want a custom component with "composite" properties (say both 
        electrical and a shield) - both types can be added to the one component.

    '''

    options = '''
    # option 1 - add a custom component - until user wants to stop
    # option 2 - (saved for later)
    # option 3 - (saved for later) (save standard tech tree to file) (overwrites)
    (1), (2), (3) ? 
    '''



    # Custom Dialog open description
    print("\n\n\n\n%s%s%s" % ("-" * 20, "Custom Stars Technology Tree", "-" * 20 ))
    print("\nThis is a basic command line interface to setup/generate custom tech components.")
    print("Play nice and do not break it. Modify the resulting saved file if necessary.\n\n")



    tech_file_name = input('''This Custom Tech Tree will be saved as: 
    <%s.tech> 
    (Press enter to keep or type a new name): ''' % fileName)

    # check if file exists - if so add a _1 to the end of the file.
    if not tech_file_name:
        tech_file_name = fileName + '.tech'
    else:
        if (tech_file_name[-5:] != '.tech'):
            tech_file_name = tech_file_name + '.tech'

    print("Ok... %s" % tech_file_name)



    customTechDict["help"] = techTreeHelp


    # option 1 - add a custom component - until user wants to stop
    # option 2 - (saved for later)
    # option 3 - (saved for later) (save all tech to file - new Custom Dictionary)


    # add while loop to allow for modifications of dict from command line

    opts = input(options)
    if opts == '1':
        customTechDict = customTechOption1(customTechDict)
    
    elif opts == '2':       # not implemented 
        customTechDict = customTechOption2(customTechDict)

    elif opts == '3':
        print("Saving the tech tree to .tech file. ")
        customTechDict = customTechOption3(customTechDict)  # currently overwrites customTechDict
    
    else:
        print("%s not a valid option- exit" % opt)

    
    printCustomSetup(customTechDict, "Technology")

    return tech_file_name, customTechDict



    
def customTechOption1(customTechDict):
    """ Users can add a component via command line interactive dialog.

    

    """
    typeValues = """
    All components have : (c)osts, (b)ase, (t)ech requirements

    Plus:   (a)rmor, (s)hields, (w)eapons, (e)ngines, (bo)mbs, (mi)nelayer, (El)ectrical,
            (O)rbital, (P)lanetary Installation, (m)echanical, (sc)anner, (h)ull,
            (T)erraforming <special> 
            
    (q)uit -> end adding types
    """

    cmpt = Component()


    print("----- Adding a New Component ----")

    while True:
        
        newItem = input("(n)ew component, (q)uit:")
        if newItem == "q":
            break

        
        print("new component attributes")

        tmpComponentDict = {}
        tmpName = input("name:")
        tmpType = input("type (%s):" % cmpt.objectTypes)        # need a list of types and names

        tmpComponentDict['name'] = tmpName
        tmpComponentDict['itemType'] = tmpType  

        #tmpComponentDict = addCustomTechType(tmpComponentDict, BaseTech())
        tmpComponentDict = addCustomTechType(tmpComponentDict, cmpt.costs())
        tmpComponentDict = addCustomTechType(tmpComponentDict, cmpt.techRequirements())

        while True:

            print(typeValues)
            tmpAddType = input("Add special features:")
            if tmpAddType == "q":
                break
            elif tmpAddType == "c":
                tmpObj = cmpt.costs()
            elif tmpAddType == "b":
                tmpObj = cmpt.base()              
            elif tmpAddType == "t":
                tmpObj = cmpt.techRequirements()
            elif tmpAddType == "a":
                tmpObj = cmpt.armor()
            elif tmpAddType == "s":
                tmpObj = cmpt.shields()
            elif tmpAddType == "w":
                tmpObj = cmpt.weapons()
            elif tmpAddType == "e":
                tmpObj = cmpt.engines()
            elif tmpAddType == "bo":
                tmpObj = cmpt.bombs()
            elif tmpAddType == "mi":
                tmpObj = cmpt.minelayer()
            elif tmpAddType == "El":
                tmpObj = cmpt.electronics()
            elif tmpAddType == "O":
                tmpObj = cmpt.orbital()
            elif tmpAddType == "P":
                tmpObj = cmpt.planetaryInstallations()
            elif tmpAddType == "m":
                tmpObj = cmpt.mechanical()
            elif tmpAddType == "h":
                tmpObj = cmpt.hull()
            elif tmpAddType == "sc":
                tmpObj = cmpt.scanner()
            elif tmpAddType == "T":
                tmpObj = cmpt.terraforming()
            else:
                print("*** Warning *** \nEntry not understood, try again")
                continue

            tmpComponentDict = addCustomTechType(tmpComponentDict, tmpObj)

        #print("after inner break")

        customTechDict[tmpName] = tmpComponentDict

    return customTechDict


def addCustomTechType(tmpComponentDict, typeObj):
    """

    """
    d = typeObj.__dict__

    print("\nEnter to keep '<value>' ")

    return mergeTechTree(tmpComponentDict, d)


def mergeTechTree(d1, d2):

    for eachKey in d2:
        if eachKey == 'itemType':
            continue
        elif eachKey == 'name':
            continue

        each = input("%s = %s : <%s>? " % (eachKey, d2[eachKey], d2[eachKey]))
        if not each:
            continue
        d1[eachKey] = each

    return d1


def customTechOption2(customTechDict):

    y = """Add 1 to N generic components to the tech tree JSON file. This allows 
editing of the tech component using a text file. 

*** Warning - do not modify the 'keys' part of the JSON file. ***

    """
    # use the Component() static methods along with collections.OrderedDict to 
    # create a usable structure for text editing

    print("Custom Tech Option 2 is not implemented")

    return customTechDict



def customTechOption3(customTechDict):
    customTechDict = standard_tech_tree()     # overwrites custom tech tree. 

    customTechDict["OnlyUseCustomTechTree"] = True  # Only use this tech tree


    return customTechDict



