"""
    This file is part of Stars Core Engine, which provides an interface and processing of Stars data.
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

    Contributors to this project agree to abide by the interpretation expressed in the 
    COPYING.Interpretation document.

"""
"""

    use a dictionary of (x,y,z) coords along with space object id's to collect locations and other data

    d = {}
    l = d.setdefault((25,45), [])   # it returns the list associated with the first value or a new list
    l.append(355)
    l.append(655)

    

"""




from space_objects import SpaceObjects


class Fleets(SpaceObjects):
    """
        Fleets - can exist as a single ship. 

    """

    def __init__(self,args):
        super(Fleets, self).__init__()
        pass