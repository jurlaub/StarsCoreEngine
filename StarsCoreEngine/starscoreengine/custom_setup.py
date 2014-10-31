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


def customSetupDialog(template):
    """
    Warning... not robust!

    The custom setup dialog creates an interactive command line session allowing
    the game host to customize StandardGameTemplate values. The configuration 
    results are saved to an .ini file that can be used to generate future games.

    input: template = StandardGameTemplate.standardUniverse dictionary
    output: saves answers to an .ini file and returns dictionary to game.py

    The dialog will indicate the key and the standard value. A blank setting 
    results in the standard value

    """
    customTemplateDict = {}

    print("\n-" * 20 + "Custom Stars Universe" + "-" * 20 )
    print("\nThis is a basic command line interface to setup/generate a custom game.")
    print("Play nice and do not break it. Modify the resulting saved file if necessary.\n\n")

    ini_file_name = input("what do you want to name the .ini file? ")
    number_of_universes = int(input("How many universes do you want to play in? (1): "))
    number_of_players = int(input("How many players are in the universe total?: "))


    customTemplateDict['number_of_universes'] = number_of_universes
    customTemplateDict['number_of_players'] = number_of_players
    customTemplateDict['ini_file_name'] = ini_file_name + '.ini'



    for i in range(0, number_of_universes):
        universeDict = {}
        template["UniverseNumber"] = i
        print("\nIn Universe#%s" % i)
        

        for x in iter(template):
            if x == 'UniverseNumber':
                continue
            elif x == 'UniverseSizeXY':
                print("%s requires a tuple: make sure to add '()' around the xy pair" % x)

            print("'%s':%s" %(x, template[x]))
            tmpValue = input("What value do you want for %s: <%s>? " % (x, template[x]))
            if not tmpValue:
                tmpValue = template[x]
            universeDict[x] = tmpValue

        
        tmpUniverseName = 'UniverseNumber' + str(i)
        customTemplateDict[tmpUniverseName] = universeDict


    printCustomSetup(customTemplateDict)    

    #print("\n\ncustom file name: %s.ini : %s universe(s)" % (ini_file_name, number_of_universes))





def printCustomSetup(customDict):

    for i in iter(customDict):

        if isinstance(i, dict):
            for x in iter(i):
                print("'%s':%s" %(x, i[x]))
        else:
            print("%s: %s" % (i, customDict[i]))



