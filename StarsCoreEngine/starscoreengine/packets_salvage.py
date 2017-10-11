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

from .space_objects import SpaceObjects


class PacketsAndSalvage(SpaceObjects):
    """ Salvage in Standard Stars are minerals that can be retrieved by any who are co-located. Velocity is 0.
        Packets in Standard Stars minerals combined at a base with a Mass Driver (see tech tree) with a velocity(~5-14) 
        that typically has a planet destination. 
    """
    def __init__(self, arg):
        super(PacketsAndSalvage, self).__init__()
        self.arg = arg
        

