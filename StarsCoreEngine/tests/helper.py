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


class PlayerTestObject(object):
    """
    Player test object

    """

    def __init__(self):
        self.playerNumber = None
