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
"""
RaceTemplate 

"""


# class RaceTemplate(object):

#     def __init__(self):
#         pass





def get_PRT_list():
    return ["HE", "SS", "WM", "CA", "IS", "SD", "PP", "IT", "AR", "JOAT"]


# PRT opening setup?


# def get_SS_template():
#     """ a PRT specific values. 

#     """
#     pass



def chooseBestShipComponents(techTree, techLevels, shipHull, ShipDesign):
    """ chooseBestShipComponents assists the Game object with selecting the best
    game components when generating a ship for players when starting a new game.

    input: techTree, raceData.techLevels, JSON shipHull, ShipDesign (empty).

    output: ShipDesign with the highest level components for the class that are 
    possible. (or standard components - like some general slots may have options, 
        like mechanical, but the mechanical options are hardwired. DD has extra 
        fuel capacity) 

    """

    pass



def colonyShip():
    shipName = "Santa Maria"
    shipDesign =    {       'designName': shipName, 
                            'designID': 0,
                            'hullID': 'Colony Ship',
                            'component':{   "B": {"itemID": "Daddy Long Legs 7", "itemQuantity": 1 },
                                            "A": {"itemID": "Colonization Module", "itemQuantity": 1}
                                        } 
                    }
    return shipName, shipDesign

def scoutShip():
    shipName = "Long Eye"
    shipDesign =    {       'designName': shipName, 
                            'designID': 0,
                            'hullID': 'Scout',
                            'component':{   "C": {"itemID": "Long Hump 6", "itemQuantity": 1 },
                                            "B": {"itemID": "Fuel Tank", "itemQuantity": 1 },
                                            "A": {"itemID": "Mole Scanner", "itemQuantity": 1}
                                        } 
                    }
    return shipName, shipDesign

def destroyerShip():
    shipName = "Defender"
    shipDesign =    {       'designName': shipName, 
                            'designID': 0,
                            'hullID': 'Destroyer',
                            'component':{   
                                            "G": {"itemID": "X-Ray Laser", "itemQuantity": 1 },
                                            "F": {"itemID": "X-Ray Laser", "itemQuantity": 1 },
                                            "E": {"itemID": "Manoeuvring Jet", "itemQuantity": 1 },
                                            "D": {"itemID": "Fuel Tank", "itemQuantity": 1 },
                                            "C": {"itemID": "Long Hump 6", "itemQuantity": 1 },
                                            "B": {"itemID": "Battle Computer", "itemQuantity": 1 },
                                            "A": {"itemID": "Tritanium", "itemQuantity": 2}
                                        } 
                    }
    return shipName, shipDesign

def smallFrieghterShip():
    shipName = "Grazing Cow"
    shipDesign =    {       'designName': shipName, 
                            'designID': 0,
                            'hullID': 'Small Freighter',
                            'component':{   "C": {"itemID": "Long Hump 6", "itemQuantity": 1 },
                                            "B": {"itemID": "Fuel Tank", "itemQuantity": 1 },
                                            "A": {"itemID": "Mole-skin Shield", "itemQuantity": 1}
                                        } 
                    }
    return shipName, shipDesign


def startingDesigns():
    colonyName, colonyDesign = colonyShip()
    scoutName, scoutDesign = scoutShip()
    destroyerName, destroyerDesign = destroyerShip()
    frieghtName, frieghtDesign = smallFrieghterShip()

    designs = {
        "NewDesign" : {
            colonyName : colonyDesign,
            scoutName : scoutDesign,
            destroyerName :destroyerDesign,
            frieghtName : frieghtDesign
        },
            "RemoveDesign" : []
    }

    return designs
