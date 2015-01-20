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

game_xfile.py methods should not depend on being used by the command line. 




"""

"""
X file contains:


playerName : <playerName>,
currentYear : <submissionYear>,


NewShipDesign : { all info captured in ShipDesign notes from file stars_shipdesing},
RemoveShipDesign : [ShipDesign number],




"""





# def xFileController():
#     """ xFileController is used to import players .x files into the Game Object

#     """

#     pass

# method to call the game year? to find the current year?

def submissionsReady():
    """ submissionsReady - are all the .x files in the CWD? And are they all for
    the current year?

    call xFileExist()

    """
    pass


def xFileSubmissionForYear(gameName, playerNumber, currentYear):
    """
    Looks in CWD for an <gameName>.x<playerNumber> file 
    > does it contain the correct year?

    returns JSON Object, else None

    """
    pass



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



def validDesignForProduction(newDesign, techTree, techLevel, PRT, LRT):
    """ 
    input: design (ShipDesign),techTree, techLevel, PRT, LRT,
            
            calls PlayerDesigns.validDesignForProduction()
                which validates: 
                    Tech used is within tech Range
                    Tech used is permitted per PRT
                    Tech used is permitted per LRT


    output - returns newDesign with updated 'designValidForProduction':
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
    #   the hull.slot  'objectType' value must match 
    #   the component 'itemType' 
    #   the component number must be less then or equal to the hull.slot "slotsAvalable" number
    #   if any item is not a match return False

    #return True

    pass


