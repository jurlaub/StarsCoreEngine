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





def xFileController():
    """ xFileController 


    """

    pass

# method to call the game year? to find the current year?

def submissionsReady():
    """ submissionsReady - are all the .x files in the CWD? And are they all for
    the current year?

    call xFileExist()

    """
    pass


def xFileExist(gameName, playerNumber, currentYear):
    """
    Looks in CWD for an <gameName>.x<playerNumber> file 
    > does it contain the correct year?

    returns True/False

    """
    pass



# method to mv all years .x files to new directory <gamename_year> for 
# historical purposes, this process should be part of game configuration







