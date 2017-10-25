"""
    This file is part of Stars Core Engine, which provides an interface and processing of Game data.
    Copyright (C) 2017  <Joshua Urlaub + Contributors>

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



def findPlayerHW(colonies):
    """
    brief   : helper function to find player HW

    input   : individual player's dictionary of colonies

    output  : tuple (HW_key : HW_object) of first HW found in players dictionary of colonys

        NOTE: more then 1 HW in player colonies will not be found
    
    """
    hw_name = None
    hw_obj = None

    for kee, each in colonies.items():
        if each.planet.HW:
            hw_name = kee
            hw_obj = each
            break

    return (hw_name, hw_obj)



def _update_xy_orders(currentXY, offsetXY):

    return (currentXY[0] + offsetXY[0], currentXY[1] + offsetXY[1])



def obtain_fleet_orders_from_offset(currentLocation, offset ):

    temp = { "orders" : [ 
            {
            "coordinates" : _update_xy_orders(currentLocation, offset),    # or at currentLocation
            "velocity_command" : "speed_levels_from_list",
            "waypoint_action" : "action_from_list" 
            } ]
        }
    return temp

def _standard_offset():
    NORTH_OFFSET = (0, 50, 0)
    EAST_OFFSET = (50, 0, 0)
    SOUTH_OFFSET = (0, -50, 0)
    WEST_OFFSET = (-50, 0, 0)
    OFFSET_LIST = [NORTH_OFFSET, EAST_OFFSET, SOUTH_OFFSET, WEST_OFFSET ]

    return OFFSET_LIST

def generate_fleet_orders_from_standard_offset(fleetIDs, hw_xy):

    testCommands = {}

    # for each in fleetIDs:
    for x in range(0, len(fleetIDs)):
        testCommands[fleetIDs[x]] = obtain_fleet_orders_from_offset(hw_xy, _standard_offset()[x%4])
        #print(testCommands)

    return testCommands


class PlayerTestObject(object):
    """
    Player test object

    """

    def __init__(self):
        self.playerNumber = None




