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

"""
This file collects all the methods necessary to import a players x file. It is 
separated from game_utility.py specifically because the x file relies on the 
client to correctly format the data. The x file format should be clearly 
described in this file and accurately followed by a client.

game_xfile.py methods are the x file interface. They should not depend on being 
used by the command line. The StarsCoreEngine could be included as a part of
another project where the game_xfile.py methods are called directly.

game_xfile.py should provide a means for validating an x file from the command 
line.


"""

from .game_utility import loadFileFromJSON



def xfile_TEMPLATE():
    """ xfile_TEMPLATE is the standard for xfiles. 

    If the x file requires changes. Change this method. Then run the tests. 
    (Tests should break if keys are revised or value types are incompatiable)

    # 20150131 - ju -> this structure may be worth considering.
    "key" : {"info": "text about key and anything else",
            "expectedType" : "", 
            "value": {}
            }


    """
    x = {
        "game_name" : "game_name",
        "fileType": "xfile",
        "playerName" : "playerName",
        "currentYear" : "submissionYear",
        

        "NewDesign" : 

                        {"NewDesign_1" : 
                            {
                                "designName": "doomShip1", 
                                "designID": 0,
                                "hullID": "Scout",
                                "component": 
                                    {
                                        "B": {"itemID": "Fuel Mizer", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Mole Scanner", "itemQuantity": 1}
                                    } 
                            },
                        "NewDesign_2" : 
                            {
                                "designName": "doomShip2", 
                                "designID": 1,
                                "hullID": "Scout",
                                "component": 
                                    {
                                        "B": {"itemID": "Fuel Mizer", "itemQuantity": 1 },
                                        "A": {"itemID": "Fuel Tank", "itemQuantity": 1},
                                        "C": {"itemID": "Mole Scanner", "itemQuantity": 1}
                                    } 
                            }                        

                        },
        "RemoveDesign" : ["Design ID", "Design ID", "Design ID"],
                                        
        "ProductionQ" : 
            {
                "player.colonies.ID" : 
                    { 
                        "productionOrder" : ["key1", "key2", "key3"],
                        "productionItems" : { }  
                    },
                "player.colonies.ID" : 
                    {
                        "productionOrder" : ["entryID1", "entryID2" ],
                        "productionItems" : { "entryID1" : {"quantity": 5, "productionID": "item1"}, "entryID2" : {} }
                    },
                "player.colonies.ID" : 
                    {
                        "productionOrder" : [ ],
                        "productionItems" : { }
                    }

            }





    }



    return x


def xFileController(game):
    """ xFileController is used to import players .x files into the Game Object
        Input:    Game object 
                  xfiles (for current year in CWD)     

        Output:     game updated with player xfile submissions

    """

    for player in game.players.values():
        fileName = ("%s.x%s") % (game.game_name, player.playerNumber)


        xfile = obtainXFile(fileName)


        errorMSG = ("year->%s: .x%s: ") % (str(game.year), str(player.playerNumber))
        
        if xfile:

            #test for xfile validity
            
            if int(xfile["currentYear"]) == int(game.year):
                """process the x file by updating the player object.
                """

                processFleets(xfile, player)
                processMinefields(xfile, player)
                processDesign(xfile, player, game.technology)
                processProductionQ(xfile, player)
                processMessagesFromPlayer(xfile, player)

            else:
                errorMSG = ("%s  Not current year -> (%s); ") % (errorMSG, xfile["currentYear"])

        else:
            errorMSG = ("%s  %s file unable to load; ") % (errorMSG, fileName)


        player.xfilestatus.append(errorMSG)


def obtainXFile(fileName):
    """
    try block should be in the loadFileFromJSON method.

    """

    try:
        xfile = loadFileFromJSON(fileName)
    
    except IOError as e:
        print("Unable to open %s" % fileName)

    else:  
        return xfile

    


def processFleets(xfile, playerObj):

    print("processing fleets for #%d: %s" % (playerObj.playerNumber, playerObj.raceName))


def processMinefields(xfile, playerObj): # ?player object or universe?
    
    pass



def processDesign(xfile, playerObj, techTree):

    designObj = playerObj.designs
    newDesigns = xfile["NewDesign"]
    removeDesigns = xfile["RemoveDesign"]

    # remove design from PlayerDesign.currentShips/Starbase ()



    # add design to PlayerDesign
    for eachDesign in newDesigns.values():

        #--TODO-- isShipDesignValid here
        #--TODO-- validDesignForProduction here
        

        designObj.addDesign(eachDesign, techTree)





    print("processing design for #%d: %s" % (playerObj.playerNumber, playerObj.raceName))




def processProductionQ(xfile, playerObj):
    """processProductionQ
    Input:  xfile, playerObj
    Output: Returns nothing
            all the player colonies ProductionQ objects have updated ProductionQ
            and ProductionLists

    If there is a change to the P_Q or P_L, then the whole thing is resent. 

    """

    colonyProduction = xfile["ProductionQ"]

    playerColonies = playerObj.colonies

    for kee, obj in colonyProduction.items():
        if kee in playerColonies:
            colonyQ = playerColonies[kee].productionQ
            
            if "productionOrder" in obj:
                colonyQ.productionOrder = obj["productionOrder"]
            
            if "productionItems" in obj:
                colonyQ.productionItems = obj["productionItems"]
        #print("Processed Q for %s" % kee)
        #print("%s" % obj)


    #print("processing productionQ for #%d: %s" % (playerObj.playerNumber, playerObj.raceName))



def processMessagesFromPlayer(xfile, message ):
    """
    This is the in game communication from one player to another. Their sent 
    messages should be delivered to a common class - as of yet unidentified.
    """
    pass





# def submissionsReady():
#     """ submissionsReady - are all the .x files in the CWD? And are they all for
#     the current year?

#     call xFileExist()

#     """
#     pass


# def xFileSubmissionForYear(gameName, playerNumber, currentYear):
#     """
#     Looks in CWD for an <gameName>.x<playerNumber> file 
#     > does it contain the correct year?

#     returns JSON Object, else None

#     """
#     pass



# method to mv all years .x files to new directory <gamename_year> for 
# historical purposes, this process should be part of game configuration

def createHistoryFolder():

    pass


def mvXFile():
    pass



def updatePlayerShipDesign():
    """ 
    input: player, gamespec, NewShipDesign, RemoveShipDesign

    output: updates player ship designs


    """

    # check remove ship design

    # check player ship designs count < game specification

    # if count below maximum, and new designs in NewShipDesign

    # then generate new design object from data in NewShipDesign


    pass


"""
Validate Ship Designs. 

1) validDesignForProduction - 
        Tech used is within tech Range
        Tech used is permitted per PRT
        Tech used is permitted per LRT
2) isShipDesignValid
        validates components correctly match the slots in Hull.
"""



def validDesignForProduction(newDesign, techTree, playerObj):
    """ 
    input: design (ShipDesign),techTree, playerObj(techLevel, PRT, LRT)
            
            calls PlayerDesigns.validDesignForProduction()
                which validates: 
                    Tech used is within tech Range
                    Tech used is permitted per PRT
                    Tech used is permitted per LRT


    output - returns newDesign with updated "designValidForProduction":
        True = Design is valid for production 
        False = Design is not valid for production

    """

    # obtain hull
    # does it meet techLevel?

    # for each component, 
    #       does it meet techLevel?
    #       does the PRT meet the Component requirements
    #       does the LRT meet the Component requirements

    # return newDesign

    pass

def isShipDesignValid(newDesign, techTree):
    """ validShipDesign assesses itself to determine if it is a valid ship 
    design. 

    Validates that the components added to the design align with the 
    Hull.slots. 

    input: newDesign, techTree
    output: 
        True = Ship Design has correct components, correct number of components
        False = Ship Design has an error

    """

    # find newDesign Hull
    # find hull in techTree

    # find component slot in hull

    # for each entry in newDesign.component
    #   is compared to the hull.slot entry
    #   the hull.slot  "objectType" value must match 
    #   the component "itemType" 
    #   the component number must be less then or equal to the hull.slot "slotsAvalable" number
    #   if any item is not a match return False

    #return True

    pass


def xFileIsValid(xfile):
    """
    This method tests that the xfile containes the correct objects/keys and 
    values match expected types. 

    """
    pass




