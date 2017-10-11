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





class Token:
    """Ships of the same design in a fleet form a single token, contains everything needed
    for the battles, needs to persist after battles to keep damage"""

    def __init__(self, designID, numbers, damage = 0):
        self.designID = designID 
        self.number = numbers
        #list of [[number, damage (%)], ..., so [100, 0.5], [100, 0] is a token of 200 ships, 100 of which have 50% damage
        self.damage = damage  
       
        #used in battle
        self.armor = None
        self.shields = None
        #modified every turn in battle
        self.mass = None




